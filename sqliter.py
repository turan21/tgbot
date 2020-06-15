import sqlite3

db = sqlite3.connect('users.db')
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER NOT NULL PRIMARY KEY, username INTEGER NOT NULL,file_path TEXT, age INTEGER, gender INTEGER)""")
db.commit()

username = int(input("username : "))
file_path = input("Path : ")
age = int(input("age : "))
gender = int(input("gender : "))
data_person_name = [(username, file_path,age,gender),]

cur.execute("SELECT user_id FROM users")
cur.executemany('INSERT INTO users(username, file_path, age, gender) VALUES (?,?,?,?)', data_person_name)
db.commit()

