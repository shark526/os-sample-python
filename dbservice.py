# -*- coding: utf-8 -*-
'''create DB, and AUD oprations'''
import os
import sqlite3
from sqlite3 import Error
import time


DB_FILE_PATH = "wechat_server.db"
# id integer PRIMARY KEY AUTOINCREMENT,
SQL_CREATE_USER_TABLE = """ CREATE TABLE IF NOT EXISTS user_info (
                                user_id text PRIMARY KEY ,
                                location text,
                                city text,
                                query_type text,
                                update_time text,
                                query_time text,
                                query_result text
                            ); """

SQL_UPDATE_USER_INFO = """INSERT OR REPLACE INTO user_info (user_id, location, city, query_type,update_time, query_time, query_result) VALUES (?,?,?,?,?,?,?);"""
SQL_SELECT_USER_INFO = """SELECT * FROM user_info WHERE user_id=?;"""
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        connct = sqlite3.connect(db_file)
        # print sqlite3.version
        return connct
    except Error as ex:
        print ex
    return None

def exec_sql(conn, sql, prameters=None):
    """ execute sql script """
    try:
        c = conn.cursor()
        execresult = None
        if prameters:
            execresult = c.execute(sql, prameters)
        else:
            execresult = c.execute(sql)
        conn.commit()
        #return execresult
        return c.fetchall()
    except Error as ex:
        print(ex)
    finally:
        {
            conn.close()
        }

def update_user_info(userinfo):
    """ update User info """
    conn = create_connection(DB_FILE_PATH)
    try:
        exec_sql(conn, SQL_UPDATE_USER_INFO, userinfo)
    except Error as e:
        print(e)

def get_user_info(userid):
    """ update User info """
    conn = create_connection(DB_FILE_PATH)
    try:
        return exec_sql(conn, SQL_SELECT_USER_INFO, userid)
    except Error as e:
        print(e)

def initial_db():
    conn = create_connection(DB_FILE_PATH)
    exec_sql(conn, SQL_CREATE_USER_TABLE)
    conn.close()

if __name__ == '__main__':
    #pass
    if not os.path.isfile(DB_FILE_PATH):
	initial_db()
    # userinfo = ("fkfuks211", "123.5,1354.3", "chengdu", "l","2017-09-04 11", time.strftime('%Y-%m-%d %H'), "88")
    # update_user_info(userinfo)
    # print "user fkfuks211 insert/update done"
    # curuserid = ("fkfuks211",)
    # query = get_user_info(curuserid) 
    # print "got %s records" % len(query)
    # print query 

