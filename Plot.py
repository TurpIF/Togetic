#!/usr/bin/env python3
import time
import Togetic.Plot.ThreadedPlot

if __name__ == '__main__':
    addr_input = '/tmp/togetic-plot'
    plot = Togetic.Plot.ThreadedPlot(addr_input)
    try:
        plot.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        plot.stop()
        plot.join(2)
