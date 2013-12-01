#!/usr/bin/env python2

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import socket
from Queue import Queue
import threading

queue = Queue()

def read_data(file_in, queue, nbr_data):
    while True:
        line = file_in.readline().strip().split(' ')
        if len(line) == nbr_data + 1 and line[0] == 'T':
            try:
                f = list(map(float, line[1:]))
            except ValueError:
                pass
            else:
                queue.put(f)

def linear_interpolation(x0, y0, x1, y1):
    if x1 == x0:
        return []
    return [(y1 - y0) * (x - x0) / (x1 - x0) + y0
            for x in xrange(int(x0), int(x1))]

def x2time(x):
    return x * 1000

def update_plot(num, data, lines):
    d = queue.get()
    t = x2time(d[0])

    if not hasattr(update_plot, 'old_time'):
        update_plot.old_time = t
    old_t = update_plot.old_time

    if t - old_t < 1:
        return lines
    for i, y in enumerate(d[1:]):
        data[i + 1, :-1] = data[i + 1, 1:]
        data[i + 1, -1] = y

    data[0] = np.linspace(0, 100, 100)
    for i, l in enumerate(lines):
        l.set_data(data[0], data[i + 1])

    update_plot.old_time = t
    return lines

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect('./test')
file_sock = sock.makefile('r', bufsize=0)

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
period = 20
update_lines.counter = 0
nbr_data = 7

thread = threading.Thread(target=read_data, args=(file_sock, queue, nbr_data))
thread.start()

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

line_ani = animation.FuncAnimation(fig1, update_plot, npoints,
        fargs=(data, lines), interval=period, blit=True)

plt.show()

# vim: set ts=4 sw=4:
