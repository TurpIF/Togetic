import sys
sys.path += ['..']

# import quick2wire.i2c as i2c
import time

from Server.AbstractServer import AbstractServer

class MagnetHandler(AbstractServer):
    def __init__(self, shm_serial, shm):
        AbstractServer.__init__(self)
        self._shm_serial = shm_serial
        self._shm = shm
        # self._addr = 0x1e
        # self._reg_data = 0x03
        # self._reg_ctl_a = 0x00
        # self._reg_ctl_b = 0x01
        # self._reg_mode = 0x02

    # def start(self):
    #     with i2c.I2CMaster() as bus:
    #         bus.transaction(
    #             i2c.writing_bytes(self._addr, self._reg_ctl_a, 0x18),
    #             i2c.writing_bytes(self._addr, self._reg_ctl_b, 0x00),
    #             i2c.writing_bytes(self._addr, self._reg_mode, 0x01)
    #         )
    #     AbstractServer.start(self)

    def _free(self):
        pass

    def _serve(self):
        # try:
        #     with i2c.I2CMaster() as bus:
        #         bus.transaction(
        #                 i2c.writing_bytes(self._addr, self._reg_mode, 0x01))
        #         x1, x0, y1, y0, z1, z0 = bus.transaction(
        #                 i2c.writing_bytes(self._addr, self._reg_data),
        #                 i2c.reading(self._addr, 6))[0]
        # except OSError: # Read error
        #     return
        # x = (x1 << 8) | x0
        # y = (y1 << 8) | y0
        # z = (z1 << 8) | z0
        # time.sleep(0.02)
        # self._shm.data = (x, y, z)
        print 'heho'
        self._shm_serial.acquire()
        self._shm_serial.get(False).write('m')
        l = self._shm_serial.get(False).readline()
        self._shm_serial.release()
        mes = l.split(' ')
        if len(mes) == 3:
            try:
                x, y, z = map(float, mes)
            except ValueError:
                pass
            else:
                self._shm.data = (x, y, z)
        time.sleep(0.02)
