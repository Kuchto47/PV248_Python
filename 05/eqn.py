#import numpy
import sys
import re


def main():
    file = open(sys.argv[1], 'r', encoding="utf_8")
    splitted_equations = []
    matrix = []
    results = []
    variables = []
    for line in file:
        splitted_equations.append(re.findall(r"(-? ?[0-9a-zA-Z]+)", line))
    for equation in splitted_equations:
        res_list = get_equation_as_numbers(equation, variables)
        matrix.append(res_list[:-1])
        results.append(res_list[-1])
    print(matrix, "###", results, "###", variables)  # check of parsing -- delete before final push


def get_equation_as_numbers(eq, variables):
    res_list = []
    d = {}
    for i, component in enumerate(eq):
        if component[0] == "-":
            t = get_info(component[1:])
            is_negative = True
        else:
            t = get_info(component)
            is_negative = False
        if t[0] is not None:
            var = t[0].group(1)
            if var not in variables:
                variables.append(var)
            d[var] = actual_number(t[1])*(-1) if is_negative else actual_number(t[1])
        else:
            res_list.insert(i, actual_number(t[1]))
    for i, var in enumerate(variables):
        if var in d.keys():
            res_list.insert(i, d[var])
        else:
            res_list.insert(i, 0)
    return res_list


def get_info(component):
    c = component.strip()
    number = re.match(r"([0-9]+)", c)
    variable = re.match(r".*([a-zA-Z])", c)
    return variable, number


def actual_number(number):
    if number is not None:
        return int(number.group(1))
    else:
        return 1


main()
