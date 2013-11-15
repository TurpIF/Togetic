import socket

from Server.Handler import Handler

class ClientHandler(Handler):
    def __init__(self, addr):
        # Connect to the socket as a client
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.connect(addr)
        except (FileNotFoundError, ConnectionRefusedError):
            raise
        Handler.__init__(self, (sock, addr))

