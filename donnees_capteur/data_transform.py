import os
import sys

command = 'cat '+ sys.argv[1] + ' | grep "Thread-%s" | awk ' + "'{print $(NF - 2)" "$(NF - 1)" "$(NF)}' > thread_%s.dat"

for i in [2, 3, 4] :
    print command % (i, i)
    os.system(command % (i, i))
