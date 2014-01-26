import math
import time
from Togetic.Server.AbstractServer import AbstractServer

class NoiseFilter(object):
    def __init__(self, size, distance)
        super(NoiseFilter, self).__init__()
        self.size = size
        self.distance = distance
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
        return self.hist[-1]

    def add_value(self, value):
        self.sum += value
        self.sq_sum += value ** 2
        self.hist += [value]

        if len(self.hist) > self.size:
            self.sum -= self.hist[0]
            self.sq_sum -= self.hist[0] ** 2
            self.hist = self.hist[1:]

        if (v - self.avg) ** 2 > self.distance * self.sq_std:
            return self.avg
        return v

class FilterHandler(AbstractServer):
    def __init__(self, input_shm, output_shm):
        AbstractServer.__init__(self)
        self._in_shm = input_shm
        self._out_shm = output_shm
        self._time = None

        self.pos = tuple([NoiseFilter(1, 3) for _ in range(3)])
        self.ang = tuple([NoiseFilter(1, 3) for _ in range(3)])

        self.fX, self.fY, self.fZ = 0, 0, 0

        self.gyr = tuple([NoiseFilter(10, 3) for _ in range(3)])

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
            a = tuple(in_data[1:4])
            g = tuple(in_data[4:7])
            c = tuple(in_data[7:10])

            print('B', g[0], g[1], g[2])
            g = tuple([gyr.add_value(v) for gyr, v in zip(self.gyr, g)])
            print('A', g[0], g[1], g[2])

            self.fX = a[0] * alpha + (self.fX * (1 - alpha))
            self.fY = a[1] * alpha + (self.fY * (1 - alpha))
            self.fZ = a[2] * alpha + (self.fZ * (1 - alpha))

            # self._p = math.atan2(self.fX, math.sqrt(self.fY**2 + self.fZ**2))
            # self._r = math.atan2(-self.fY, self.fZ)
            # self._y = 0

            def angle(old, gyro):
                return old + dt * gyro

            self.ang = tuple([ang.add_value(angle(ang.value, vg))
                for ang, vg in zip(self.ang, g)])

            x, y, z = [pos.value for pos in self.pos]
            p, r, y = [ang.value for ang in self.ang]
            x, y, z = 0, 0, 0
            out_data = t, x, y, z, p, r, y
            self._out_shm.data = out_data
            self._time = t
        time.sleep(0.01)

    def _free(self):
        pass
