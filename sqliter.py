# import sqlite3
# class Sqliter:
#     def __init__(self,database):
#         self.connection = sqlite3.connect(database)
#         self.cursor = self.connection.cursor()
#
#     def select_all(self):
#         with self.connection:
#             return self.cursor.execute('SELECT * FROM users').fetchall()
#
#     def create_connection(db_file):
#         """ create a database connection to the SQLite database
#             specified by db_file
#         :param db_file: database file
#         :return: Connection object or None
#         """
#         conn = None
#         try:
#             conn = sqlite3.connect(db_file)
#         except Exception as e:
#             print(e)
#
#         return conn