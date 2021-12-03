import mysql.connector
import sys
import os

conn = mysql.connector.connect(user='appaccount',
                               password='anInsecurePassword', host='localhost',
                               database='echo-app')


def check_login(login, password):
    global conn
    ''' Checks if login exists in the DB and returns login_id/-1/-2'''
    cursor = conn.cursor()

    try:
        cursor.execute(''' select id, password from accounts where username = %s; ''', (login,))
    except mysql.connector.Error as er:
            print('SQL error: ', er)
            return -3

    rows = cursor.fetchall()
    #login does not exist
    if len(rows) == 0:
        return -1
    #incorrect password
    elif rows[0][1] != password:
        return -2

    return rows[0][0]


def create_login(login, password):
    global conn
    cursor = conn.cursor()
    try:
        cursor.execute('''select id from accounts a where a.username = %s;''', (login,))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return

    rows = cursor.fetchall()
    # login does not exist
    if len(rows) == 0:
        try:
            cursor.execute('''select id from accounts;''')
        except mysql.connector.Error as er:
            print('SQL error: ', er)
            return -3

        rows = cursor.fetchall()
        try:
            cursor.execute('''insert into accounts (username, password) values (%s, %s)''',
                           (login, password))

        except mysql.connector.Error as er:
            print('SQL error: ', er)
            return -3
        conn.commit()
        return 1
    else:
        return -1
