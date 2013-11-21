#!/bin/env python3

import sys
import time
import argparse
# from Filter.ThreadedFilter import ThreadedFilter
import Filter.ThreadedFilter

if __name__ == '__main__':
    addr_in = '/tmp/togetic-input'
    addr_out = '/tmp/togetic-out'
    f = ThreadedFilter(addr_in, addr_out)
    try:
        f.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        f.stop()
        f.join(2)
        sys.exit()
