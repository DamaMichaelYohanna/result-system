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
            "CREATE TABLE IF NOT EXISTS Session  (name CHAR UNIQUE, status CHAR )",
            "CREATE TABLE IF NOT EXISTS Term  (name CHAR, status CHAR)",
            "CREATE TABLE IF NOT EXISTS Subject  (name CHAR, class CHAR, division CHAR)",
            "CREATE TABLE IF NOT EXISTS Student  (id INTEGER NOT NULL PRIMARY KEY, name CHAR, sex CHAR, class_ CHAR, age INT, state CHAR, lga CHAR)",
            "CREATE TABLE IF NOT EXISTS Score  (student CHAR, subject CHAR, session CHAR,"
            " term CHAR, first_CA INT, second_CA INT, exams INTEGER, total INT)"
        ]
        for sql in sql_list:
            self.cursor.execute(sql)
            self.conn.commit()

    def insert_record(self, sql):
        try:
            return_value = self.cursor.execute(sql)
            self.conn.commit()
        except sqlite3.OperationalError as error:
            return_value = error
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

    def fetch_class(self):
        sql = f"""SELECT * FROM Class"""
        return self.cursor.execute(sql)

    def fetch_session(self):
        sql = f"""SELECT * FROM Session"""
        return self.cursor.execute(sql)

    def fetch_subject_per_class(self, class_):
        sql = f"""SELECT name FROM Subject WHERE class = '{class_}'"""
        return self.cursor.execute(sql)

    def fetch_result(self, class_, subject, session):
        sql = f"""SELECT student, session, term FROM Subject"""
        return self.cursor.execute(sql)

    def insert_score(self, student_name, subject, session, first_Ca, second_ca, exam):
        """function to isert the new data into the ict"""
        sql = f"""INSERT INTO Score (student, subject, session, first_ca, second_ca, exam, total) 
        VALUES ({student_name}, {subject}, "{session}", '{first_Ca}', '{second_ca}', {exam} )"""
        result= self.cursor.execute(sql)
        self.conn.commit()


    def run_sql(self, sql):
        result= self.cursor.execute(sql)
        self.conn.commit()
        return result


obj = DatabaseOps()
# "INSERT INTO Term (name) VALUES ('Second')",
# "INSERT INTO Term (name) VALUES ('Third')"
# obj.insert_record("INSERT INTO Subject (name, class) VALUES ('English', 'JSS 1');")
# obj.insert_record("INSERT INTO Subject (name, class) VALUES ('Mathematics', 'JSS 1');")
# obj.insert_record("INSERT INTO Subject (name, class) VALUES ('Basic Science', 'JSS 1');")
# obj.conn.commit()
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
