import datagetter
import sys
import sqlite3


def obtain_input_data_as_objects():
    return datagetter.get_print_objects_from_file(sys.argv[1])


def init_db():
    db_file = sys.argv[1]  # 2!!!
    connection = sqlite3.connect(db_file)
    c = connection.cursor()
    c.execute("create table person ( id integer primary key not null, born integer, died integer, name varchar not null );")
    c.execute("create table score ( id integer primary key not null, name varchar, genre varchar, key varchar, incipit varchar, year integer );")
    c.execute("create table voice ( id integer primary key not null, number integer not null, score integer references score( id ) not null,range varchar,name varchar );")
    c.execute("create table edition ( id integer primary key not null, score integer references score( id ) not null, name varchar, year integer );")
    c.execute("create table score_author( id integer primary key not null, score integer references score( id ) not null, composer integer references person( id ) not null );")
    c.execute("create table edition_author( id integer primary key not null, edition integer references edition( id ) not null, editor integer references person( id ) not null );")
    c.execute("create table print ( id integer primary key not null, partiture char(1) default 'N' not null, edition integer references edition( id ) );")
    return connection


def put_data_into_db(db, datas):
    #TODO


def main():
    c = init_db()
    prnts = obtain_input_data_as_objects()
    put_data_into_db(c, prnts)


main()
