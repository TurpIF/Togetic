import math
import time
from Togetic.Server.AbstractServer import AbstractServer

def noise_filter(distance):
    def _noise_filter(value, avg, sq_std):
        if (value - avg) ** 2 > distance * sq_std:
            return avg
        return value
    return _noise_filter

class Histo(object):
    def __init__(self, size)
        super(NoiseFilter, self).__init__()
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
    def sq_std(self):
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
    def __init__(self, input_shm, output_shm):
        AbstractServer.__init__(self)
        self._in_shm = input_shm
        self._out_shm = output_shm
        self._time = None

        self.pos = tuple([Histo(1) for _ in range(3)])
        self.ang = tuple([Histo(1) for _ in range(3)])

        self.acc = tuple([Histo(1) for _ in range(3)])
        self.fX, self.fY, self.fZ = 0, 0, 0

        self.gyr = tuple([Histo(10) for _ in range(3)])

    def _serve(self):
        alpha = 0.5

        in_data = self._in_shm.data
        self._in_shm.data = None
        if in_data is not None and len(in_data) == 10:
            # print(in_data)
            if self._time is None:
                self._time = in_data[0]
                return
            t = in_data[0]
            dt = t - self._time
            a = in_data[1:4]
            g = in_data[4:7]
            c = in_data[7:10]

            for h, v in zip(self.gyr, g):
                h.add_value(v)
            g = [noise_filter(3)(h.value, h.avg, h.sq_std) for h in self.gyr]

            self.fX = a[0] * alpha + (self.fX * (1 - alpha))
            self.fY = a[1] * alpha + (self.fY * (1 - alpha))
            self.fZ = a[2] * alpha + (self.fZ * (1 - alpha))

            # self._p = math.atan2(self.fX, math.sqrt(self.fY**2 + self.fZ**2))
            # self._r = math.atan2(-self.fY, self.fZ)
            # self._y = 0

            for h, v in zip(self.ang, g):
                val = h.value + dt * v
                h.add_value(val)
            ang = [noise_filter(3)(h.value, h.avg, h.sq_std) for h in self.ang]

            for h in self.ang:
                h.add_value(0)
            pos = [noise_filter(3)(h.value, h.avg, h.sq_std) for h in self.pos]

            x, y, z = pos
            p, r, y = ang
            x, y, z = 0, 0, 0
            out_data = t, x, y, z, p, r, y
            self._out_shm.data = out_data
            self._time = t
        time.sleep(0.01)

    def _free(self):
        pass
