#!/usr/bin/python2.7
import sys

import numpy
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Rectangle

data = map(lambda x: [float(e) for e in x.split('\n')[0].split(' ')],
           sys.stdin.readlines())
d = zip(*data)
x = numpy.array(d[0])
y = numpy.array(d[1])

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
l, = plt.plot(x, y, label='XY')

# range of the sliders
dil = 5
center = 10

if len(sys.argv) > 1 :
    square_x = 10.0
    currentAxis = plt.gca()
    currentAxis.add_patch(Rectangle((-square_x/2, -square_x/2), square_x, square_x, fill=None))

# pos x, pos y, largeur, hauteur
ax_dx = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_dy = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_cx = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_cy = plt.axes([0.25, 0.25, 0.65, 0.03])


s_dx = Slider(ax_dx, 'Dilatation x', -dil, dil, valinit=1.0)
s_dy = Slider(ax_dy, 'Dilatation y', -center, center, valinit=1.0)
s_cx = Slider(ax_cx, 'Centre y', -100.0, 100.0, valinit=0.0)
s_cy = Slider(ax_cy, 'Centre y', -100.0, 100.0, valinit=0.0)

def update(val):
    dx = s_dx.val
    cx = s_cx.val

    dy = s_dy.val
    cy = s_cy.val

    data_x = (x - cx)*dx
    data_y = (y - cy)*dy

#    print "origine (x, y) : ", cx, cy
#    print "dilatation (x, y, ratio x/y) : ", dx, dy, dx/dy
#    print ''
    l.set_xdata(data_x)
    l.set_ydata(data_y)
    fig.canvas.draw_idle()

s_dx.on_changed(update)
s_dy.on_changed(update)
s_cx.on_changed(update)
s_cy.on_changed(update)


plt.legend()
#plt.title("Title of Plot")
#plt.xlabel("X Axis Label")
#plt.ylabel("Y Axis Label")

plt.show()

print "origine (x, y) : ", s_cx.val, s_cy.val
print "dilatation (x, y, ratio x/y) : ", s_dx.val, s_dy.val, s_dx.val/s_dy.val
print ''
