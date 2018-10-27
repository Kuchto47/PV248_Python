import numpy
import sys
import re
import copy


def main():
    file = open(sys.argv[1], 'r', encoding="utf_8")
    splitted_equations = []
    matrix = []
    results = []
    variables = []
    augmented_matrix = []
    for line in file:
        splitted_equations.append(re.findall(r"(-? ?[0-9a-zA-Z]+)", line))
    for equation in splitted_equations:
        res_list = get_equation_as_numbers(equation, variables)
        matrix.append(res_list[:-1])
        results.append(res_list[-1])
        augmented_matrix.append(res_list)
    try_solve(matrix, results, variables, augmented_matrix)


def try_solve(matrix, results, variables, augmented_matrix):
    number_of_solutions = get_solutions_count(matrix, augmented_matrix, len(variables))
    if number_of_solutions == 0:
        print("no solution")
    elif number_of_solutions == 1:
        solve(matrix, results, variables)
    else:
        print("solution space dimension: 1")


def solve(matrix, results, variables):
    result = get_solution(matrix, results)
    result_string = ""
    sorted_variables = copy.deepcopy(variables)
    sorted_variables.sort()
    for i, var in enumerate(sorted_variables):
        index_of_var_in_original_list = variables.index(var)
        result_string += var + " = " + str(result[index_of_var_in_original_list])
        if i < len(result):
            result_string += ", "
    print("solution: " + result_string)


def get_solution(matrix, results):
    a = numpy.array(matrix)
    b = numpy.array(results)
    return numpy.linalg.solve(a, b)


def get_solutions_count(coef_matrix, augm_matrix, number_of_vars):
    coef_matrix_rank = numpy.linalg.matrix_rank(coef_matrix)
    augm_matrix_rank = numpy.linalg.matrix_rank(augm_matrix)
    if coef_matrix_rank != augm_matrix_rank:
        return 0
    return 1 if number_of_vars == coef_matrix_rank else 2


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
