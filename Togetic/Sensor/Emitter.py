from Togetic.Server import Handler

def Emitter(shm_accel, shm_gyro, shm_magnet):
    class _Emitter(Handler):
        def _msgToSend(self):
            data_accel = shm_accel.data
            data_gyro = shm_gyro.data
            data_magnet = shm_magnet.data
            #data_str = 'TOGETIC ' + ' '.join(map(str, data))
            # TODO
            data_str = ''
            return bytes(data_str + '\n', 'UTF-8')

        def _parseRecv(self, data_raw):
            pass

        def _run(self):
            pass
    return _Emitter
