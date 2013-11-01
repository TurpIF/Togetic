import GameLogic
import Rasterizer
import threading
import mathutils
import time

# Shared memory
relPosition = mathutils.Vector((0, 1, 0))
lockPosition = threading.Lock()

initialized = False
initPosition = mathutils.Vector((0, 0, 0))

# Sample trajectory to test the module
import math
def setPosition(time):
    global lockPosition
    global relPosition

    path = lambda t: mathutils.Vector((10 * math.cos(t), 10 * math.sin(t), 0))
    pos = path(time)

    lockPosition.acquire(True)
    relPosition = pos
    lockPosition.release()

def server():
    t = 0
    while True:
        setPosition(t)
        time.sleep(0.01)
        t += 0.01

t = threading.Thread(target=server)
t.start()

def main():
    global lockPosition
    global relPosition
    global initialized
    global initPosition

    controller = GameLogic.getCurrentController()
    owner = controller.owner

    if not initialized:
        initPosition = owner.worldPosition.copy()
        initialized = True

    lockPosition.acquire(True)
    owner.worldPosition = initPosition + relPosition
    lockPosition.release()
