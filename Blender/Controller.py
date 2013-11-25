import threading
import mathutils
import socket
import os
import select
import bpy

from Server import ClientHandler
from Togetic.Blender import PositionController

static_controller = None
def main(controller):
    global static_controller
    if static_controller is None:
        addr = bpy.context.scene.socket_address
        try:
            static_controller = Controller(addr, controller.owner)
        except (FileNotFoundError, ConnectionRefusedError):
            static_controller = None
    if static_controller is not None:
        static_controller.run()
