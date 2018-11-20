import pandas
import sys
import numpy
import json
import datetime
import math


def main():
    data = pandas.read_csv(sys.argv[1])
    json.dump(get_data(data), sys.stdout, indent=4, ensure_ascii=False)


def get_mean_median(data):
    return data.mean(), data.median()


def get_passed_count(data):
    passed = 0
    for d in data:
        if float(d) > 0:
            passed += 1
    return passed


def get_slope(data):
    cumulated_data = data.cumsum()
    x = numpy.array(cumulated_data.keys())
    y = numpy.array(cumulated_data.values)
    a = numpy.vstack([x, numpy.zeros(len(x))]).T
    return numpy.linalg.lstsq(a, y, 1)[0][0]


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
    data_with_days_from_start_of_semester = get_data_with_days_from_start_of_semester(student_data)
    data_grouped_by_exercises = get_data_grouped_by_exercises(student_data)
    mean_median = get_mean_median(data_grouped_by_exercises)
    slope = get_slope(data_with_days_from_start_of_semester)
    return {
        "mean": mean_median[0],
        "median": mean_median[1],
        "total": data_with_days_from_start_of_semester.sum(),
        "passed": get_passed_count(data_grouped_by_exercises),
        "regression slope": slope,
        "date 16": float("inf") if slope == 0 else get_date_from_days(16/slope),
        "date 20": float("inf") if slope == 0 else get_date_from_days(20/slope)
    }


def get_data_grouped_by_exercises(data):
    extra_length = len("YYYY-MM-DD/")
    return data.groupby(data.keys().map(lambda x: x[extra_length:])).sum()


def get_data_with_days_from_start_of_semester(data):
    extra_length = len("/NN") * (-1)
    grouped_data = data.groupby(data.keys().map(lambda x: x[:extra_length])).sum()
    data_with_days_from_start_of_semester = grouped_data.rename(lambda x: update_key(x))
    return data_with_days_from_start_of_semester


def get_date_from_days(days_from_start_of_semester):
    start_of_semester = datetime.date(2018, 9, 17)
    timedelta = datetime.timedelta(days=days_from_start_of_semester)
    date = start_of_semester+timedelta
    print("DATE - DELTA:", date-timedelta)
    return "%d-%02d-%02d" % (date.year, date.month, date.day)


main()
