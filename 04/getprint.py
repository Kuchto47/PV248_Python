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
    cursor.execute("SELECT person.name, person.born, person.died "
                   "FROM person "
                   "WHERE person.id IN "
                   "(SELECT score_author.composer "
                   "FROM (print INNER JOIN edition ON print.edition = edition.id) "
                   "INNER JOIN score_author ON score_author.score = edition.score "
                   "WHERE print.id = ?)", (print_number,))
    persons = cursor.fetchall()
    result = []
    for person in persons:
        d = {}
        d["name"] = person[0]
        if person[1] is not None:
            d["born"] = str(person[1])
        if person[2] is not None:
            d["died"] = str(person[2])
        result.append(d)
    return result


main()
