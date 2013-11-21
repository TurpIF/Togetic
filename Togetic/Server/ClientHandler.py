import socket

from Togetic.Server.Handler import Handler

class ClientHandler(Handler):
    def __init__(self, addr):
        # Connect to the socket as a client
        self._addr = addr
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        Handler.__init__(self, (sock, addr))

    def start(self):
        try:
            self._socket.connect(self._addr)
        except (FileNotFoundError, ConnectionRefusedError):
            raise
        Handler.start(self)

