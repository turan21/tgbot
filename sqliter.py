import sqlite3
from sqlite3 import Error


class Words():
    WORDS_LIST = []


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT content FROM words")

    rows = cur.fetchall()

    for row in rows:
        Words.WORDS_LIST.append(row)
        # print(row)


def main():
    database = "words.db"

    conn = create_connection(database)
    with conn:
        select_all_tasks(conn)


if __name__ == '__main__':
    main()
