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
            cursor.execute('''insert into accounts (username, password) values (%s, %s)''',
                           (login, password))

        except mysql.connector.Error as er:
            print('SQL error: ', er)
            return -3
        conn.commit()
        return 1
    else:
        return -1


def send_dm(sender, password, recipient, message):
    '''

    :param sender:
    :param password:
    :param recipient:
    :return: returns a
    '''
    global conn
    cursor = conn.cursor()
    #find sender info and confirm details
    try:
        cursor.execute('''select id, password from accounts where username = %s''',(sender,))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3
    rows = cursor.fetchall()

    # failed sender validation.
    if len(rows)==0 or rows[0][1] != password:
        return -2

    sender_id = rows[0][0]

    #find recipient
    try:
        cursor.execute('''select id from accounts where username=recipient''', (recipient,))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3
    rows = cursor.fetchall()

    if len(rows)==0:
        #recipient doesn't exist
        return -1
    recipient_id = rows[0][0]

    #is sender or recipient blocked
    try:
        cursor.execute('''select * from blocks where blocks where blocked_by=%d or blocked_by=%d''',
                       (sender_id,recipient_id))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3

    if len(rows)!=0:
        return -4

    try:
        cursor.execute('''insert into direct_messages (sender, recipient, message) values (%d, %d, %s);''',
                       (sender_id, recipient_id, message))
        cursor.commit()
        return 0
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3


def get_messages_in(channel_name):
    global conn
    cursor = conn.cursor()

    messages = []

    try:
        cursor.execute('''select a.username, msg.content 
        from channel_messages msg join accounts a on msg.sender_id=a.id join channels c on c.channel_id=msg.channel_id 
        where c.channel_name=%s 
        order by msg.message_id;''',(channel_name,))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3

    rows = cursor.fetchall()
    for row in rows:
        display = str(row[0]) +  ' : ' +  str(row[1])
        messages.append(display)

    return messages





def send_channel_message(channel_name, username, content):
    global conn
    cursor = conn.cursor()

    try:
        cursor.execute('''select channel_id from channels where channel_name=%s;''', (channel_name,))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3
    rows = cursor.fetchall()
    if len(rows)==0:
        return -1
    channel_id = rows[0][0]

    try:
        cursor.execute('''select id from accounts where username=%s;''', (username,))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3
    rows = cursor.fetchall()
    if len(rows)==0:
        return -1
    user_id = rows[0][0]
    # get channel_id


    try:
        cursor.execute('''insert into channel_messages (channel_id, sender_id, content) values (%s, %s, %s);''', (channel_id, user_id, content))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3
    conn.commit()
    return 1






def create_channel(name, creator_name):
    global conn
    cursor=conn.cursor()
    try:
        cursor.execute('''select * from channels where channel_name=%s;''', (name,))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3

    rows = cursor.fetchall()
    if len(rows) != 0:
        # channel exists
        return -1

    try:
        cursor.execute('''insert into channels (channel_name) values (%s);''', (name,))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3

    conn.commit()
    join_channel(name, creator_name)
    return 1


def join_channel(channel_name, username):
    global conn
    cursor = conn.cursor()
    try:
        cursor.execute('''select channel_id from channels where channel_name = %s;''', (channel_name,))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3
    rows = cursor.fetchall()

    #channel does not exist
    if len(rows) == 0:
        return -1

    channel_id = rows[0][0]

    try:
        # find creator id
        cursor.execute('''select id from accounts where username=%s;''', (username,))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3
    rows = cursor.fetchall()

    user_id = rows[0][0]

    try:
        # make the creator a member of the new channel
        cursor.execute('''insert into channel_members (channel_id, member_id) values (%s, %s);''', (channel_id, user_id))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3
    conn.commit()
    return 1


def get_user_channels(username):
    global conn
    cursor = conn.cursor()
    #get userid
    user_id = 0
    try:
        cursor.execute('''select id from accounts a where a.username=%s;''', (username,))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return -3
    rows = cursor.fetchall()

    if len(rows)==0:
        return -1

    user_id = rows[0][0]

    try:
        cursor.execute('''select c.channel_name from channel_members cm join accounts a on cm.member_id=a.id join channels c on c.channel_id=cm.channel_id where a.id=%s;''',(user_id,))
    except mysql.connector.Error as er:
        print('SQL error: ', er)
        return []

    rows = cursor.fetchall()

    channels = []
    for i in range(len(rows)):
        channels.insert(i, rows[i][0])
    return channels






def change_password(login, password, newpassword):
    #Todo: add a password changer feature
    pass
