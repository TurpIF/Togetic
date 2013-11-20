import sys
sys.path += ['..']

import time
# import quick2wire.i2c as i2c

from Server.AbstractServer import AbstractServer

class GyroHandler(AbstractServer):
    def __init__(self, shm_serial, shm):
        AbstractServer.__init__(self)
        self._shm_serial = shm_serial
        self._shm = shm
        # self._bus = i2c.I2CMaster()

        # harware: SDO pin connected to the voltage supply (on peut le connecter a la masse => la slave address change)
        # self._addr = 0x69 # = 0b01101001
        # self._reg_data = 0x28

        # Il y'a une histoire avec un bit de start, a checker
        #self._reg_CRL_REG1 jouer la dessus pour eventuellement selectionner tel ou tel axe datasheet p29
        # En attendant de se mettre d'accord sur d'eventuels reglages, voila pour le mode bypass, le format des donnees est l'octet par defaut. 
        # self._reg_FIFO_CTRL_REG = 0b00000000

    # def start(self):
    #     with self._bus:
    #         self._bus.transaction(
    #             i2c.writing_bytes(self._addr, self._reg_FIFO_CTRL_REG, 0)
    #         )
    #     AbstractServer.start(self)

    def _free(self):
        pass

    def _serve(self):
        # with self._bus:
        #     xL, xH, yL, yH, zL, zH = self._bus.transaction(
        #             i2c.writing_bytes(self._addr, self._reg_data),
        #             i2c.reading(self._addr, 6))[0]
        # x = (xH << 8) | xL
        # y = (yH << 8) | yL
        # z = (zH << 8) | zL
        print 'salut'
        self._shm_serial.acquire()
        self._shm_serial.get(False).write('g')
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
