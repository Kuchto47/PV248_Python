#import numpy
import sys
import re


def main():
    file = open(sys.argv[1], 'r', encoding="utf_8")
    splitted_equations = []
    matrix = []
    results = []
    for line in file:
        splitted_equations.append(re.findall(r"(-? ?[0-9a-zA-Z]+)", line))
    for equation in splitted_equations:
        res_list = []
        for component in equation:
            if is_minus(component[0]):
                res_list.append(get_number(component[1:])*(-1))
            else:
                res_list.append(get_number(component))
        matrix.append(res_list[:-1])
        results.append(res_list[-1])


def is_minus(char):
    return char == "-"


def get_number(component):
    c = component.strip()
    if c[0].isdigit():
        return int(c[0])
    else:
        return 1


main()
