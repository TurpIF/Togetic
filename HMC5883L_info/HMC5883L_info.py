import serial
import json
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update_lines(num, data, lines, texts):
	update_lines.counter += 1
	ser.write('r')
	time.sleep(.02)
	l = ser.readline()
	d = json.loads(l)
#	print(d['raw'])
#	print(num)
	if update_lines.counter > 3:
		texts[0].set_text('Raw::X = ' + str(d['raw']['x']))
		texts[1].set_text('Raw::Y = ' + str(d['raw']['y']))
		texts[2].set_text('Raw::Z = ' + str(d['raw']['z']))
		texts[3].set_text('Scaled::X = ' + str(d['scaled']['x']))
		texts[4].set_text('Scaled::Y = ' + str(d['scaled']['y']))
		texts[5].set_text('Scaled::Z = ' + str(d['scaled']['z']))
		texts[6].set_text('Heading (rad) = ' + str(d['heading']))
		texts[7].set_text('Heading (deg) = ' + str(d['headingDegrees']))

	if update_lines.counter < npoints + 3 :
		data[0,num] = num
		data[1,num] = d['raw']['x']
		data[2,num] = d['raw']['y']
		data[3,num] = d['raw']['z']
		data[4,num] = d['scaled']['x']
		data[5,num] = d['scaled']['y']
		data[6,num] = d['scaled']['z']
		for i in range(len(lines)):
			lines[i].set_xdata(data[0,:num])
			lines[i].set_ydata(data[i+1,:num])
	else:
		data[1:7,0:(npoints-1)] = data[1:7,1:npoints]
		data[1,npoints-1] = d['raw']['x']
		data[2,npoints-1] = d['raw']['y']
		data[3,npoints-1] = d['raw']['z']
		data[4,npoints-1] = d['scaled']['x']
		data[5,npoints-1] = d['scaled']['y']
		data[6,npoints-1] = d['scaled']['z']
		for i in range(len(lines)):
			lines[i].set_xdata(data[0])
			lines[i].set_ydata(data[i+1])
	return lines + texts

npoints = 100
period = 50
update_lines.counter = 0

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.write('r')	# dummy char
time.sleep(.5)
#ser.flushInput()
for l in ser.readlines():
#	print(l)
	pass

fig1 = plt.figure()
plt.hold(True)

#data = np.random.rand(2, 25)
data = np.zeros([7, npoints])
#data[0] = np.arange(npoints)

lines = plt.plot([], [], 'r-', [], [], 'g-', [], [], 'b-', [], [], 'r--', [], [], 'g--', [], [], 'b--')
#for i in range(len(lines)):
#	lines[i].set_xdata(data[0])
#	lines[i].set_ydata(data[i+1])
plt.xlim(0, npoints)
plt.ylim(-1024, 1024)
plt.xlabel('x')
plt.title('test')

texts = []
ax, = fig1.get_axes()
for i in range(8):
	texts.append(plt.text(0, (i+1)*.05,'',
		horizontalalignment='left',
		verticalalignment='center',
		backgroundcolor='#ffffff',
		transform = ax.transAxes))

line_ani = animation.FuncAnimation(fig1, update_lines, npoints, fargs=(data, lines, texts),
		    interval=period, blit=True)

plt.show()

#while True:
##	ser.flushInput()
#	ser.write('r')
##	ser.flushOutput()
#	time.sleep(.5)
#	l = ser.readline()
##	print(l)
#	d = json.loads(l)
#	print(d)
#	time.sleep(.1)

