import os
import sqlite3
import src.const as const
from sqlite3 import Error


def init_database():
    if not os.path.exists(const.DB_DIR):
        os.makedirs(const.DB_DIR)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS "AudioFragments" (
                                                                    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                    "author_id" INTEGER, 
                                                                    "fragment_name" TEXT UNIQUE
                                                                )''')
    conn.close()


def get_fragment_id_by_name(conn, name):
    sql = '''SELECT id FROM AudioFragments WHERE fragment_name = ?'''
    cur = conn.cursor()
    cur.execute(sql, [str(name)])
    return cur.fetchall()


def add_fragment(conn, author_id, name):
    sql = '''INSERT INTO AudioFragments(author_id, fragment_name) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (author_id, name))
    conn.commit()
    return get_fragment_id_by_name(conn, name)


def delete_fragment(conn, fragment_id):
    sql = '''DELETE FROM AudioFragments WHERE id like ?'''
    cur = conn.cursor()
    cur.execute(sql, [str(fragment_id)])
    conn.commit()


def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(const.DB_FILE)
    except Error as e:
        print(e)
    return conn
