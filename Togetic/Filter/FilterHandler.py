import math
import time
from Togetic.Server.AbstractServer import AbstractServer

class FilterHandler(AbstractServer):
    def __init__(self, input_shm, output_shm):
        AbstractServer.__init__(self)
        self._in_shm = input_shm
        self._out_shm = output_shm
        self._time = None

        self.gyro_sens = 1#6500000.536
        self.accel_sens = 1

        self._x = 0
        self._y = 0
        self._z = 0

        self._pitch = 0
        self._roll = 0
        self._yaw = 0

        self.fX, self.fY, self.fZ = 0, 0, 0

        self._gyr = []
        self._gyr_avg = None
        self._gyr_sq_avg = None
        self._gyr_size = 50
        self._gyr_dist = 3

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
            acc_x, acc_y, acc_z = in_data[1:4]
            gyr = gyr_x, gyr_y, gyr_z = in_data[4:7]
            mag_x, mag_y, mag_z = in_data[7:10]

            print('B', gyr_x, gyr_y, gyr_z)
            if len(self._gyr) == 0:
                self._gyr = [gyr for _ in range(self._gyr_size)]
                self._gyr_avg = self._gyr[0]
                self._gyr_sq_avg = tuple([self._gyr_size * d**2
                    for d in self._gyr[0]])
            else:
                std_sq = tuple([sq_avg / self._gyr_size - avg**2
                    for sq_avg, avg in zip(self._gyr_sq_avg, self._gyr_avg)])

                self._gyr_avg = tuple([avg + (v - old) / self._gyr_size
                    for old, v, avg in
                    zip(self._gyr[0], gyr, self._gyr_avg)])
                self._gyr_sq_avg = tuple([sq_avg + (v**2 - old**2)
                    for old, v, sq_avg in
                    zip(self._gyr[0], gyr, self._gyr_sq_avg)])
                self._gyr = self._gyr[1:] + [gyr]

                if False in [(v - avg)**2 <= self._gyr_dist * s
                        for v, avg, s in zip(gyr, self._gyr_avg, std_sq)]:
                    gyr = gyr_x, gyr_y, gyr_z = self._gyr_avg

            print('A', gyr_x, gyr_y, gyr_z)
            self.fX = acc_x * alpha + (self.fX * (1 - alpha))
            self.fY = acc_y * alpha + (self.fY * (1 - alpha))
            self.fZ = acc_z * alpha + (self.fZ * (1 - alpha))

            # self._pitch = math.atan2(self.fX, math.sqrt(self.fY**2 + self.fZ**2))
            # self._roll = math.atan2(-self.fY, self.fZ)
            # self._yaw = 0

            self._pitch += dt * gyr_x
            self._roll += dt * gyr_y
            self._yaw += dt * gyr_z

            # force = abs(acc_x) + abs(acc_y) + abs(acc_z)
            # if True or 8192 < force < 32768:
            #     pitch_acc = math.atan2(acc_y, acc_z) * 180 / math.pi
            #     self._pitch = self._pitch * 0.98 + pitch_acc * 0.02;

            # self._pitch %= math.pi
            # self._roll %= math.pi
            # self._yaw %= math.pi

            # print((self._pitch, self._roll))

            x = acc_x
            y = acc_y
            z = acc_z
            # print(x*x+y*y+z*z)
            theta = self._pitch
            phi = self._roll
            psy = self._yaw
            # theta = gyr_x
            # phi = gyr_y
            # psy = gyr_z
            x, y, z = 0, 0, 0
            out_data = t, x, y, z, theta, phi, psy
            self._out_shm.data = out_data
            self._time = t
        time.sleep(0.01)

    def _free(self):
        pass
