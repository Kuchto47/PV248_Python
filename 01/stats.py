import sys
import re


def open_file():
    args = sys.argv
    return open(args[1], 'r', encoding="utf_8")


def get_composers():
    f = open_file()
    composers = {}
    exp = re.compile(r"Composer: (.*)")
    for line in f:
        get_all_composers_from_line(line, exp, composers)
    return composers


def get_all_composers_from_line(line, expression, d):
    match = expression.match(line)
    if match is not None:
        value = match.group(1)
        composers = get_multiple_composers_from_one_line(value)
        for composer in composers:
            composer_without_years = extract_years_from_name(composer)
            trimmed_composer = composer_without_years.strip()
            v = d.get(trimmed_composer)
            if v is None:
                d[trimmed_composer] = 1
            else:
                d[trimmed_composer] = v + 1


def get_multiple_composers_from_one_line(value):
    return value.split(";")


def extract_years_from_name(name):
    expression = re.compile(r"") #TODO!
    return expression.match(name).group(1)


# def getCenturies():
#     f = openFile()
#     centuries = {}
#     exp = re.compile(r"Composition Year: (.*)")
#     for line in f:
#         getAllComposersFromLine(line, exp, centuries)
#     return centuries

def main():
    comps = get_composers()
    for k, v in comps.items():
        print("%s: %d" % (k, v))


main()
