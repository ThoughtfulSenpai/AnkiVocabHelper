import os
import sqlite3
from datetime import datetime

def create_connection(table_name):
    conn = None
    try:
        # Create a database file with the specified table name
        db_file_path = os.path.join(os.getcwd(), f'{table_name}.db')
        conn = sqlite3.connect(db_file_path)

       # (Create a table in the new database)
        create_table(conn)

        return conn
    except Exception as e:
        print(e)



def create_table(conn):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL,
                    frequency REAL,
                    date_added TEXT DEFAULT '01-01-1970'
                );'''
        conn.execute(sql)
    except Exception as e:
        print(e)

def add_language(conn, language):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS languages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    language TEXT NOT NULL
                );'''
        conn.execute(sql)
        sql = '''INSERT INTO languages(language) VALUES(?)'''
        cur = conn.cursor()
        cur.execute(sql, (language,))
        conn.commit()
    except Exception as e:
        print(e)

def get_language(conn):
    sql = '''SELECT language FROM languages ORDER BY id DESC LIMIT 1'''
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    return result[0] if result is not None else None

def delete_word(conn, word):
    sql = '''DELETE FROM words WHERE word = ?'''
    cur = conn.cursor()
    cur.execute(sql, (word,))
    conn.commit()

def add_word(conn, word, frequency):
    word = word.lower()
    sql = '''INSERT INTO words(word, frequency, date_added) VALUES(?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (word, float(frequency), datetime.now().strftime("%d-%m-%Y")))
    conn.commit()

def add_column(conn):
    try:
        sql = '''ALTER TABLE words ADD COLUMN date_added TEXT;'''
        conn.execute(sql)
    except Exception as e:
        print(e)

def add_favorite_column(conn):
    try:
        sql = '''ALTER TABLE words ADD COLUMN favorite INTEGER DEFAULT 0;'''
        conn.execute(sql)
    except Exception as e:
        print(e)

def get_favorite(conn, word):
    # Получите текущее состояние избранного для слова из базы данных
    sql = '''SELECT favorite FROM words WHERE word = ?'''
    cur = conn.cursor()
    cur.execute(sql, (word,))
    result = cur.fetchone()
    return result[0] if result is not None else None

def set_favorite(conn, word, favorite):
    # Установите новое состояние избранного для слова в базе данных
    sql = '''UPDATE words SET favorite = ? WHERE word = ?'''
    cur = conn.cursor()
    cur.execute(sql, (1 if favorite else 0, word))
    conn.commit()

def column_exists(conn, column_name):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info(words)")
    return any(row[1] == column_name for row in cur.fetchall())

def get_all_words(conn):
    sql = '''SELECT id, word, frequency, date_added, favorite FROM words ORDER BY favorite DESC, frequency ASC'''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def update_word_frequency(conn, word, frequency):
    sql = '''UPDATE words SET frequency = ? WHERE word = ?'''
    cur = conn.cursor()
    cur.execute(sql, (frequency, word))
    conn.commit()

def word_exists(conn, word):
    word = word.lower()
    sql = '''SELECT * FROM words WHERE word = ?'''
    cur = conn.cursor()
    cur.execute(sql, (word,))
    return cur.fetchone() is not None

def main():
    conn = create_connection()

    if conn is not None:
        create_table(conn)
    else:
        print("Error! Couldn't connect to Data Base.")


if __name__ == '__main__':
    main()
