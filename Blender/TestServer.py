#!/bin/env python2.7

import sys
import socket
import os
import time
import threading

# Dummy path to send
def path(t):
    import math
    return (10 * math.cos(t), 10 * math.sin(t), 0)

class PositionServer(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)

        self._socket = socket
        self._time = 0
        self._dt = 0.01
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            x, y, z = path(self._time)
            data = 'POSITION ' + str(x) + ' ' + str(y) + ' ' + str(z)
            try:
                self._socket.send(data + '\n')
            except socket.error:
                print 'An error occur with a client'
                self.stop()

            time.sleep(self._dt)
            self._time += self._dt

        self._socket.close()

    def stop(self):
        self._running = False


if __name__ == '__main__':
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    addr = '/tmp/togetic-blender'

    if os.path.exists(addr):
        try:
            os.remove(addr)
        except OSError:
            print 'A file `' + addr + '` already exists. Shutdown'
            sys.exit(0)

    sock.bind(addr)
    lsServer = []

    try:
        while True:
            sock.listen(1)
            conn, addr = sock.accept()
            print 'New client'
            server = PositionServer(conn)
            server.start()
            lsServer += [server]
    except KeyboardInterrupt:
        for server in lsServer:
            server.stop()
            server.join(5)

    sock.close()
