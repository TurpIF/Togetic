import sys
sys.path += ['..']

import time
import quick2wire.i2c as i2c

from Server.AbstractServer import AbstractServer

class AccelHandler(AbstractServer):
    def __init__(self, shm):
        AbstractServer.__init__(self)
        self._shm = shm
        self._addr = 0x53
        self._reg_data = 0x32
        self._reg_power_ctl = 0x2d
        self._reg_data_format = 0x31
        self._reg_fifo_ctl = 0x38
        self._reg_int_enable = 0x2e

    def start(self):
        with i2c.I2CMaster() as bus:
            bus.transaction(
                i2c.writing_bytes(self._addr, self._reg_power_ctl, 0x0))
            bus.transaction(
                i2c.writing_bytes(self._addr, self._reg_power_ctl, 0x10))
            bus.transaction(
                i2c.writing_bytes(self._addr, self._reg_power_ctl, 0x08))
            # bus.transaction(
            #     i2c.writing_bytes(self._addr, self._reg_data_format, 0x0C),
            #     i2c.writing_bytes(self._addr, self._reg_fifo_ctl, 0x00),
            #     i2c.writing_bytes(self._addr, self._reg_int_enable, 0x00)
            # )
        AbstractServer.start(self)

    def _free(self):
        pass

    def _serve(self):
        try:
            with i2c.I2CMaster() as bus:
                x0, x1, y0, y1, z0, z1 = bus.transaction(
                    i2c.writing_bytes(self._addr, self._reg_data),
                    i2c.reading(self._addr, 6))[0]
        except OSError:
            return
        x = (x1 << 8) | x0
        y = (y1 << 8) | y0
        z = (z1 << 8) | z0
        print(x0, x1, y0, y1, z0, z1)
        time.sleep(0.02)
        # self._shm.data = (x, y, z)
