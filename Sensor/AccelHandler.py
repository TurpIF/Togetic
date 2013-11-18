import sys
sys.path += ['..']

from Server.AbstractServer import AbstractServer
import quick2wire.i2c as i2c

class AccelHandler(AbstractServer):
    def __init__(self, shm):
        AbstractServer.__init__(self)
        self._shm = shm
        self._bus = i2c.I2CMaster()
        self._addr = 0x1D
        self._reg_data = 0x32
        self._reg_data_format = 0x31
        self._reg_fifo_ctl = 0x38
        self._reg_int_enable = 0x2E
	
    def start(self):
        with self._bus:
            self._bus.transaction(
                i2c.writing_bytes(self._addr, self._reg_data_format, 0b01001100),
                i2c.writing_bytes(self._addr, self._reg_fifo_ctl, 0),
                i2c.writing_bytes(self._addr, self._reg_int_enable, 0)
            )
        AbstractServer.start(self)

    def _free(self):
        pass

    def _serve(self):
        with self._bus:
            x0, x1, y0, y1, z0, z1 = self._bus.transaction(
                i2c.writing_bytes(self._addr, self._reg_data),
                i2c.reading(self._addr, 6))[0]
            x = (x1 << 8) | x0
            y = (y1 << 8) | y0
            z = (z1 << 8) | z0
            self._shm.data = (x, y, z)
