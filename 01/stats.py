import sys
import re


def openFile():
    args = sys.argv
    return open(args[1], 'r', encoding="utf_8")


def getComposers():
    f = openFile()
    composers = {}
    exp = re.compile(r"Composer: (.*)")
    for line in f:
        getAllComposersFromLine(line, exp, composers)
    return composers


def getAllComposersFromLine(line, expression, d):
    match = expression.match(line)
    if match is not None:
        value = match.group(1)
        composers = getMultipleComposersFromOneLine(value)
        for composer in composers:
            v = d.get(composer)
            if v is None:
                d[composer] = 1
            else:
                d[composer] = v + 1


def getMultipleComposersFromOneLine(value):
    return value.split("; ")


# def getCenturies():
#     f = openFile()
#     centuries = {}
#     exp = re.compile(r"Composition Year: (.*)")
#     for line in f:
#         getAllComposersFromLine(line, exp, centuries)
#     return centuries

def main():
    comps = getComposers()
    for k, v in comps.items():
        print("%s: %d" % (k, v))


main()
