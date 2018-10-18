import sys
import db_connector
import json


def main():
    name = str(sys.argv[1])
    db = db_connector.connect_db()
    cursor = db.cursor()
    rows_with_name = get_all_rows_with_name(name, cursor)
    result_dict = {}
    for row in rows_with_name:
        list_of_prints = get_list_of_prints_for_name(row, cursor)
        result_dict[row[3]] = list_of_prints
    json.dump(result_dict, sys.stdout, indent=4, ensure_ascii=False)


def get_all_rows_with_name(name, cursor):
    name_for_select = "%"+name+"%"
    cursor.execute("SELECT * FROM person where name LIKE ?", (name_for_select,))
    return cursor.fetchall()


def get_list_of_prints_for_name(row, cursor):
    name = row[3]
    result_list = []
    return result_list
