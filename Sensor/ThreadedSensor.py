#!/bin/env python3

import sys
sys.path += ['..']

import time
import serial
from shm import shm

from Server.AbstractServer import AbstractServer
from Server.Listener import Listener

from Sensor.Emitter import Emitter
from Sensor.SerialHandler import SerialHandler

class ThreadedSensor(AbstractServer):
    def __init__(self, addr_input, addr_output):
        AbstractServer.__init__(self)

        shm_accel = shm()
        shm_gyro = shm()
        shm_compass = shm()
        shm_serial = shm(serial.Serial(addr_input, 115200, timeout=0.01))
        self._accel_handler = SerialHandler('a', shm_serial, shm_accel)
        self._gyro_handler = SerialHandler('r', shm_serial, shm_gyro)
        self._compass_handler = SerialHandler('c', shm_serial, shm_compass)
        self._emitter = Listener(addr_output,
            Emitter(shm_accel, shm_gyro, shm_compass))

    def start(self):
        for s in [self._accel_handler, self._gyro_handler,
                self._compass_handler, self._emitter]:
            s.start()
        AbstractServer.start(self)

    def _serve(self):
        time.sleep(0.5)

    def _free(self):
        for s in [self._accel_handler, self._gyro_handler,
                self._compass_handler, self._emitter]:
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
