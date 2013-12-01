import math
from Togetic.Server.AbstractServer import AbstractServer

class FilterHandler(AbstractServer):
    def __init__(self, input_shm, output_shm):
        AbstractServer.__init__(self)
        self._in_shm = input_shm
        self._out_shm = output_shm
        self._time = None

        self.gyro_sens = 1
        self.accel_sens = 1

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

            self._pitch += gyr_x * dt
            self._roll += gyr_y * dt
            self._yaw += gyr_z * dt

            dt2 = dt * dt
            self._x += acc_x * dt2
            self._y += acc_y * dt2
            self._z += acc_z * dt2

            self._pitch %= math.pi
            self._roll %= math.pi
            self._yaw %= math.pi

            x = self._x
            y = self._y
            z = self._z
            theta = self._pitch
            phi = self._roll
            psy = self._yaw
            out_data = time, x, y, z, theta, phi, psy
            self._out_shm.data = out_data

    def _free(self):
        pass
