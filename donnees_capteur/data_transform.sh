#!/bin/sh
cat $1 | grep "A" | awk '{print $(NF - 2)" "$(NF - 1)" "$(NF)}' > ./thread_A.dat
cat $1 | grep "G" | awk '{print $(NF - 2)" "$(NF - 1)" "$(NF)}' > ./thread_G.dat
cat $1 | grep "C" | awk '{print $(NF - 2)" "$(NF - 1)" "$(NF)}' > ./thread_C.dat
