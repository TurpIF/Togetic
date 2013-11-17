#!/bin/env python3

from threading import Lock

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