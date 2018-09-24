import sys
import re


def open_file():
    file_path = sys.argv[1]
    return open(file_path, 'r', encoding="utf_8")


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
            composer = extract_years_from_name(composer)
            trimmed_composer = composer.strip()
            if trimmed_composer == "":
                continue
            v = d.get(trimmed_composer)
            if v is None:
                d[trimmed_composer] = 1
            else:
                d[trimmed_composer] = v + 1


def get_multiple_composers_from_one_line(value):
    return value.split(";")


def extract_years_from_name(name):
    return re.sub(r'\([^)]*\)', '', name)


def get_centuries():
    f = open_file()
    centuries = {}
    exp = re.compile(r"Composition Year:(.*)")
    for line in f:
        get_all_centuries(line, exp, centuries)
    return centuries


def get_all_centuries(line, exp, d):
    match = exp.match(line)
    if match is not None:
        value = match.group(1)
        year = get_year(value)
        if year is not None:
            century = int(int(year.group(1))/100) + 1
            add_century(d, century)
        else:
            actual_century = get_century_otherwise(value)
            if actual_century is not None:
                century = int(actual_century.group(1))
                add_century(d, century)


def add_century(dictionary, century):
    count = dictionary.get(century)
    if count is None:
        dictionary[century] = 1
    else:
        dictionary[century] = count + 1


def get_century_otherwise(value):
    exp = re.compile(r".*([0-9]{2}).*")
    return exp.match(value)


def get_year(value):
    exp = re.compile(r".*([0-9]{4}).*")
    return exp.match(value)


def century_wanted():
    centuries = get_centuries()
    for k, v in centuries.items():
        print("%sth century: %s" % (k, v))


def composers_wanted():
    comps = get_composers()
    for k, v in comps.items():
        print("%s: %d" % (k, v))


def main():
    choice = sys.argv[2]
    if choice == "composer":
        composers_wanted()
    elif choice == "century":
        century_wanted()


main()
