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
l_names_subplot_1 = ['accel_x', 'accel_y', 'accel_z']
l_names_subplot_2 = ['rot_x', 'rot_y', 'rot_z']
nb_var = len(l_names_subplot_1) + len(l_names_subplot_2)

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
    return [random.random()-0.5 for i in xrange(nb_var)]



#queue = Queue()
#sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#sock.connect('/tmp/togetic_sortie_filtre')
#file_sock = sock.makefile('r', bufsize=0)


##############################   matplotlib stuff
# graphic creation
fig, (ax1, ax2) = plt.subplots(2, sharex=True)  #xlim=(0, 100), ylim=(-1, 1))

# axes limits
ax1.set_xlim((0, 100))
ax1.set_ylim((-1, 1))
ax2.set_xlim((0, 100))
ax2.set_ylim((-1, 1))

# init plots (create one line object for each data)
lines = []
for n in l_names_subplot_1:
    line, = ax1.plot([], [], label=n)
    lines.append(line)
for n in l_names_subplot_2:
    line, = ax2.plot([], [], label=n)
    lines.append(line)

# legends, grid...
legend1 = ax1.legend(loc='upper left', shadow=True)
legend2 = ax2.legend(loc='upper left', shadow=True)
ax1.grid()
ax2.grid()
time_text = ax1.text(0.5, 0.9, '', ha='center', va='center',
                    transform=ax1.transAxes)


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

    # suz hack lolz (we need a single list of objects)
    return lines + [time_text]


#Init only required for blitting to give a clean slate.
def init():
    time_text.set_text("")
    # if we put data in the lines, they won't be cleared during the update
    for l in lines:
        l.set_data([], [])
    return lines + [time_text]

ani = animation.FuncAnimation(fig, animate, np.arange(1, 1000), init_func=init,
    interval=25, blit=True)
plt.show()

