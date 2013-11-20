import sys
sys.path += ['..']

from Server.AbstractServer import AbstractServer

class GyroHandler(AbstractServer):
    def __init__(self, shm_serial, shm):
        AbstractServer.__init__(self)
        self._shm_serial = shm_serial
        self._shm = shm

    def _free(self):
        pass

    def _serve(self):
        self._shm_serial.acquire()
        self._shm_serial.get(False).write('r')
        l = self._shm_serial.get(False).readline()
        self._shm_serial.release()
        mes = l.split()
        print self, mes
        if len(mes) == 3:
            try:
                x, y, z = map(float, mes)
            except ValueError:
                pass
            else:
                self._shm.data = (x, y, z)
                # print x, y, z
