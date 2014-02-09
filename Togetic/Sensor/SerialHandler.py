import time
from Togetic.Server.AbstractServer import AbstractServer


class SerialHandler(AbstractServer):
    def __init__(self, name, request, transformation, shm_serial, shm):
        AbstractServer.__init__(self)
        self._request = request
        self._transformation = transformation
        self._shm_serial = shm_serial
        self._shm = shm
        self._name = name
        self._calibrated = False
        self._gyr_avg = [0, 0, 0]
        self._acc_avg = [0, 0, 0]
        self._avg_size = 500
        self._avg_cur = 0

    def __str__(self):
        return self._name

    def _free(self):
        pass

    def _serve(self):
        time.sleep(0.01)
        t = time.time()
        self._shm_serial.acquire()
        self._shm_serial.get(False).write(bytearray(self._request, 'ascii'))
        l = self._shm_serial.get(False).readline()
        self._shm_serial.release()
        print('T', time.time() - t)
        print('B', l)
        try:
            mes = l.decode('ascii').split()
        except UnicodeDecodeError:
            pass
        else:
            if len(mes) == 9:
                if not self._calibrated:
                    try:
                        self._acc_avg[0] += float(mes[0])
                        self._acc_avg[1] += float(mes[1])
                        self._acc_avg[2] += float(mes[2])
                        self._gyr_avg[0] += float(mes[3])
                        self._gyr_avg[1] += float(mes[4])
                        self._gyr_avg[2] += float(mes[5])
                    except ValueError:
                        pass
                    else:
                        self._avg_cur += 1
                        if self._avg_cur >= self._avg_size:
                            self._calibrated = True
                            self._acc_avg[0] /= self._avg_size
                            self._acc_avg[1] /= self._avg_size
                            self._acc_avg[2] /= self._avg_size
                            self._gyr_avg[0] /= self._avg_size
                            self._gyr_avg[1] /= self._avg_size
                            self._gyr_avg[2] /= self._avg_size
                else:
                    try:
                        ax, ay, az, gx, gy, gz, cx, cy, cz = \
                                self._transformation(list(map(float, mes)),
                                                     self._acc_avg,
                                                     self._gyr_avg)
                        if abs(float(mes[3])) > 30000 or \
                                abs(float(mes[4])) > 30000 or \
                                abs(float(mes[5])) > 30000:
                            print('D gogolito', mes)
                    except ValueError:
                        print(mes, ' -> GTFO!!!')
                    else:
                        # print(self, (ax, ay, az), (gx, gy, gz), (cx, cy, cz))
                        print('A', (ax, ay, az))
                        print('G', (gx, gy, gz))
                        print('C', (cx, cy, cz))
                        self._shm.data = (t,
                                ax, ay, az,
                                gx, gy, gz,
                                cx, cy, cz)
