#!/bin/env python3

import sys
sys.path += ['..']

from shm import shm

from Server.AbstractServer import AbstractServer
from Server.Listener import Listener

from Sensor.Emitter import Emitter
from Sensor.AccelHandler import AccelHandler
from Sensor.MagnetHandler import MagnetHandler
from Sensor.GyroHandler import GyroHandler

class ThreadedSensor(AbstractServer):
    def __init__(self, addr_output):
        AbstractServer.__init__(self)

        shm_accel = shm()
        shm_gyro = shm()
        shm_magnet = shm()
        # self._accel_handler = AccelHandler(shm_accel)
        # self._gyro_handler = GyroHandler(shm_gyro)
        self._magnet_handler = MagnetHandler(shm_magnet)
        # self._emitter = Listener(addr_output,
        #     Emitter(shm_accel, shm_gyro, shm_magnet))

    def start(self):
        # self._accel_handler.start()
        # self._gyro_handler.start()
        self._magnet_handler.start()
        # self._emitter.start()
        AbstractServer.start(self)

    def _serve(self):
        pass

    def _free(self):
        pass
        # for s in [self._accel_handler, self._gyro_handler,
        #         self._magnet_handler, self._emitter]:
        #     s.stop()
        #     s.join(2)

if __name__ == '__main__':
    addr_out = '/tmp/togetic-sensor'
    f = ThreadedSensor(addr_out)
    try:
        f.start()
        while True:
            pass
    except KeyboardInterrupt:
        f.stop()
        f.join(2)
