import sys

for line in sys.stdin:
    if "POS" in line.upper():
        data = line.strip().split()[1:]
        print data
