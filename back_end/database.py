import os.path
import sqlite3
import pathlib
from pathlib import Path


class DatabaseOps:
    def __init__(self):
        file_path = Path(__file__).resolve().parent
        print(file_path)
        self.conn = sqlite3.connect(os.path.join(file_path, "result.sqlite3"))
        print("connection es")
        self.cursor = self.conn.cursor()
        self.set_up()

    def set_up(self):
        sql_list = [
            "CREATE TABLE IF NOT EXISTS Class  (name CHAR)",
            "CREATE TABLE IF NOT EXISTS Subject  (name CHAR, grade CHAR, division CHAR)",
            "CREATE TABLE IF NOT EXISTS Student  (id INTEGER NOT NULL PRIMARY KEY, name CHAR, sex CHAR, class_ CHAR, age INT, state CHAR, lga CHAR)",
            "CREATE TABLE IF NOT EXISTS Score  (student CHAR, subject CHAR,"
            " assignment INT, test1 INT, test2 INT, exam INT, total INT)",
        ]
        for sql in sql_list:
            self.cursor.execute(sql)

    def insert_record(self, sql):
        try:
            return_value = self.cursor.execute(sql)
            self.conn.commit()
        except sqlite3.OperationalError:
            return_value = 'error'
        return return_value

    def fetch_record(self, key):
        if key.upper() == "ALL":
            sql = f"""SELECT * FROM Student"""
        else:
            sql = f"""SELECT * FROM Student WHERE class_ = '{key}' """
        try:
            return_value = self.cursor.execute(sql)
        except sqlite3.OperationalError:
            return_value = 'error'
        return return_value

    def search_record(self, word):
        sql = f"""SELECT * FROM Student WHERE name = '{word}' """
        return_value = self.cursor.execute(sql)
        return return_value

    def run_sql(self):
        sql = f"""SELECT * FROM Class"""
        return self.cursor.execute(sql)


# obj = DatabaseOps()
# obj.insert_record("INSERT INTO Class (name) VALUES ('JSS 1');")
# obj.insert_record("INSERT INTO Class (name) VALUES ('JSS 2');")
# obj.insert_record("INSERT INTO Class (name) VALUES ('JSS 3');")
# obj.insert_record("INSERT INTO Class (name) VALUES ('SSS 1');")
# obj.insert_record("INSERT INTO Class (name) VALUES ('SSS 2');")
# obj.insert_record("INSERT INTO Class (name) VALUES ('SSS 1');")
# obj.insert_record("INSERT INTO Subject (name, grade, division) VALUES ('Civil Education', 'senior', 'all');")
# obj.insert_record("INSERT INTO Subject (name, grade, division) VALUES ('Mathematics', 'senior', 'all');")
# obj.insert_record("INSERT INTO Subject (name, grade, division) VALUES ('Chemistry', 'senior', 'science');")
# obj.insert_record("INSERT INTO Score (student, subject, assignment, test1, test2, exam, total) VALUES ('Gabriel', 'Chemistry', 10, 10, 10, 70, 100);")
# obj.insert_record("INSERT INTO Score (student, subject, assignment, test1, test2, exam, total) VALUES ('Gabriel', 'Physics', 10, 10, 10, 70, 100);")
# obj.insert_record("INSERT INTO Score (student, subject, assignment, test1, test2, exam, total) VALUES ('Gabriel', 'Mathematics', 10, 10, 10, 70, 100);")
# obj.insert_record("""INSERT INTO Student (name, age, sex, state)
#             VALUES ('name', 'age', 'male', 'state');""")
