import time
from queue import Queue

from Togetic.Server.AbstractServer import AbstractServer
from Togetic.Server.Listener import Listener

from Togetic.Plot.Receiver import Receiver
from Togetic.Plot.PlotHandler import PlotHandler

class ThreadedPlot(AbstractServer):
    def __init__(self, addr_input):
        AbstractServer.__init__(self)

        queue_in = Queue()
        self._receiver = Receiver(addr_input, queue_in)
        self._handler = PlotHandler(queue_in)

    def start(self):
        self._receiver.start()
        self._handler.start()
        AbstractServer.start(self)

    def _serve(self):
        time.sleep(0.5)

    def _free(self):
        for s in [self._receiver, self._handler]:
            print('Stopping ', s)
            s.stop()
            s.join(2)
            print(s, 'stopped')
