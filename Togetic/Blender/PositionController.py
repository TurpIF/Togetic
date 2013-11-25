import mathutils

from Togetic.shm import shm
from Togetic.Blender.Receiver import Receiver

class PositionController:
    def __init__(self, addr_input, owner):
        self._owner = controller.owner
        self._initPosition = self._owner.worldPosition.copy()
        self._shm = shm([0, 0, 0, 0, 0, 0])
        self._receiver = server(addr_input, shm)
        self._receiver.start()

    def __del__(self):
        if self._receiver is not None and self._receiver.isAlive():
            self._receiver.stop()
            self._receiver.join(2)

    def run(self):
        data = self._shm.data
        x, y, z, theta, phy, psy = data
        self._owner.worldPosition = self._initPosition \
                + mathutils.Vector((x, y, z))
