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
    composer_name = row[3]
    born = row[1]
    died = row[2]
    composer_id = row[0]
    result_list = []
    cursor.execute("SELECT score FROM score_author WHERE composer IS ?", (composer_id,))
    scores_ids = cursor.fetchall()
    scores = get_scores(scores_ids, cursor)
    for score in scores:


    return result_list


def get_scores(scores_ids, cursor):
    scores = []
    for score_id in scores_ids:
        cursor.execute("SELECT * FROM score WHERE id IS ?", (score_id,))
        scores.append(cursor.fetchone())
    return scores


main()