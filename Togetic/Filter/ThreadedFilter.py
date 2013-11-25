import time
from Togetic.shm import shm

from Togetic.Server.AbstractServer import AbstractServer
from Togetic.Server.Listener import Listener

from Togetic.Filter.Receiver import Receiver
from Togetic.Filter.Emitter import Emitter
from Togetic.Filter.FilterHandler import FilterHandler

class ThreadedFilter(AbstractServer):
    def __init__(self, addr_input, addr_output):
        AbstractServer.__init__(self)

        shm_in = shm()
        shm_out = shm()
        self._receiver = Receiver(addr_input, shm_in)
        self._handler = FilterHandler(shm_in, shm_out)
        self._emitter = Listener(addr_output, Emitter(shm_out))

    def start(self):
        self._receiver.start()
        self._handler.start()
        self._emitter.start()
        AbstractServer.start(self)

    def _serve(self):
        time.sleep(0.5)

    def _free(self):
        for s in [self._receiver, self._handler, self._emitter]:
            print('Stopping ', s)
            s.stop()
            s.join(2)
            print(s, 'stopped')
