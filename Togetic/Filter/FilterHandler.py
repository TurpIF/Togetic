import math
import time
from Togetic.Server.AbstractServer import AbstractServer

def noise_f(distance):
    def _noise_f(value, histo):
        if (value - histo.avg) ** 2 > distance * histo.std:
            return histo.avg
        return value
    return _noise_f

def lowpass_f(alpha):
    def _lowpass_f(value, histo):
        if len(histo.hist) >= 2:
            return histo.hist[-2] * alpha + value * (1.0 - alpha)
        return value
    return _lowpass_f

class Histo(object):
    def __init__(self, size):
        super(Histo, self).__init__()
        self.size = size
        self.hist = []
        self.sum = 0
        self.sq_sum = 0

    @property
    def avg(self):
        if len(self.hist) == 0:
            return 0
        return self.sum * 1.0 / len(self.hist)

    @property
    def std(self):
        if len(self.hist) == 0:
            return 0
        return (self.sq_sum - self.sum) * 1.0 / len(self.hist)

    @property
    def value(self):
        if not self.hist:
            return 0
        return self.hist[-1]

    def add_value(self, value):
        self.sum += value
        self.sq_sum += value ** 2
        self.hist += [value]

        if len(self.hist) > self.size:
            self.sum -= self.hist[0]
            self.sq_sum -= self.hist[0] ** 2
            self.hist = self.hist[1:]

class FilterHandler(AbstractServer):
    def __init__(self, shm_serial, shm_kinect, output_shm):
        AbstractServer.__init__(self)
        self._serial_shm = shm_serial
        self._kinect_shm = shm_kinect
        self._out_shm = output_shm
        self._time = None

        self.pos = [Histo(1) for _ in range(3)]
        self.ang = [Histo(10) for _ in range(3)]
        self.acc = [Histo(10) for _ in range(3)]
        self.gyr = [Histo(50) for _ in range(3)]
        self.com = [Histo(10) for _ in range(3)]

    def _serve(self):
        alpha = 0.5

        serial_data = self._serial_shm.data
        # self._serial_shm.data = None
        if serial_data is not None and len(serial_data) == 10:
            # print(in_data)
            if self._time is None:
                self._time = serial_data[0]
                return
            t = serial_data[0]
            dt = t - self._time
            a = serial_data[1:4]
            g = serial_data[4:7]
            c = serial_data[7:10]

            for h, v in zip(self.gyr, g):
                h.add_value(v)
            g = [h.value for h in self.gyr]
            g = [noise_f(3)(v, h) for v, h in zip(g, self.gyr)]

            for h, v in zip(self.com, c):
                h.add_value(v)
            c = [h.value for h in self.com]
            c = [noise_f(3)(v, h) for v, h in zip(c, self.com)]

            for h, v in zip(self.acc, a):
                h.add_value(v)
            a = [h.value for h in self.gyr]
            a = [noise_f(3)(v, h) for v, h in zip(a, self.acc)]
            a = [lowpass_f(0.5)(v, h) for v, h in zip(a, self.acc)]

# TODO verifier qu'on est pas superieur a 1.3G de norme
            vax = math.atan2(a[0], math.sqrt(a[1]**2 + a[2]**2))
            vay = math.atan2(a[1], math.sqrt(a[0]**2 + a[2]**2))
            if a[2] < 0:
                vay = math.pi / 2.0 +  (math.pi / 2.0 - math.copysign(vay, a[1]))
            # vay = math.atan2(-a[1], a[2])
            vgx = self.ang[0].value + dt * g[0]
            vgy = self.ang[1].value + dt * g[1]
            vgz = self.ang[2].value + dt * g[2]
            alpha = 0.1
            vx = vax * alpha + vgx * (1 - alpha)
            vy = vay * alpha + vgy * (1 - alpha)
            vaz = 0
# TODO gerer les divisions par zero
            # vaz = math.atan((c[0] * math.cos(vy) \
            #         + c[1] * math.sin(vx) * math.sin(vy) \
            #         - c[2] * math.cos(vx) * math.sin(vy)) \
            #         / (c[1] * math.cos(vx) \
            #         + c[2] * math.sin(vx)))
            # vx = 0
            # vy = 0
            # vgz = 0
            self.ang[0].add_value(vx)
            self.ang[1].add_value(vy)
            # self.ang[2].add_value(vaz * alpha + vgz * (1 - alpha))
            self.ang[2].add_value(vgz)
            # for h, v in zip(self.ang, g):
            #     val = h.value + dt * v
            #     h.add_value(val)
            ang = [h.value for h in self.ang]
            ang = [noise_f(3)(v, h) for v, h in zip(ang, self.ang)]
            # print('A', ang[0], ang[1], ang[2])
            # print('a', str(a[0])[:6], str(a[1])[:6], str(a[2])[:6])
            # ang = [lowpass_f(0.5)(v, h) for v, h in zip(ang, self.ang)]

# kinect

            x, y, z = self.pos[0].value, self.pos[1].value, self.pos[2].value
            kinect_data = self._kinect_shm.data
            print('K', kinect_data)
            if kinect_data is not None and len(kinect_data) == 4:
                kx = -(kinect_data[1] + 140) / 20.0
                ky = -(kinect_data[3] - 1000) / 20.0
                kz = (kinect_data[2] - 0) / 20.0
                self.pos[0].add_value(kx)
                self.pos[1].add_value(ky)
                self.pos[2].add_value(kz)
                pos = [h.value for h in self.pos]
                pos = [noise_f(3)(v, h) for v, h in zip(pos, self.pos)]
                x, y, z = pos

            u, v, w = ang
            u, v, w = 0, 0, 0
            out_data = t, x, y, z, u, v, w
            # print('O', out_data)
            self._out_shm.data = out_data
            self._time = t
        time.sleep(0.01)

    def _free(self):
        pass

