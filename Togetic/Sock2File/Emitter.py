from queue import Empty
from Togetic.Server import ClientHandler

def Emitter(queue):
    class _Emitter(ClientHandler):
        def _msgToSend(self):
            if queue.empty():
                return
            try:
                data = queue.get(False)
            except Empty:
                return
            else:
                if data is not None:
                    data_str = 'T ' + ' '.join(map(str, data))
                    return data_str + '\n'

        def _parseRecv(self, data_raw):
            pass

        def _run(self):
            pass
    return _Emitter
