import time
from Togetic.shm import shm

from Togetic.Server.AbstractServer import AbstractServer
from Togetic.Server.Listener import Listener

from Togetic.Filter.Receiver import ReceiverSerial
from Togetic.Filter.Receiver import ReceiverKinect
from Togetic.Filter.Emitter import Emitter
from Togetic.Filter.FilterHandler import FilterHandler


class ThreadedFilter(AbstractServer):
    def __init__(self, addr_input_serial, addr_input_kinect, addr_output):
        AbstractServer.__init__(self)

        shm_serial = shm()
        shm_kinect = shm()
        shm_out = shm()
        self._receiver_serial = ReceiverSerial(addr_input_serial, shm_serial)
        self._receiver_kinect = ReceiverKinect(addr_input_kinect, shm_kinect)
        self._handler = FilterHandler(shm_serial, shm_kinect, shm_out)
        self._emitter = Listener(addr_output, Emitter(shm_out))

    def start(self):
        self._receiver_serial.start()
        self._receiver_kinect.start()
        self._handler.start()
        self._emitter.start()
        AbstractServer.start(self)

    def _serve(self):
        time.sleep(0.5)

    def _free(self):
        for s in [
                self._receiver_serial,
                self._receiver_kinect,
                self._handler,
                self._emitter]:
            print('Stopping ', s)
            s.stop()
            s.join(2)
            print(s, 'stopped')
