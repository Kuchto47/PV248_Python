import datagetter
import sys
import sqlite3


def obtain_input_data_as_objects():
    return datagetter.get_print_objects_from_file(sys.argv[1])


def init_db():
    db_file = sys.argv[2]  # 2!!!
    connection = sqlite3.connect(db_file)
    c = connection.cursor()
    c.execute("create table person ( id integer primary key not null, born integer, died integer, name varchar not null );")
    c.execute("create table score ( id integer primary key not null, name varchar, genre varchar, key varchar, incipit varchar, year integer );")
    c.execute("create table voice ( id integer primary key not null, number integer not null, score integer references score( id ) not null,range varchar,name varchar );")
    c.execute("create table edition ( id integer primary key not null, score integer references score( id ) not null, name varchar, year integer );")
    c.execute("create table score_author( id integer primary key not null, score integer references score( id ) not null, composer integer references person( id ) not null );")
    c.execute("create table edition_author( id integer primary key not null, edition integer references edition( id ) not null, editor integer references person( id ) not null );")
    c.execute("create table print ( id integer primary key not null, partiture char(1) default 'N' not null, edition integer references edition( id ) );")
    connection.commit()
    return connection


def put_data_into_db(db, datas):
    for rec in datas:
        write_object(db, rec)
    db.commit()


def write_object(db, rec):
    c = db.cursor()
    composers_ids = insert_persons(c, rec.edition.composition.authors)
    editors_ids = insert_persons(c, rec.edition.authors)
    score_id = insert_score(c, rec.edition.composition)
    edition_id = insert_edition(c, rec.edition, score_id)
    insert_score_authors(c, composers_ids, score_id)
    insert_edition_authors(c, editors_ids, edition_id)
    insert_voices(c, rec.edition.composition.voices, score_id)
    insert_print(c, rec, edition_id)
    c.close()


def insert_print(cursor, record, edition_id):
    partiture = 'N'
    if record.partiture:
        partiture = 'Y'
    v = (record.print_id, partiture, edition_id)
    cursor.execute("SELECT * from print WHERE id IS ?", (record.print_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO print(id, partiture, edition) VALUES (?,?,?)", v)


def insert_voices(cursor, voices, score_id):
    for voice in voices:
        v = (voice.order, score_id, voice.range, voice.name)
        cursor.execute("SELECT * FROM voice WHERE number IS ? AND score IS ? AND range IS ? AND name IS ?", v)
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO voice(number, score, range, name) VALUES (?,?,?,?)", v)


def insert_edition_authors(cursor, editors_ids, edition_id):
    for editor in editors_ids:
        v = (edition_id, editor)
        cursor.execute("SELECT * FROM edition_author WHERE edition IS ? AND editor is ?", v)
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO edition_author(edition, editor) VALUES (?,?)", v)


def insert_score_authors(cursor, composers_ids, score_id):
    for composer in composers_ids:
        v = (score_id, composer)
        cursor.execute("SELECT * FROM score_author WHERE score IS ? AND composer is ?", v)
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO score_author(score, composer) VALUES (?,?)", v)


def insert_edition(cursor, edition, score_id):
    v = (score_id, edition.name, None)
    cursor.execute("SELECT * FROM edition WHERE score IS ? AND name IS ? AND year IS ?", v)
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO edition(score, name, year) VALUES (?,?,?)", v)
        return cursor.lastrowid
    return result[0]


def insert_score(cursor, composition):
    v = (composition.name, composition.genre, composition.key, composition.incipit, composition.year)
    cursor.execute("SELECT * FROM score WHERE name IS ? AND genre IS ? AND key IS ? AND incipit IS ? AND year IS ?", v)
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO score(name, genre, key, incipit, year) VALUES (?,?,?,?,?)", v)
        return cursor.lastrowid
    return result[0]


def insert_persons(cursor, persons):
    ids = []
    for person in persons:
        name = person.name
        if name is None:
            name = ""
        cursor.execute("SELECT * FROM person WHERE name IS ?", (name,))
        fetched = cursor.fetchone()
        if fetched is None:
            cursor.execute("INSERT INTO person(born, died, name) VALUES (?,?,?)", (person.born, person.died, name))
            ids.append(cursor.lastrowid)
        else:
            ids.append(fetched[0])
            born = fetched[1]
            died = fetched[2]
            if born is None:
                if person.born is not None:
                    cursor.execute("UPDATE person SET born=? WHERE id=?", (person.born, fetched[0]))
            if died is None:
                if person.died is not None:
                    cursor.execute("UPDATE person SET died=? WHERE id=?", (person.died, fetched[0]))
    return ids


def main():
    c = init_db()
    prnts = obtain_input_data_as_objects()
    put_data_into_db(c, prnts)


main()
