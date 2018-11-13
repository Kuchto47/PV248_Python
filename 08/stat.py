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
    print(data.keys())


def dates(data):
    print(data.keys())


def deadlines(data):
    keys = data.keys()
    stats = get_means_medians_quantiles(data)
    d = {}
    for key in keys:
        if key == "student":
            continue
        d[key] = get_statistics(stats[0][[key]], stats[1][[key]], get_number_of_passed_guys(data.loc[:, key]), key)
    json.dump(d, sys.stdout, indent=4, ensure_ascii=False)


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


main()
