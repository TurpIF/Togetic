import time
from Togetic.Server.AbstractServer import AbstractServer

class SerialHandler(AbstractServer):
    def __init__(self, request, transformation, shm_serial, shm):
        AbstractServer.__init__(self)
        self._request = request
        self._transformation = transformation
        self._shm_serial = shm_serial
        self._shm = shm

    def _free(self):
        pass

    def _serve(self):
        time.sleep(0.01)
        self._shm_serial.acquire()
        self._shm_serial.get(False).write(bytearray(self._request, 'ascii'))
        l = self._shm_serial.get(False).readline()
        self._shm_serial.release()
        try:
            mes = l.decode('ascii').split()
        except UnicodeDecodeError:
            pass
        else:
            if len(mes) == 3:
                try:
                    x, y, z = self._transformation(list(map(float, mes)))
                except ValueError:
                    pass
                else:
                    print(self, (x, y, z))
                    self._shm.data = (x, y, z)
