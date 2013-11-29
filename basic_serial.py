#!/usr/bin/env python2

import serial
import json
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update_lines(num, data, lines):
    update_lines.counter += 1
    ser.write('a')
    l = ser.readline()
    print l
    x, y, z = map(float, l.split(' '))
    print(x, y, z)

    if update_lines.counter < npoints + 3:
        data[0, num] = num
        data[1, num] = x
        data[2, num] = y
        data[3, num] = z
        for i, l in enumerate(lines):
            l.set_xdata(data[0, :num])
            l.set_ydata(data[i + 1, :num])
    else:
        data[1:7, 0:(npoints - 1)] = data[1:7,1:npoints]
        data[1, npoints - 1] = x
        data[2, npoints - 1] = y
        data[3, npoints - 1] = z
        for i, l in enumerate(lines):
            l.set_xdata(data[0])
            l.set_ydata(data[i + 1])
    return lines

npoints = 100
period = 50
update_lines.counter = 0

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.write('r')
time.sleep(0.5)
for l in ser.readlines():
    pass

fig1 = plt.figure()
plt.hold(True)

data = np.zeros([4, npoints])

lines = plt.plot([], [], 'r-', [], [], 'g-', [], [], 'b-')
plt.legend(('Raw::X', 'Raw::Y', 'Raw::Z'), loc='upper left')
plt.xlim(0, npoints)
plt.ylim(-1024, 1024)
plt.xlabel('x')
plt.title('test')

line_ani = animation.FuncAnimation(fig1, update_lines, npoints,
        fargs=(data, lines), interval=period, blit=True)

plt.show()

# vim: set ts=4 sw=4:
