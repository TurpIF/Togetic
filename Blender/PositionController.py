import threading
import mathutils
import socket
import os
import select
import bpy
import sys
sys.path += ['..']

from Server import ClientHandler

# Shared memory
relPosition = [0, 0, 0, 0, 0, 0]
lockPosition = threading.Lock()

# Sample trajectory to test the module
import math
class server(ClientHandler):
    def _parseRecv(self, data_raw):
        global lockPosition
        global relPosition

        data_line = data_raw.decode('utf-8').split('\n')
        for data in data_line:
            data_array = data.split(' ')
            # Read data parsed like 'POSITION X Y Z THETA PHI PSY' to test
            if len(data_array) == 7 and data_array[0] == 'TOGETIC':
                try:
                    # Get the position
                    x = float(data_array[1])
                    y = float(data_array[2])
                    z = float(data_array[3])
                    theta = float(data_array[4])
                    phi = float(data_array[5])
                    psy = float(data_array[6])
                except ValueError:
                    continue

                # Set the position
                lockPosition.acquire(True)
                relPosition[0] = x
                relPosition[1] = y
                relPosition[2] = z
                relPosition[3] = theta
                relPosition[4] = phi
                relPosition[5] = psy
                lockPosition.release()

    def _msgToSend(self):
        pass

    def _run(self):
        pass

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
        if self._server is not None and self._server.isAlive():
            self._server.stop()
            self._server.join(2)

    def run(self, controller):
        global lockPosition
        global relPosition

        owner = controller.owner

        lockPosition.acquire(True)
        x = relPosition[0]
        y = relPosition[1]
        z = relPosition[2]
        theta = relPosition[3]
        phi = relPosition[4]
        psy = relPosition[5]
        lockPosition.release()

        owner.worldPosition = self._initPosition + mathutils.Vector((x, y, z))

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
