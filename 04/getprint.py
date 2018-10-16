import sys
import db_connector
import json


def main():
    print_number = int(sys.argv[1])
    db = db_connector.connect_db()
    cursor = db.cursor()
    obtained_composers = get_composers_from_print_id(print_number, cursor)
    json.dump(obtained_composers, sys.stdout, indent=4, ensure_ascii=False)


def get_composers_from_print_id(print_number, cursor):
    cursor.execute("SELECT edition FROM print WHERE id IS ?", (print_number,))
    print_record = cursor.fetchone()
    cursor.execute("SELECT score FROM edition WHERE id IS ?", (print_record[0],))
    edition_record = cursor.fetchone()
    cursor.execute("SELECT composer FROM score_author WHERE score IS ?", (edition_record[0],))
    score_authors = cursor.fetchall()
    result = []
    for score_author in score_authors:
        cursor.execute("SELECT name, born, died FROM person WHERE id IS ?", (score_author[0],))
        composer = cursor.fetchone()
        d = {}
        d["name"] = composer[0]
        if composer[1] is not None:
            d["born"] = str(composer[1])
        if composer[2] is not None:
            d["died"] = str(composer[2])
        result.append(d)
    return result


main()
