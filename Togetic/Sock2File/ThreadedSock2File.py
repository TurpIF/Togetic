import time
from queue import Queue

from Togetic.Server.AbstractServer import AbstractServer
from Togetic.Server.Listener import Listener

from Togetic.Sock2File.Receiver import Receiver
from Togetic.Sock2File.Emitter import Emitter

class ThreadedSock2File(AbstractServer):
    def __init__(self, addr_input, addr_output):
        AbstractServer.__init__(self)

        queue_in = Queue()
        self._receiver = Receiver(addr_input, queue_in)
        self._emitter = Emitter(queue_in)(addr_output, True)

    def start(self):
        self._receiver.start()
        self._emitter.start()
        AbstractServer.start(self)

    def _serve(self):
        time.sleep(0.5)

    def _free(self):
        for s in [self._receiver, self._emitter]:
            print('Stopping ', s)
            s.stop()
            s.join(2)
            print(s, 'stopped')
