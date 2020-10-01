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
    cursor.execute('''CREATE TABLE IF NOT EXISTS "Admins" (
                                                                    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                    "user_id" INTEGER UNIQUE
                                                                )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS "Responses" (
                                                                    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                    "response" TEXT UNIQUE
                                                                )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS "Keywords" (
                                                                    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                    "keyword" TEXT UNIQUE
                                                                )''')
    conn.close()


def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(const.DB_FILE)
    except Error as e:
        print(e)
    return conn


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


def get_all_keywords(conn):
    sql = '''SELECT keyword FROM Keywords'''
    cur = conn.cursor()
    cur.row_factory = lambda cursor, row: row[0]
    cur.execute(sql)
    results = cur.fetchall()
    return results


def is_keyword(conn, keyword):
    sql = '''SELECT id FROM Keywords WHERE keyword = ?'''
    cur = conn.cursor()
    cur.execute(sql, [str(keyword)])
    results = cur.fetchall()
    return len(results) > 0


def add_keyword(conn, keyword):
    sql = '''INSERT INTO Keywords(keyword) VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql, [str(keyword)])
    conn.commit()


def delete_keyword(conn, keyword):
    sql = '''DELETE FROM Keywords WHERE keyword = ?'''
    cur = conn.cursor()
    cur.execute(sql, [str(keyword)])
    conn.commit()


def is_response(conn, response):
    sql = '''SELECT id FROM Responses WHERE response = ?'''
    cur = conn.cursor()
    cur.execute(sql, [str(response)])
    results = cur.fetchall()
    return len(results) > 0


def add_response(conn, response):
    sql = '''INSERT INTO Responses(response) VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql, [str(response)])
    conn.commit()


def delete_response(conn, response):
    sql = '''DELETE FROM Responses WHERE response = ?'''
    cur = conn.cursor()
    cur.execute(sql, [str(response)])
    conn.commit()


def get_all_responses(conn):
    sql = '''SELECT response FROM Responses'''
    cur = conn.cursor()
    cur.row_factory = lambda cursor, row: row[0]
    cur.execute(sql)
    results = cur.fetchall()
    return results


def add_admin(conn, user_id):
    sql = '''INSERT INTO Admins(user_id) VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql, [str(user_id)])
    conn.commit()


def is_admin(conn, user_id):
    sql = '''SELECT id FROM Admins WHERE user_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, [str(user_id)])
    results = cur.fetchall()
    return len(results) > 0


def delete_admin(conn, user_id):
    sql = '''DELETE FROM Admins WHERE user_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, [str(user_id)])
    conn.commit()

