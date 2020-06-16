import sqlite3
from sqlite3 import Error


# db = sqlite3.connect('words.db')
# cur = db.cursor()
#
# cur.execute(
#     """CREATE TABLE IF NOT EXISTS words (words_id INTEGER NOT NULL PRIMARY KEY, content VARCHAR[150] NOT NULL)""")
# db.commit()
#
#
# def write_db(content):
#     cur.execute("SELECT words_id FROM words")
#     content_text = str(content)
#     cur.execute('insert into words(content) values (?)', (content_text,))
#     db.commit()
#
#
# write_db("Алардын чоңдору – чыгыш жактан куюлган Түп менен Жыргалаң суулары")

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




# def select_task_by_priority(conn, priority):
#     """
#     Query tasks by priority
#     :param conn: the Connection object
#     :param priority:
#     :return:
#     """
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
#
#     rows = cur.fetchall()
#
#     for row in rows:
#         print(row)


def main():
    database = "words.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # print("1. Query task by priority:")
        # select_task_by_priority(conn, 1)

        print("2. Query all tasks")
        select_all_tasks(conn)


if __name__ == '__main__':
    main()
