from pylab import *

l_name = ['./thread_A.dat', './thread_G.dat', './thread_C.dat']

def _plot(f_name) :
    l_x = []
    l_y = []
    l_z = []
    print 'lol', f_name
    with open(f_name, "r") as f:
        for i in f:
            x, y, z = 0, 0, 0
            try:
                data = i.strip()[1:-1]
                data = data.split(",")
                x, y, z = map(float, data)
            except ValueError:
                print data
                continue
            l_x.append(x)
            l_y.append(y)
            l_z.append(z)
    print '    x avg :', sum(l_x) * 1.0 / len(l_x)
    print '    y avg :', sum(l_y) * 1.0 / len(l_y)
    print '    z avg :', sum(l_z) * 1.0 / len(l_z)
    for l, d in zip([l_x, l_y, l_z], ["x", "y", "z"]) :
        plot(l)
        name = f_name.split('./')[1].split(".")[0] + "_" + d + ".png"
        print("sauvegarde : {}".format(name))
        savefig(name)
        clf()

for name in l_name :
    print 'lil', name
    _plot(name)
