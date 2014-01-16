import math
from Togetic.Server.AbstractServer import AbstractServer

class FilterHandler(AbstractServer):
    def __init__(self, input_shm, output_shm):
        AbstractServer.__init__(self)
        self._in_shm = input_shm
        self._out_shm = output_shm
        self._time = None

        self.gyro_sens = 6500000.536
        self.accel_sens = 81920000

        self._x = 0
        self._y = 0
        self._z = 0

        self._pitch = 0
        self._roll = 0
        self._yaw = 0

    def _serve(self):
        in_data = self._in_shm.data
        if in_data is not None and len(in_data) == 10:
            if self._time is None:
                self._time = in_data[0]
                return
            time = in_data[0]
            dt = time - self._time
            acc_x, acc_y, acc_z = map(lambda x: x / self.accel_sens,
                    in_data[1:4])
            gyr_x, gyr_y, gyr_z = map(lambda x: x / self.gyro_sens,
                    in_data[4:7])
            mag_x, mag_y, mag_z = in_data[7:10]

            # self._pitch += gyr_x * dt
            # self._roll += gyr_y * dt
            # self._yaw = 0

            # force = abs(acc_x) + abs(acc_y) + abs(acc_z)
            # if True or 8192 < force < 32768:
            #     pitch_acc = math.atan2(acc_y, acc_z) * 180 / math.pi
            #     self._pitch = self._pitch * 0.98 + pitch_acc * 0.02;

            # self._pitch %= math.pi
            # self._roll %= math.pi
            # self._yaw %= math.pi

            # print((self._pitch, self._roll))

            x = time
            y = 1
            z = 6
            theta = self._pitch
            phi = self._roll
            psy = self._yaw
            out_data = time, x, y, z, theta, phi, psy
            print(out_data)
            self._out_shm.data = out_data
            self._time = time

    def _free(self):
        pass
