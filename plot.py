#!/usr/bin/env python2

import json
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect('./test')
file_sock = sock.makefile('r', bufsize=0)

def get_data():
    # return [update_lines.counter, 20 * math.cos(update_lines.counter), 0, 0, 0]
    # line = raw_input().split(' ')
    line = file_sock.readline().strip().split(' ')
    print line
    if len(line) == nbr_data + 1 and line[0] == 'T':
        try:
            f = list(map(float, line[1:]))
        except ValueError:
            pass
        else:
            f[0] = update_lines.counter
            return f
    return [0] * nbr_data

def update_lines(num, data, lines):
    update_lines.counter += 1

    ls_data = get_data()

    if update_lines.counter < npoints + 3:
        for i in xrange(nbr_data):
            data[i, num] = ls_data[i]
        for i, l in enumerate(lines):
            l.set_xdata(data[0, :num])
            l.set_ydata(data[i + 1, :num])
    else:
        data[1:, 0:(npoints - 1)] = data[1:, 1:npoints]
        for i in xrange(1, nbr_data):
            data[i, npoints - 1] = ls_data[i]
        for i, l in enumerate(lines):
            l.set_xdata(data[0])
            l.set_ydata(data[i + 1])
    return lines

npoints = 100
period = 50
update_lines.counter = 0
nbr_data = 10

fig1 = plt.figure()
plt.hold(True)

data = np.zeros([nbr_data, npoints])

colors = ['r', 'g', 'b']
strokes = ['-', '--', '.', '-.']
col_strokes = [c + s for s in strokes for c in colors]
lines = plt.plot(*sum([[[], [], cs] for cs in col_strokes[:nbr_data - 1]], []))
# lines = plt.plot()
plt.legend(tuple(['data ' + str(i) for i in xrange(1, nbr_data)]), loc='upper left')
plt.xlim(0, npoints)
plt.ylim(-11, 11)
plt.xlabel('x')
plt.title('test')

line_ani = animation.FuncAnimation(fig1, update_lines, npoints,
        fargs=(data, lines), interval=period, blit=True)

plt.show()

# vim: set ts=4 sw=4:
