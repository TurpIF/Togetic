from Togetic.Server.AbstractServer import AbstractServer

class FilterHandler(AbstractServer):
    def __init__(self, input_shm, output_shm):
        AbstractServer.__init__(self)
        self._in_shm = input_shm
        self._out_shm = output_shm

    def _serve(self):
        in_data = self._in_shm.data
        out_data = in_data
        self._out_shm.data = out_data

    def _free(self):
        pass
