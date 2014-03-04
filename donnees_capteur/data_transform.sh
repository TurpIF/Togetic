#!/bin/sh
usage="Usage:
./data_transform <data-file>

Read the <data-file> file and take the tree last columns of the lines
beginning by \"A \", \"G \" and \"C \" into, respectively ./thread_A.dat,
./thread_G.dat and ./thread_C.dat."

[ "$#" -ne 1 ] && echo "$usage" && exit 1
cat $1 | grep "^A " | awk '{print $(NF - 2)" "$(NF - 1)" "$(NF)}' > ./thread_A.dat
cat $1 | grep "^G " | awk '{print $(NF - 2)" "$(NF - 1)" "$(NF)}' > ./thread_G.dat
cat $1 | grep "^C " | awk '{print $(NF - 2)" "$(NF - 1)" "$(NF)}' > ./thread_C.dat
