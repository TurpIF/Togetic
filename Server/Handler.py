import select

from Server.AbstractServer import AbstractServer

class Handler(AbstractServer):
    def __init__(self, client):
        """
        \brief  Initialise the server and stock the socket and address of the
                client.
        """
        AbstractServer.__init__(self)
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
