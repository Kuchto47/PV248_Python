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
        list_of_prints = get_list_of_prints_for_composer(row[0], cursor)
        result_dict[row[3]] = list_of_prints
    json.dump(result_dict, sys.stdout, indent=4, ensure_ascii=False)


def get_all_rows_with_name(name, cursor):
    name_for_select = "%"+name+"%"
    cursor.execute("SELECT * FROM person where name LIKE ?", (name_for_select,))
    return cursor.fetchall()


def get_list_of_prints_for_composer(composer_id, cursor):
    result_list = []
    cursor.execute("SELECT score FROM score_author WHERE composer IS ?", (composer_id,))
    scores_ids = cursor.fetchall()
    for score_id in scores_ids:
        one_dict = {}
        cursor.execute("SELECT score.id, "  #0
                       "edition.id, "       #1
                       "score.name, "       #2
                       "score.genre, "      #3
                       "score.key, "        #4
                       "score.incipit, "    #5
                       "score.year, "       #6
                       "edition.name, "     #7
                       "print.id, "         #8
                       "print.partiture "   #9
                       "FROM (score INNER JOIN edition ON score.id = edition.score) "
                       "INNER JOIN print on edition.id = print.edition "
                       "WHERE score.id = ?", (score_id[0],))
        result_row = cursor.fetchone()
        cursor.execute("SELECT person.name FROM person INNER JOIN score_author ON score_author.composer = person.id "
                       "WHERE score_author.score = ?", (result_row[0],))
        authors_names = cursor.fetchall()
        cursor.execute("SELECT person.name FROM person INNER JOIN edition_author ON edition_author.editor = person.id "
                       "WHERE edition_author.edition = ?", (result_row[1],))
        editors_names = cursor.fetchall()
        cursor.execute("SELECT number, name, range FROM voice WHERE voice.score = ?", (result_row[0],))
        voices = cursor.fetchall()
        init_dict(one_dict, result_row, authors_names, editors_names, voices)
        result_list.append(one_dict)
    return result_list


def init_dict(d, row, authors_names, editors_names, voices):
    d["Print Number"] = row[8]
    d["Composer"] = get_names_list(authors_names)
    if row[2] is not None:
        d["Title"] = row[2]
    if row[3] is not None:
        d["Genre"] = row[3]
    if row[4] is not None:
        d["Key"] = row[4]
    if row[6] is not None:
        d["Composition Year"] = row[6]
    if row[7] is not None:
        d["Edition"] = row[7]
    d["Editor"] = get_names_list(editors_names)
    d["Voices"] = get_voices_dict(voices)
    if row[9] is not None:
        d["Partiture"] = row[9] == "Y"
    if row[5] is not None:
        d["Incipit"] = row[5]


def get_voices_dict(voices):
    res = {}
    for voice in voices:
        if voice[1] is None and voice[2] is None:
            continue
        partial = {}
        if voice[1] is not None:
            partial["name"] = voice[1]
        if voice[2] is not None:
            partial["range"] = voice[2]
        res[str(voice[0])] = partial
    return res


def get_names_list(names):
    res = []
    for name in names:
        res.append(name[0])
    return res


main()
