import threading
import mathutils
import socket
import os
import select
from Server import Server
import bpy

# Shared memory
relPosition = mathutils.Vector((0, 1, 0))
lockPosition = threading.Lock()

# Sample trajectory to test the module
import math
class server(Server):
    def __init__(self, addr):
        Server.__init__(self)

        # Connect to the socket as a client
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            self._socket.connect(addr)
        except (FileNotFoundError, ConnectionRefusedError):
            raise

    def _serve(self):
        global lockPosition
        global relPosition

        (readables, _, _) = select.select([self._socket], [], [])
        if readables:
            data_raw = self._socket.recv(1024)
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

    def _free(self):
        self._socket.close()

class Controller:
    def __init__(self, controller):
        owner = controller.owner
        self._initPosition = owner.worldPosition.copy()
        addr = bpy.context.scene.socket_address
        self._server = None
        try:
            self._server = server(addr)
        except (FileNotFoundError, ConnectionRefusedError):
            raise
        self._server.start()

    def __del__(self):
        if self._server is not None:
            self._server.stop()
            self._server.join()

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
        try:
            static_controller = Controller(controller)
        except (FileNotFoundError, ConnectionRefusedError):
            static_controller = None
    if static_controller is not None:
        static_controller.run(controller)
