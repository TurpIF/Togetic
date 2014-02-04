import time
from Togetic.Server import Handler

def Emitter(shm_data): #shm_accel, shm_gyro, shm_magnet):
    class _Emitter(Handler):
        def _msgToSend(self):
            if shm_data.data is None:
                return

            data = list(shm_data.data)
            str_data = ' '.join(map(str, data))
            data_str = 'T ' + str_data
            return data_str + '\n'

        def _parseRecv(self, data_raw):
            pass

        def _run(self):
            pass
    return _Emitter
