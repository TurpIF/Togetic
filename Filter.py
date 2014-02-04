#!/usr/bin/env python3

import time
import argparse
import Togetic.Filter.ThreadedFilter

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-serial', required=True, metavar='input_serial', type=str,
            help='Filename of the socket to read in')
    parser.add_argument('--input-kinect', required=True, metavar='input_kinect', type=str,
            help='Filename of the socket to read in')
    parser.add_argument('--output', required=True, metavar='output', type=str,
            help='Filename of the socket to write in')
    parsed_args = parser.parse_args()
    addr_input_serial = parsed_args.input_serial
    addr_input_kinect = parsed_args.input_kinect
    addr_output = parsed_args.output

    # addr_input  = '/tmp/togetic-filter-in'
    # addr_output = '/tmp/togetic-filter-out'

    filter = Togetic.Filter.ThreadedFilter(addr_input_serial,
            addr_input_kinect, addr_output)
    try:
        filter.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        filter.stop()
        filter.join(2)
