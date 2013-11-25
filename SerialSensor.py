#!/usr/bin/env python3
import time
import Togetic.Sensor.ThreadedSensor

if __name__ == '__main__':
    addr_input  = '/dev/ttyACM0'
    addr_output = '/tmp/togetic-sensor'

    sensor = Togetic.Sensor.ThreadedSensor(addr_input, addr_output)
    try:
        sensor.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        sensor.stop()
        sensor.join(2)
