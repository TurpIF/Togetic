#!/usr/bin/env python3

import time
import argparse
import Togetic.Filter.ThreadedFilter

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, metavar='input', type=str,
            help='Filename of the socket to read in')
    parser.add_argument('--output', required=True, metavar='output', type=str,
            help='Filename of the socket to write in')
    parsed_args = parser.parse_args()
    addr_input = parsed_args.input
    addr_output = parsed_args.output

    # addr_input  = '/tmp/togetic-filter-in'
    # addr_output = '/tmp/togetic-filter-out'

    filter = Togetic.Filter.ThreadedFilter(addr_input, addr_output)
    try:
        filter.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        filter.stop()
        filter.join(2)
