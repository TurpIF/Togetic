#!/usr/bin/env python3

import sys
import os
sys.path += [os.path.dirname(__file__)]

import time
import argparse
import Togetic.Kinect.ThreadedSensor

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, metavar='output', type=str,
            help='Filename of the socket to write in')
    parsed_args = parser.parse_args()
    addr_output = parsed_args.output

    kinect = Togetic.Kinect.ThreadedSensor(addr_output)
    try:
        kinect.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        kinect.stop()
        kinect.join(2)
