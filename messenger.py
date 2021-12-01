import mysql.connector
import sys

def check_login(conn, login):
    ''' Checks if login exists in the DB and returns login_id/-1'''
    cursor = conn.cursor()

    try:
        cursor.execute(''' select id from accounts where login = %s; ''', (login,))
    except mysql.connector.Error as er:
            print('SQL error: ', er)
            sys.exit()

    rows = cursor.fetchall()

    if len(rows) == 0:
        print('Login does not exist')
        return -1

    return rows[0][0]
    
# connection
conn = mysql.connector.connect(user='appaccount', password='csci2052021', host='AU20012', database='messenger_db')

# ask the user to enter login
login = input('Enter your login: ')
login_id = check_login(conn, login)
if login_id == -1:
    sys.exit()

while True:
    print('1: Read\t2: Send\t3:Quit')
    option = int(input('Select the option: '))
    if option == 3:
        sys.exit()
    elif option == 1:
        cursor = conn.cursor()
        try:
            cursor.execute(''' select a2.login, m.message from accounts a1 join messages m on a1.id = m.dst
                                    join accounts a2 on m.src=a2.id where a1.login = %s order by m.id desc''', (login,))
        except mysql.connector.Error as er:
            print('SQL error: ', er)
            sys.exit()

        rows = cursor.fetchall()
        for row in rows:
            print(row)
    elif option == 2:
        destination = input('Enter destination login: ')
        destination_id = check_login(conn, destination)
        if destination_id == -1:
            print('Receiver does not exist')
            continue
        message = input('Enter the message:' )
        cursor = conn.cursor()
        try:
            cursor.execute(''' insert into messages (id, src, dst, message) select max(id) + 1, %s,
                                               %s, %s from messages''', (login_id, destination_id, message))
        except mysql.connector.Error as er:
            print('SQL error: ', er)
            sys.exit()

        conn.commit()












    

        
        
    
