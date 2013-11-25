#!/usr/bin/env python3
import time
import Togetic.Filter.ThreadedFilter

if __name__ == '__main__':
    addr_input  = '/tmp/togetic-filter-in'
    addr_output = '/tmp/togetic-filter-out'
    filter = Togetic.Filter.ThreadedFilter(addr_input, addr_output)
    try:
        filter.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        filter.stop()
        filter.join(2)
