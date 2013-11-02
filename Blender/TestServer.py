#!/bin/env python3

import time
from Server import ClientServer
from Server import ListenerServer

def PositionServer(path):
    class _PositionServer(ClientServer):
        def __init__(self, client):
            ClientServer.__init__(self, client)
            self._time = 0
            self._dt = 0.01

        def _msgToSend(self):
            x, y, z = path(self._time)
            data = 'POSITION ' + str(x) + ' ' + str(y) + ' ' + str(z)
            return bytes(data + '\n', 'UTF-8')

        def _parseRecv(self, data):
            pass

        def _run(self):
            time.sleep(self._dt)
            self._time += self._dt

    return _PositionServer

def dummyPath(t):
    import math
    return (10 * math.cos(t), 10 * math.sin(t), 0)

if __name__ == '__main__':
    addr = '/tmp/togetic-blender'
    listener = ListenerServer(addr, PositionServer(dummyPath))
    try:
        listener.start()
        while True:
            pass
    except KeyboardInterrupt:
        listener.stop()
