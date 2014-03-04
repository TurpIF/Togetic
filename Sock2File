#!/usr/bin/env python3

import time
import argparse
import Togetic.Sock2File.ThreadedSock2File

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, metavar='input', type=str,
            help='Filename of the socket to read in')
    parser.add_argument('--output', required=True, metavar='output', type=str,
            help='Filename of the file to write in')
    parsed_args = parser.parse_args()
    addr_input = parsed_args.input
    addr_output = parsed_args.output

    th = Togetic.Sock2File.ThreadedSock2File(addr_input, addr_output)
    try:
        th.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        th.stop()
        th.join(2)
