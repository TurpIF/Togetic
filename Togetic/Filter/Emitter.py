from Togetic.Server import Handler
import time

def Emitter(shm):
    class _Emitter(Handler):
        def _msgToSend(self):
            data = shm.data
            if data is not None:
                print(time.time() - data[0])
                data_str = 'T ' + ' '.join(map(str, data))
                return data_str + '\n'

        def _parseRecv(self, data_raw):
            pass

        def _run(self):
            pass
    return _Emitter
