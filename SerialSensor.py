#!/usr/bin/env python3

import time
import argparse
import Togetic.Sensor.ThreadedSensor

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, metavar='input', type=str,
            help='Filename of the device to read in')
    parser.add_argument('--output', required=True, metavar='output', type=str,
            help='Filename of the socket to write in')
    parsed_args = parser.parse_args()
    addr_input = parsed_args.input
    addr_output = parsed_args.output

    # addr_input  = '/dev/ttyACM0'
    # addr_output = '/tmp/togetic-sensor'
    sensor = Togetic.Sensor.ThreadedSensor(addr_input, addr_output)
    try:
        sensor.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        sensor.stop()
        sensor.join(2)
