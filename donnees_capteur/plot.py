from pylab import *

l_name = ['./thread_2.dat', './thread_3.dat', './thread_4.dat']

def _plot(f_name) :
    l_x = []
    l_y = []
    l_z = []
    print 'lol', f_name
    with open(f_name, "r") as f:
        for i in f:
            data = i.strip()[1:-1]
            data = data.split(",")
            x, y, z = data
            l_x.append(x)
            l_y.append(y)
            l_z.append(z)
    for l, d in zip([l_x, l_y, l_z], ["x", "y", "z"]) :
        plot(l)
        name = f_name.split('./')[1].split(".")[0] + "_" + d + ".png"
        print("sauvegarde : {}".format(name))
        savefig(name)
        clf()

for name in l_name :
    print 'lil', name
    _plot(name)
