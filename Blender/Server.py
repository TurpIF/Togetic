import sys
import socket
import os
import threading
import select

class Server(threading.Thread):
    def __init__(self):
        """
        \brief Initialise the server.

        When this class is inherited, this __init__ have to be called.
        """
        threading.Thread.__init__(self)
        self._running = False

    def stop(self):
        """
        \brief Stop the run loop of the server

        Break the infinite loop of the run function to stop the thread.
        The thread have to be joined to be sure it's really stopped.
        """
        self._running = False

    def run(self):
        """
        \brief Running function of the thread

        Running function of the server called when the server is started (this
        start function from threading.Thread).
        It's an infinite loop calling each time the _serve function.
        When the loop is broken, this function call the _stop function in case
        there is something to free.
        If the _serve method throw an exception, the current thread stop. Other
        type of exception have to be managed in the _serve method.
        """
        self._running = True
        while self._running:
            try:
                self._serve()
            except Exception as e:
                print('Thread', self, 'stopped by an exception :', e, file=sys.stderr)
                self.stop()
        self._free()

    def _serve(self):
        """
        \brief  Function called each loop of the infinite run loop of the
                server.
        """
        raise Exception('Not implemented yet')

    def _free(self):
        """
        \brief  Function called when the run loop is broken. Let inherited
                class to release/free/close some ressources.
        """
        raise Exception('Not implemented yet')

class ClientServer(Server):
    def __init__(self, client):
        """
        \brief  Initialise the server and stock the socket and address of the
                client.
        """
        Server.__init__(self)
        self._socket = client[0]
        self._addr = client[1]

    def _free(self):
        """
        \brief Close the socket.
        """
        self._socket.close()

    def _serve(self):
        """
        \brief Select usable IOs and send/recv in consequence.
        """
        selection = select.select([self._socket], [self._socket], [], 0)
        if selection[0]:
            data = self._socket.recv(4096)
            self._parseRecv(data)
        if selection[1]:
            data = self._msgToSend()
            if data is not None:
                self._socket.send(data)
        self._run()

    def _parseRecv(self, data):
        """
        \brief Parse data input from the client.
        \param data Raw data sent by the client.

        When client send message, this function is called with
        the raw data in parameter.
        """
        raise Exception('Not implemented yet')

    def _msgToSend(self):
        """
        \brief Return the data to send to the client

        When the client can receive a message, this function is
        called to know what data has to be sent.
        """
        raise Exception('Not implemented yet')

    def _run(self):
        """
        \brief Execute some code without IOs

        On each loop, this function is called and have not to
        communicate with the client. It's better if this function
        is non-blocking.
        """
        raise Exception('Not implemented yet')

class ListenerServer(Server):
    def __init__(self, addr, clientServer):
        """
        \brief Initialise the server to listen connexion on a socket.

        \param addr         Address where the socket is created
        \param clientServer Class of the server used to communicate with new
                            clients. This class have to inherit from
                            ClientServer.

        The socket is on the UNIX domain using the TCP protocol.
        Try to bind this socket to the given address. If a file `addr` already
        exists, try to remove it before binding.
        Could throw OSError or socket.error exception.
        During the run of the listener, when a new client is connected, create
        a new instance of `clientServer` and start it immedialty.
        """
        Server.__init__(self)
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if os.path.exists(addr):
            try:
                os.remove(addr)
            except OSError:
                raise
        try:
            self._socket.bind(addr)
        except socket.error:
            self._socket.close()
            raise
        self._clients = []
        self._clientServer = clientServer

    def _serve(self):
        """
        \brief Wait for new clients and start a communication with.

        Listen entrant communication on the socket and accept everyone.
        Create an instance of the `clientServer` server to communicate with the
        client.
        """
        (readables, _, _) = select.select([self._socket], [], [], 0)
        if self._socket in readables:
            self._socket.listen(1)
            client = self._socket.accept()
            server = self._clientServer(client)
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
