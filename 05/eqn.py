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
        res_list = []
        for i, component in enumerate(equation):
            if is_minus(component[0]):
                res_list.append(get_number(component[1:], variables, i)*(-1))
            else:
                res_list.append(get_number(component, variables, i))
        matrix.append(res_list[:-1])
        results.append(res_list[-1])
    print(matrix, "###", results, "###", variables)


def is_minus(char):
    return char == "-"


def get_number(component, variables, index):
    c = component.strip()
    number = re.match(r"([0-9]+)", c)
    variable = re.match(r".*([a-zA-Z])", c)
    if variable is not None:
        var = variable.group(1)
        if var in variables:
            if variables[index] == var:
                return actual_number(number)
            #TODO
        else:
            variables.append(var)
            return actual_number(number)
    else:
        return actual_number(number)


def actual_number(number):
    if number is not None:
        return int(number.group(1))
    else:
        return 1


main()
