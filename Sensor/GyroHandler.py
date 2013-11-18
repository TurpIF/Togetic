import sys
sys.path += ['..']

from Server.AbstractServer import AbstractServer
import quick2wire.i2c as i2c

class GyroHandler(AbstractServer):
    def __init__(self, shm):
        AbstractServer.__init__(self)
        self._shm = shm
        self._bus = i2c.I2CMaster()

        # harware: SDO pin connected to the voltage supply (on peut le connecter � la masse => la slave address change)
        self._addr = 0x69 # = 0b01101001
        self._reg_data = 0x28

        # Il y'a une histoire avec un bit de start, � checker
        #self._reg_CRL_REG1 jouer l� dessus pour �ventuellement s�lectionner tel ou tel axe datasheet p29
        # En attendant de se mettre d'accord sur d'�ventuels r�glages, voil� pour le mode bypass, le format des donn�es est l'octet par d�faut. 
        self._reg_FIFO_CTRL_REG = 0b00000000

    def start(self):
        with self._bus:
            self._bus.transaction(
                i2c.writing_bytes(self._addr, self._reg_FIFO_CTRL_REG, 0)
            )
        AbstractServer.start(self)

    def _free(self):
        pass

    def _serve(self):
        with self._bus:
            xL, xH, yL, yH, zL, zH = self._bus.transaction(
                    i2c.writing_bytes(self._addr, self._reg_data),
                    i2c.reading(self._addr, 6))[0]
        x = (xH << 8) | xL
        y = (yH << 8) | yL
        z = (zH << 8) | zL
        self._shm.data = (x, y, z)
