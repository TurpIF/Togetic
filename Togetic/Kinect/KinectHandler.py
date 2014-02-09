import time
import sys
from Togetic.Server.AbstractServer import AbstractServer


class KinectHandler(AbstractServer):
    def __init__(self, shm):
        AbstractServer.__init__(self)
        self._shm = shm

    def _free(self):
        pass

    def _serve(self):
        line = sys.stdin.readline().split()
        if len(line) == 4 and line[0] == 'POS':
            try:
                x = float(line[1])
                y = float(line[2])
                z = float(line[3])
            except ValueError:
                pass
            else:
                t = time.time()
                self._shm.data = t, x, y, z
                print('P', self._shm.get())
        # time.sleep(0.01)
