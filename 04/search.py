import sys
import db_connector
import json


def main():
    name = str(sys.argv[1])
    db = db_connector.connect_db()
    cursor = db.cursor()
    rows_with_name = get_all_rows_with_name(name, cursor)


def get_all_rows_with_name(name, cursor):
    name_for_select = "%"+name+"%"
    cursor.execute("SELECT * FROM person where name LIKE ?", (name_for_select,))
    return cursor.fetchall()