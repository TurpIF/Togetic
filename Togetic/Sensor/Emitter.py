import time
from Togetic.Server import Handler

def Emitter(shm_data): #shm_accel, shm_gyro, shm_magnet):
    class _Emitter(Handler):
        def _msgToSend(self):
            if shm_data.data is None:
                return
            # if shm_accel.data is None:
            #     return
            # if shm_gyro.data is None:
            #     return
            # if shm_magnet.data is None:
            #     return

            data = list(shm_data.data)
            # data_accel = list(shm_accel.data)
            # data_gyro = list(shm_gyro.data)
            # data_magnet = list(shm_magnet.data)
            data = [time.time()] + data # data_accel + data_gyro + data_magnet
            str_data = ' '.join(map(str, data))
            data_str = 'T ' + str_data
            return data_str + '\n'

        def _parseRecv(self, data_raw):
            pass

        def _run(self):
            pass
    return _Emitter
