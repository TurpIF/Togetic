#!/usr/bin/env python2

# datas
import socket
from Queue import Queue
import random

# maths and graph
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation



##############################   constants
nb_points = 100
t = [i for i in xrange(nb_points)]
l_names = ['accel_x', 'accel_y', 'accel_z', 'rot_x', 'rot_y', 'rot_z']


#############################    data management
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


def get_random_data():
    return [random.random()-0.5 for i in xrange(len(l_names))]



#queue = Queue()
#sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#sock.connect('/tmp/togetic_sortie_filtre')
#file_sock = sock.makefile('r', bufsize=0)


##############################   matplotlib stuff
# graphic creation
fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(-1, 1))

# init plots (create one line object for each data)
lines = []
for n in l_names:
    line, = ax.plot([], [], label=n)
    lines.append(line)

# legends, grid...
legend = ax.legend(loc='upper left', shadow=True)
plt.grid()
time_text = ax.text(0.5, 0.9, '', ha='center', va='center',
                    transform=ax.transAxes)


#############################    animation
# update and init fonction

def animate(i):
    data = get_random_data()
    time_text.set_text('time = {}'.format(i % 1000)) # :( doesn't work
    for l, d in zip(lines, data):
        tmp = l.get_ydata()  # get the previous values
        tmp.append(d)  # add the new data
        if len(tmp) >= len(t):
            tmp = tmp[1:]  # queue style (first we contruct the queue)
        l.set_data(t[:len(tmp)], tmp)  # update the plot data
    return lines + [time_text]


#Init only required for blitting to give a clean slate.
def init():
    # if we put data in the lines, they won't be cleared during the update
    for l in lines:
        l.set_data([], [])
    return lines

ani = animation.FuncAnimation(fig, animate, np.arange(1, 1000), init_func=init,
    interval=25, blit=True)
plt.show()


