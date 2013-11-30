#!/usr/bin/env python2

def read():
    size = 200
    plot_data = [[0] * 10] * size
    with open('/tmp/togetic2') as f:
        for line in f:
            data_array = line.split(' ')
            if len(data_array) > 1 and data_array[0] == 'T':
                try:
                    ret = list(map(float, data_array[1:]))
                except ValueError:
                    pass
                else:
                    plot_data = plot_data[1:] + [ret]
                    print ret
                    yield plot_data

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()
line, = ax.plot(np.random.rand(200))
ax.set_ylim(-10, 10)

def update(data):
    # line.set_ydata(data)
    d = zip(*data)
    # print d
    for e in d:
        plt.plot(e)
    # plt.plot(data)
    return line,

def data_gen():
    while True: yield np.random.rand(200)

ani = animation.FuncAnimation(fig, update, read, interval=100)
plt.show()
