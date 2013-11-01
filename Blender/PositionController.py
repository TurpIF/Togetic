import GameLogic
import Rasterizer
import threading
import time

# Shared memory
relPosition = [0, 1, 0]
lockPosition = threading.Lock()

initialized = False
initPosition = [0, 0, 0]

Sample trajectory to test the module
import math
time = 0
path = lambda t: (10 * math.cos(t), 10 * math.sin(t), 0)
def getPosition():
    time += 0.1
    pos = path(time)

    lockPosition.acquire(True)
    relPosition = pos
    lockPosition.release()

def server():
    while True:
        getPosition()
        time.sleep(0.1)

t = threading.Thread(target=server)
t.start()

def main():
    controller = GameLogic.getCurrentController()
    owner = controller.owner

    if not initialized:
        initPosition = owner.worldPosition
        initialized = True

    lockPosition.acquire(True)
    owner.worldPosition = map(
        lambda (abs, rel) : abs + rel,
        zip(initPosition, relPosition))
    lockPosition.release()
