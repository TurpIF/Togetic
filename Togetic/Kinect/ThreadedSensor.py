import time
import sys

from Togetic.shm import shm

from Togetic.Server.AbstractServer import AbstractServer
from Togetic.Server.Listener import Listener

from Togetic.Kinect.Emitter import Emitter
from Togetic.Kinect.KinectHandler import KinectHandler


class ThreadedSensor(AbstractServer):
    def __init__(self, addr_output):
        AbstractServer.__init__(self)

        shm_data = shm()
        self._handler = KinectHandler(shm_data)
        self._emitter = Listener(addr_output,
            Emitter(shm_data))

    def start(self):
        time.sleep(5)  # Wait for the serial to be ready
        for s in [
                self._handler,
                self._emitter]:
            s.start()
        AbstractServer.start(self)

    def _serve(self):
        time.sleep(0.5)

    def _free(self):
        for s in [
                self._handler,
                self._emitter]:
            print('Stopping ', s)
            s.stop()
            s.join(2)
            print(s, 'stopped')

if __name__ == '__main__':
    addr_input = '/dev/ttyACM1'
    addr_output = '/tmp/togetic-kinect'
    f = ThreadedSensor(addr_input, addr_output)
    try:
        f.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        f.stop()
        f.join(2)
        sys.exit()
