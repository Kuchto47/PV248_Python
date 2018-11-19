import pandas
import sys
import numpy
import json
import datetime


def main():
    data = pandas.read_csv(sys.argv[1])
    json.dump(get_data(data), sys.stdout, indent=4, ensure_ascii=False)


def get_mean_median(data):
    return data.mean(), data.median()


def get_passed_count(data):
    passed = 0
    for d in data:
        if int(d) > 0:
            passed += 1
    return passed


def get_slope(data):
    extra_length = len("/NN")*(-1)
    grouped_data = data.groupby(data.keys().map(lambda x: x[:extra_length])).sum()
    data_with_days_from_start_of_semester = grouped_data.rename(lambda x: update_key(x))
    print(data_with_days_from_start_of_semester)
    return None
    # y = numpy.array(data.values[0])
    # print(y)
    # x = numpy.array(range(0, len(data.values[0])))
    # print(x)
    # A = numpy.vstack([x, [0]*len(x)]).T
    # print(A)
    # return numpy.polyfit(data.values[0], [0]*len(data.values[0]), 1)


def update_key(key):
    start_of_semester = datetime.date(2018, 9, 17)
    date_format = "%Y-%m-%d"
    d = datetime.datetime.strptime(key, date_format)
    return (d.date() - start_of_semester).days


def get_data(data):
    student = sys.argv[2]
    if student == "average":
        student_data = data.drop(columns="student").mean()
    else:
        student_data = data[data['student'] == int(student)].drop(columns="student").mean()
    mean_median = get_mean_median(student_data)
    return {
        "mean": mean_median[0],
        "median": mean_median[1],
        "total": student_data.sum(),
        "passed": get_passed_count(student_data),
        "regression slope": get_slope(student_data)
    }


main()
