#!/bin/env python3

import sys
from threading import Lock

sys.path += ['..']
from Server.AbstractServer import AbstractServer
from Server.Listener import Listener

from Filter.Receiver import Receiver
from Filter.Emitter import Emitter
from Filter.FilterHandler import FilterHandler

class shm:
    def __init__(self):
        self._data = None
        self._lock = Lock()

    def set(self, data):
        with self._lock:
            self._data = data

    def get(self):
        with self._lock:
            return self._data

    data = property(get, set)

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
        pass

    def _free(self):
        for s in [self._receiver, self._handler, self._emitter]:
            s.stop()
            if s.isAlive():
                s.join(2)

if __name__ == '__main__':
    addr_in = '/tmp/togetic-input'
    addr_out = '/tmp/togetic-out'
    f = ThreadedFilter(addr_in, addr_out)
    try:
        f.start()
    except KeyboardInterrupt:
        f.stop()
        f.join(2)
        if f.isAlive():
            f.terminate()
