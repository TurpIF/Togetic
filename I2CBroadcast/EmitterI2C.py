
import sys

sys.path += ['..']
from Server import Handler

def Emitter(shm):
    class _Emitter(Handler):
        def _msgToSend(self):
            data = shm.data
            data_str = 'TOGETIC ' + ' '.join(map(str, data))
            return bytes(data_str + '\n', 'UTF-8')

        def _parseRecv(self, data_raw):
            pass

        def _run(self):
            pass
    return _Emitter