import socket

from Togetic.Server.Handler import Handler


class ClientHandler(Handler):
    def __init__(self, addr, file=False):
        # Connect to the socket as a client
        self._addr = addr
        self._using_file = file

        if not file:
            self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            file_stream = self._socket.makefile('rwb', buffering=0)
        else:
            self._socket = None
            file_stream = open(addr, 'wb+', buffering=0)
        Handler.__init__(self, (file_stream, addr))

    def start(self):
        if self._socket is not None:
            try:
                self._socket.connect(self._addr)
            except (FileNotFoundError, ConnectionRefusedError):
                raise
        Handler.start(self)

    def stop(self):
        if self._socket is not None:
            self._socket.close()
        Handler.stop(self)
