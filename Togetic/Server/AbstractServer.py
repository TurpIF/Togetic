import sys
import threading
import time

class AbstractServer(threading.Thread):
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
        This function doesn't terminate the thread. If there are blocking calls
        inside the main loop of the thread, this calls may not let the thread
        to finish.
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
                time.sleep(0.005)
            except Exception as e:
                # print('Server `', self, '` stopped by an exception :', e, file=sys.stderr)
                self.stop()
                raise
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


