import os
import sys

command = 'cat '+ sys.argv[1] + ' | grep "%s" | awk ' + "'{print $(NF - 2)" "$(NF - 1)" "$(NF)}' > thread_%s.dat"

for i in ["A", "G", "C"] :
    print command % (i, i)
    os.system(command % (i, i))
