import time
import math
import serial

from Togetic.shm import shm

from Togetic.Server.AbstractServer import AbstractServer
from Togetic.Server.Listener import Listener

from Togetic.Sensor.Emitter import Emitter
from Togetic.Sensor.SerialHandler import SerialHandler

class ThreadedSensor(AbstractServer):
    def __init__(self, addr_input, addr_output):
        AbstractServer.__init__(self)

        # Offset en bits
        # gyr_offset_x = 4.18973187447
        # gyr_offset_y = -7.3076830588
        # gyr_offset_z = 14.5367319947
        acc_scale = 1.0 # bits -> mg -> g
        gyr_scale = math.pi / 180.0 * 8.75 / 1000 # bits -> deg -> rad

        tr_accel = lambda bits, avg: (
                (bits[0] - avg[0]) * 0.00376390 * acc_scale,
                (bits[1] - avg[1]) * 0.00376009 * acc_scale,
                (bits[2] - avg[2]) * 0.00349265 * acc_scale + 1)
        tr_gyro = lambda bits, avg: (
                (bits[0] - avg[0]) * gyr_scale,
                (bits[1] - avg[1]) * gyr_scale,
                (bits[2] - avg[2]) * gyr_scale)
        tr_compass = lambda bits: (
                0.019292 * (bits[0] - 50.097),
                0.019780 * (bits[1] + 313.964),
                0.018400 * (bits[2] - 197.500))

        transformation = lambda bits, a_avg, g_avg: (
            tr_accel(bits[0:3], a_avg) +
            tr_gyro(bits[3:6], g_avg) +
            tr_compass(bits[6:9]))

        shm_data = shm()
        # shm_accel = shm()
        # shm_gyro = shm()
        # shm_compass = shm()
        shm_serial = shm(serial.Serial(addr_input, 115200, timeout=0.01))
        self._handler = SerialHandler('R', 'r', transformation, shm_serial, shm_data)
        # self._accel_handler = SerialHandler('A', 'a', tr_accel, shm_serial, shm_accel)
        # self._gyro_handler = SerialHandler('G', 'g', tr_gyro, shm_serial, shm_gyro)
        # self._compass_handler = SerialHandler('C', 'c', tr_compass, shm_serial, shm_compass)
        self._emitter = Listener(addr_output,
            Emitter(shm_data)) #shm_accel, shm_gyro, shm_compass))

    def start(self):
        time.sleep(5) # Wait for the serial to be ready
        for s in [
                # self._accel_handler,
                # self._gyro_handler,
                # self._compass_handler,
                self._handler,
                self._emitter]:
            s.start()
        AbstractServer.start(self)

    def _serve(self):
        time.sleep(0.5)

    def _free(self):
        for s in [
                # self._accel_handler,
                # self._gyro_handler,
                # self._compass_handler,
                self._handler,
                self._emitter]:
            print('Stopping ', s)
            s.stop()
            s.join(2)
            print(s, 'stopped')

if __name__ == '__main__':
    addr_input = '/dev/ttyACM1'
    addr_output = '/tmp/togetic-sensor'
    f = ThreadedSensor(addr_input, addr_output)
    try:
        f.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        f.stop()
        f.join(2)
        sys.exit()
