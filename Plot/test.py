import numpy
import matplotlib.pyplot as plt

x = numpy.linspace(0, 100, 9000)
y = numpy.linspace(0, 100, 9000)

x = 10 * numpy.cos(x)
y = 10 * numpy.sin(y)

x = x + numpy.random.normal(0, 0.1, 9000)
y = y + numpy.random.normal(0, 0.1, 9000)

#plt.plot(x, y)
#plt.show()

for a, b in zip(x, y):
    print a, b
