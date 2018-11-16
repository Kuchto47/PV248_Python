import pandas
import sys
import json


def main():
    data = pandas.read_csv(sys.argv[1])
    mode = sys.argv[2]
    if mode == "exercises":
        exercises(data)
    elif mode == "dates":
        dates(data)
    elif mode == "deadlines":
        deadlines(data)
    else:
        print('Invalid mode')


def exercises(data):
    extra_length = len("YYYY-MM-DD/")
    clear_data = data.drop(columns="student")
    grouped_data = clear_data.groupby(clear_data.columns.map(lambda x: x[extra_length:]), axis=1).sum()
    json.dump(get_dictionary(grouped_data), sys.stdout, indent=4, ensure_ascii=False)


def dates(data):
    extra_length = len("/NN")*(-1)
    clear_data = data.drop(columns="student")
    grouped_data = clear_data.groupby(clear_data.columns.map(lambda x: x[:extra_length]), axis=1).sum()
    json.dump(get_dictionary(grouped_data), sys.stdout, indent=4, ensure_ascii=False)


def deadlines(data):
    json.dump(get_dictionary(data.drop(columns="student")), sys.stdout, indent=4, ensure_ascii=False)


def get_means_medians_quantiles(data):
    return data.aggregate(["mean", "median"]), data.quantile([.25, .75])


def get_statistics(current_means_medians, current_quartiles, passed, key):
    return {
            "mean": current_means_medians.loc["mean", key],
            "median": current_means_medians.loc["median", key],
            "first": current_quartiles.loc[0.25, key],
            "last": current_quartiles.loc[0.75, key],
            "passed": passed
        }


def get_number_of_passed_guys(points):
    passed = 0
    for point in points:
        if point > 0:
            passed += 1
    return passed


def get_dictionary(data):
    keys = data.keys()
    stats = get_means_medians_quantiles(data)
    d = {}
    for key in keys:
        d[key] = get_statistics(stats[0][[key]], stats[1][[key]], get_number_of_passed_guys(data.loc[:, key]), key)
    return d


main()
