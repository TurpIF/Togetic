from Togetic.Server import ClientHandler

class Receiver(ClientHandler):
    def __init__(self, addr, shm):
        ClientHandler.__init__(self, addr)
        self._shm = shm

    def _parseRecv(self, data_raw):
        data_line = data_raw.decode('ascii').split('\n')
        for data in data_line:
            data_array = data.split()
            if len(data_array) == 8 and data_array[0] == 'T':
                try:
                    pos = list(map(float, data_array[1:]))
                except ValueError:
                    pass
                else:
                    self._shm.data = pos

    def _msgToSend(self):
        pass

    def _run(self):
        pass
