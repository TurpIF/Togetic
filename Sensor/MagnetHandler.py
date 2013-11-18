import sys
sys.path += ['..']

from Server.AbstractServer import AbstractServer
import quick2wire.i2c as i2c

class MagnetHandler(AbstractServer):
    def __init__(self, shm):
        AbstractServer.__init__(self)
		self._shm = shm
		self._bus = i2c.I2CMaster()
		self._addr = 0x3D
		self._reg_data = 0x03
		self._regA = 0x00
		
	
	def start(self):
	    with self._bus:
			self._bus.transaction(
			i2c.writing_bytes(self._addr, self._regA, 0b01010000)
			#high speed i2c auto
		# il y a des data output registers. Vu qu'on fonctionne en bypass pour commencer, osef nan?
		# les settings par défaut m'ont l'air les mieux... On verra!
			)
		AbstractServer.start(self)

    def _free(self):
        pass

    def _serve(self):
		with self._bus:
			x1, x0, y1, y0, z1, z0= self._bus.transaction(
				i2c.writing_bytes(self._addr, self._reg_data),
				i2c.reading(self._addr, 6))[0]
		x = (x1 << 8) | x0
		y = (y1 << 8) | y0
		z = (z1 << 8) | z0
		self._shm.data = (x, y, z)