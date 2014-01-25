#!/usr/bin/env python3

import time
import argparse

from Togetic.Server import Handler
from Togetic.Server import Listener

def PositionServer(path):
    class _PositionServer(Handler):
        def __init__(self, client):
            Handler.__init__(self, client)
            self._time = 0
            self._dt = 0.01

        def _msgToSend(self):
            data_int = path(self._time)
            data = 'T ' + ' '.join(map(str, data_int))
            print(data)
            return data + '\n'

        def _parseRecv(self, data):
            pass

        def _run(self):
            time.sleep(self._dt)
            self._time += self._dt

    return _PositionServer

def dummyPath(t):
    import math
    return (time.time(), 0 * -10 * math.cos(t), 0 * -10 * math.sin(t), 0, 0 * math.sin(t), (int(time.time()) % 10) / 10 * 2 * math.pi, 0 * (math.cos(t) + math.sin(t)) / 2.0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, metavar='output', type=str,
            help='Filename of the socket to write in')
    parsed_args = parser.parse_args()
    addr = parsed_args.output

    listener = Listener(addr, PositionServer(dummyPath))
    try:
        listener.start()
        while True:
            pass
    except KeyboardInterrupt:
        listener.stop()
