import sys
sys.path += ['..']

from Server.AbstractServer import AbstractServer

class MagnetHandler(AbstractServer):
    def __init__(self, shm):
        AbstractServer.__init__(self)
		self._shm = shm

    def _free(self):
        pass

    def _serve(self):
        pass