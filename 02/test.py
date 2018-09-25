import sys
import scorelib


def test():
    filename = sys.argv[1]
    prints = scorelib.load(filename)
    for prnt in prints:
        prnt.format()

