#!/bin/env python3

from threading import Lock

class shm:
    def __init__(self, data=None):
        self._data = data
        self._lock = Lock()

    def set(self, data, lock=True):
        if lock:
            with self._lock:
                self._data = data
        else:
            self._data = data

    def get(self, lock=True):
        if lock:
            with self._lock:
                data = self._data
                return data
        else:
            return self._data

    def acquire(self):
        self._lock.acquire()

    def release(self):
        self._lock.release()

    data = property(get, set)
