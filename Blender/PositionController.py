import threading
import mathutils
import socket
import os

# Shared memory
relPosition = mathutils.Vector((0, 1, 0))
lockPosition = threading.Lock()

# Sample trajectory to test the module
import math
def server():
    global lockPosition
    global relPosition

    # Connect to the socket as a client
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    addr = '/tmp/togetic-blender'

    def connect():
        # Try to connect
        while True:
            try:
                sock.connect(addr)
            except FileNotFoundError:
                continue
            except ConnectionRefusedError:
                continue
            break

    connect()

    while True:
        # Very ugly solution to detect when bge is stopped
        # TODO find an other way to do it (there is still some errors sometime)
        try:
            import bge
        except ImportError:
            break

        try:
            data_raw = sock.recv(1024)
        except socket.error:
            sock.close()
            connect()
            continue

        data_line = data_raw.decode('utf-8').split('\n')
        for data in data_line:
            data_array = data.split(' ')
            # Read data parsed like 'POSITION XXX YYY ZZZ' to test
            if len(data_array) == 4 and data_array[0] == 'POSITION':
                try:
                    # Get the position
                    x = float(data_array[1])
                    y = float(data_array[2])
                    z = float(data_array[3])
                except ValueError:
                    continue

                # Set the position
                lockPosition.acquire(True)
                relPosition[0] = x
                relPosition[1] = y
                relPosition[2] = z
                lockPosition.release()

    sock.close()

t = threading.Thread(target=server)
t.start()

class Controller:
    def __init__(self, controller):
        owner = controller.owner
        self._initPosition = owner.worldPosition.copy()

    def run(self, controller):
        global lockPosition
        global relPosition

        owner = controller.owner

        lockPosition.acquire(True)
        owner.worldPosition = self._initPosition + relPosition
        lockPosition.release()

static_controller = None
def main(controller):
    global static_controller
    if static_controller is None:
        static_controller = Controller(controller)

    static_controller.run(controller)
