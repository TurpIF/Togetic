#!/bin/env python2

import sys
sys.path += ['..']

import time
import serial
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
        print '1yoho'
        shm_serial = shm(serial.Serial('/dev/ttyACM0', 115200, timeout=0.1))
        print '2yoho'
        self._accel_handler = AccelHandler(shm_serial, shm_accel)
        print '3yoho'
        self._gyro_handler = GyroHandler(shm_serial, shm_gyro)
        print '4yoho'
        self._magnet_handler = MagnetHandler(shm_serial, shm_magnet)
        print '5yoho'
        self._emitter = Listener(addr_output,
            Emitter(shm_accel, shm_gyro, shm_magnet))
        print '6yoho'

    def start(self):
        self._accel_handler.start()
        self._gyro_handler.start()
        self._magnet_handler.start()
        self._emitter.start()
        AbstractServer.start(self)

    def _serve(self):
        time.sleep(0.2)

    def _free(self):
        pass
        for s in [self._accel_handler, self._gyro_handler,
                self._magnet_handler, self._emitter]:
            s.stop()
            s.join(2)

if __name__ == '__main__':
    addr_out = '/tmp/togetic-sensor'
    f = ThreadedSensor(addr_out)
    try:
        f.start()
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        f.stop()
        f.join(2)
