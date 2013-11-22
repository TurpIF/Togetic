import socket
import os
import select

from Togetic.Server.AbstractServer import AbstractServer

class Listener(AbstractServer):
    def __init__(self, addr, handler):
# TODO let chose the protocol and the type of the socket to use
# TODO let chose the address more efficiently (filename of a socket or IP+PORT)
# TODO Do some test on the arguments used
        """
        \brief Initialise the server to listen connexion on a socket.

        \param addr     Address where the socket is created
        \param handler  Class inherited by Handler class used to communicate
                        with new clients.

        The socket is on the UNIX domain using the TCP protocol.
        Try to bind this socket to the given address. If a file `addr` already
        exists, try to remove it before binding.
        Could throw OSError or socket.error exception.
        During the run of the listener, when a new client is connected, create
        a new instance of `clientServer` and start it immedialty.
        """
        AbstractServer.__init__(self)
        self._addr = addr
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._clients = []
        self._handler = handler

    def start(self):
        if os.path.exists(self._addr):
            try:
                os.remove(self._addr)
            except OSError:
                raise
        try:
            self._socket.bind(self._addr)
            self._socket.listen(5)
        except socket.error:
            self._socket.close()
            raise
        except OSError:
            self._socket.close()
            raise
        AbstractServer.start(self)

    def _serve(self):
        """
        \brief Wait for new clients and start a communication with.

        Listen entrant communication on the socket and accept everyone.
        Create an instance of the `clientServer` server to communicate with the
        client.
        """
        (readables, _, _) = select.select([self._socket], [], [], 0)
        if self._socket in readables:
            client = self._socket.accept()
            server = self._handler(client)
            server.start()
            self._clients += [server]

    def _free(self):
        """
        \brief Free all allocated ressources.

        Stop and join all created servers and close the listener socket.
        """
        for client in self._clients:
            client.stop()
            client.join(2)
        self._socket.close()

