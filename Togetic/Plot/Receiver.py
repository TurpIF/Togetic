from Togetic.Server import ClientHandler

class Receiver(ClientHandler):
    def __init__(self, addr, queue):
        ClientHandler.__init__(self, addr)
        self._queue = queue

    def _msgToSend(self):
        pass

    def _parseRecv(self, data_raw):
        data_line = data_raw.decode('ascii').split('\n')
        for data in data_line:
            data_array = data.split(' ')
            if len(data_array) == 8 and data_array[0] == 'T':
                try:
                    info = map(float, data_array[1:])
                except ValueError:
                    return
                else:
                    self._queue.put(list(info))

    def _run(self):
        pass
