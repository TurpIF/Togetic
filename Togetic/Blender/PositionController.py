import mathutils

from Togetic.shm import shm
from Togetic.Blender.Receiver import Receiver

class PositionController:
    def __init__(self, addr_input, owner):
        self._owner = owner
        self._initPosition = self._owner.worldPosition.copy()
        self._shm = shm([0, 0, 0, 0, 0, 0])
        self._receiver = Receiver(addr_input, shm)
        self._receiver.start()

    def __del__(self):
        if self._receiver is not None and self._receiver.isAlive():
            self._receiver.stop()
            self._receiver.join(2)

    def run(self):
        data = self._shm.data
        if data is not None and len(data) == 7:
            _, x, y, z, theta, phy, psy = data
            # self._owner.worldPosition = self._initPosition \
            #         + mathutils.Vector((x, y, z))
            ori = self._owner.orientation.to_euler()
            ori.x = theta
            ori.y = 0
            ori.z = psy
            self._owner.orientation = ori
            print(x, y, z, ori.x, ori.y, ori.z)
