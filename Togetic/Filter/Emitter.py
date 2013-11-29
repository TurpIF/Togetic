from Togetic.Server import Handler

def Emitter(shm):
    class _Emitter(Handler):
        def _msgToSend(self):
            data = shm.data
            if data is not None:
                data_str = 'T ' + ' '.join(map(str, data))
                return bytes(data_str + '\n', 'ascii')

        def _parseRecv(self, data_raw):
            pass

        def _run(self):
            pass
    return _Emitter
