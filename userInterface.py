import tkinter as tk
from tkinter import *
from tkinter import ttk
import messenger

root = Tk()
root.title("MessengerApp")

frm = ttk.Frame(root, padding=10)
frm.grid()

username = None
password = None

def clear_screen(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def title_screen():
    clear_screen(frm)
    ttk.Label(frm, text="Messenger App").grid(column=1,row=0)
    ttk.Button(frm, text="Login", command=login_screen).grid(column=0,row=1)
    ttk.Button(frm, text="Sign up", command=newAcc_screen).grid(column=1, row=1)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=3, row=1)
    root.mainloop()


def login_screen(error_code=0):
    '''
    :param error_code: what error occured during this process. 0- no error
    -1 - password error
    -2 - username error
    :return:
    '''
    clear_screen(frm)
    messages={'0':'Please log in','-1':'password is incorrect', '-2':'There is no user with this username'}

    ttk.Button(frm, text="Back", command=title_screen).grid(column=0,row=0)
    ttk.Label(frm, text=messages[str(error_code)]).grid(column=1,row=0)

    def get_username():
        global username
        global password
        username = usernme.get()
        password = passwrd.get()
        error_code = messenger.check_login(username, password)
        if error_code>=0:
            signedIn_screen()
        else:
            login_screen(error_code)
            username = None
            password = None

    ttk.Label(frm, text="Username").grid(column=0, row=1)
    usernme = Entry(frm)
    usernme.grid(column=1, row=1)

    ttk.Label(frm, text="Password").grid(column=0, row=2)
    passwrd = Entry(frm)
    passwrd.grid(column=1, row=2)
    ttk.Button(frm, text="Login", command=get_username).grid(column=1, row=3)

    root.mainloop()


def newAcc_screen(error_code=0):
    '''

    :param error_code: 0 - no error
    -1 taken username
    -2 passwords do not match
    -3 unknown error
    1 account created
    :return:
    '''
    clear_screen(frm)
    message = {'1':"Account created successfully",
               '0':"Welcome. Please register with a username and password",
               '-1':"This username has been taken",
               '-2':"Passwords do not match or are empty",
               '-3':"A SQL error occured please try again."}
    ttk.Button(frm, text="Back", command=title_screen).grid(column=0,row=0)
    ttk.Label(frm, text=message[str(error_code)]).grid(column=1,row=0)

    def get_account():
        u = username.get()
        p = password.get()
        p2 = password2.get()
        if p != p2 or p == '':
            newAcc_screen(error_code=-2)
        error_code = messenger.create_login(u, p)

        newAcc_screen(error_code)

    ttk.Label(frm, text="Username").grid(column=0, row=1)
    username = Entry(frm)
    username.grid(column=1, row=1)

    ttk.Label(frm, text="Password").grid(column=0, row=2)
    password = Entry(frm)
    password.grid(column=1, row=2)

    ttk.Label(frm, text="Confirm your password").grid(column=0, row=3)
    password2 = Entry(frm)
    password2.grid(column=1, row=3)

    ttk.Button(frm, text="Sign up", command=get_account).grid(column=1, row=4)

    root.mainloop()


def open_chat(recipient, error=0):
    clear_screen(frm)

    def message():
        msg = text.get()
        messenger.send_dm(username, recipient, msg)
        open_chat(recipient)

    ttk.Button(frm, text='Back', command=signedIn_screen).grid(column=0, row=0)
    text = ttk.Entry(frm,width=50)
    text.grid(column=1, row=0)
    ttk.Button(frm, text='Send', command=message).grid(column=2, row=0)
    ttk.Label(frm,text=recipient).grid(column=3,row=0)

    msg = messenger.get_dms_from(username, recipient)
    for i in range(len(msg)):
        ttk.Label(frm, text=msg[i],wraplength=300).grid(column=1, row=i+1, sticky=tk.W)


def channel_screen(channel_name, error=0):
    clear_screen(frm)

    def message():
        msg = text.get()
        messenger.send_channel_message(channel_name, username, msg)
        channel_screen(channel_name)

    ttk.Button(frm, text='Back', command=signedIn_screen).grid(column=0, row=0)
    text = ttk.Entry(frm,width=50)
    text.grid(column=1, row=0)
    ttk.Button(frm, text='Send', command=message).grid(column=2, row=0)
    ttk.Label(frm,text=channel_name).grid(column=3,row=0)

    msg = messenger.get_messages_in(channel_name)
    for i in range(len(msg)):
        ttk.Label(frm, text=msg[i],wraplength=300).grid(column=1, row=i+1, sticky=tk.W)


def signedIn_screen(errorcode=0, suberror=0):
    clear_screen(frm)

    def logout():
        global username, password
        username = None
        password = None
        login_screen()

    def open_dm():
        signedIn_screen(1)

    def join_channel():
        signedIn_screen(2)

    def create_channel():
        signedIn_screen(3)

    def show_user_channels():
        global username
        button_dict = {}
        channels = messenger.get_user_channels(username)
        if len(channels) > 0:
            # Create Multiple Buttons with different commands

            for i in range(len(channels)):
                def open_channel(chan=channels[i]):
                    channel_screen(chan)
                button_dict[channels[i]] = ttk.Button(frm, text=channels[i],command=open_channel).grid(column=1, row=i+4)

    def cancel():
        signedIn_screen(0)

    ttk.Button(frm, text='Logout', command=logout).grid(column=0, row=0)

    ttk.Label(frm, text='Chats').grid(column=1, row=0)
    ttk.Button(frm, text='DM User', command=open_dm).grid(column=1, row=1)
    ttk.Button(frm, text='Join Channel', command=join_channel).grid(column=1, row=2)
    ttk.Button(frm, text='Create Channel', command=create_channel).grid(column=1,row=3)

    show_user_channels()

    if errorcode == 1:
        def new_dm():
            r = user_select.get()
            open_chat(r)
        user_select = Entry(frm)
        user_select.grid(column=2, row=1)
        ttk.Button(frm, text='Create', command=new_dm).grid(column=3, row=1)
        ttk.Button(frm, text='Cancel', command=cancel).grid(column=0,row=1)
    elif errorcode == 2:
        def join_chan():
            c = channel.get()
            suberror = messenger.join_channel(c, username)
            signedIn_screen(errorcode, suberror)

        channel = Entry(frm)
        channel.grid(column=2, row=2)
        ttk.Button(frm, text='Join', command=join_chan).grid(column=3, row=2)
        ttk.Button(frm, text='Cancel',command=cancel).grid(column=0, row=2)
    elif errorcode == 3:
        def new_channel():
            n = name.get()
            suberror = messenger.create_channel(name=n, creator_name=username)
            signedIn_screen(errorcode, suberror)

        name = Entry(frm)
        name.grid(column=2, row=3)
        ttk.Button(frm, text='Create', command=new_channel).grid(column=3, row=3)
        ttk.Button(frm, text='Cancel', command=cancel).grid(column=0, row=3)
        if suberror == -1:
            ttk.Label(frm, text="Channel Exists").grid(column=2, row=2)


if __name__ == '__main__':
    title_screen()
