from Togetic.Server import ClientHandler


def Receiver(data_len):
    class _Receiver(ClientHandler):
        def __init__(self, addr, shm):
            ClientHandler.__init__(self, addr)
            self._shm = shm

        def _msgToSend(self):
            pass

        def _parseRecv(self, data_raw):
            data_line = data_raw.split('\n')
            for data in data_line:
                data_array = data.split(' ')
                if data_len == 5:
                    print(data_array)
                if len(data_array) == data_len and data_array[0] == 'T':
                    try:
                        info = list(map(float, data_array[1:]))
                    except ValueError:
                        return
                    else:
                        self._shm.data = info

        def _run(self):
            pass
    return _Receiver

ReceiverKinect = Receiver(5)
ReceiverSerial = Receiver(11)
