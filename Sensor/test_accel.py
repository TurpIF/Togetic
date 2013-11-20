#!/bin/env python3

import sys
sys.path += ['..']

import time
from AccelHandler import AccelHandler
from shm import shm

if __name__ == '__main__':
    a = AccelHandler(shm())
    try:
        a.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        a.stop()
        a.join(2)
