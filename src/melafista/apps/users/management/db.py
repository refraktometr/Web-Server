import psycopg2


def get_cursor(name_database=None):
    query = "host='localhost'  user='postgres' password='postgres'"
    if name_database:
        query += " dbname=%s" % name_database
    conn = psycopg2.connect(query)
    cursor = conn.cursor()
    conn.autocommit = True
    return cursor


def create_database(name_database):
    cursor = get_cursor()
    query = "CREATE DATABASE {};".format(name_database)
    cursor.execute(query)
    print "database-", name_database, "is created"


def _create_sequence_user_id(name_database='melafista'):
    cursor = get_cursor(name_database)
    cursor.execute('CREATE SEQUENCE user_id;')
    print "sequence- user_id in-", name_database, "is created"


def create_table_users(name_database='melafista'):
    _create_sequence_user_id(name_database)
    cursor = get_cursor(name_database)
    cursor.execute(""" CREATE TABLE users (id INTEGER NOT NULL PRIMARY KEY DEFAULT NEXTVAL('user_id'),
                                    username VARCHAR(32) NOT NULL UNIQUE,
                                    password VARCHAR(128) NOT NULL,
                                    salt CHAR(32) NOT NULL);""")
    print "table- users in-", name_database, "is created"


def create_table_users_message(name_database='melafista'):
    cursor = get_cursor(name_database)
    cursor.execute("""CREATE TABLE users_message (user_id INTEGER NOT NULL REFERENCES users(id),
                        recipient_id INTEGER NOT NULL REFERENCES users(id),
                        text_message VARCHAR(1000000) NOT NULL,
                        create_at timestamp DEFAULT NOW(),
                        flag_reading BOOLEAN NOT NULL DEFAULT False
                        ); """)
    print "table- users_message in-", name_database, "is created"


def create_table_sessions(name_database='melafista'):
    cursor = get_cursor(name_database)
    cursor.execute("""CREATE TABLE sessions (
                    session_id char(64) NOT NULL UNIQUE,
                    data VARCHAR(10000) NOT NULL,
                    create_at timestamp DEFAULT NOW())""")
    print "table- sessions in-", name_database, "is created"


def setup_database(database_name):
    create_database(database_name)
    create_table_users(name_database=database_name)
    create_table_users_message(name_database=database_name)
    create_table_sessions(name_database=database_name)


def delete_database(name_database):
    cursor = get_cursor()
    query = "DROP DATABASE {};".format(name_database)
    cursor.execute(query)
    print "database-", name_database, "is deleted"


def flush_tables(name_database):
    cursor = get_cursor(name_database)
    cursor.execute("TRUNCATE TABLE users_message CASCADE")
    cursor.execute("TRUNCATE TABLE sessions CASCADE;")
    cursor.execute("TRUNCATE TABLE users CASCADE;")
