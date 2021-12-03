from tkinter import *
from tkinter import ttk
import messenger

root = Tk()
root.title("MessengerApp")

frm = ttk.Frame(root, padding=10)
frm.grid()


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
        u = username.get()
        p = password.get()
        error_code = messenger.check_login(u, p)
        if error_code>=0:
            signedIn_screen()
        else:
            login_screen(error_code)

    ttk.Label(frm, text="Username").grid(column=0, row=1)
    username = Entry(frm)
    username.grid(column=1, row=1)

    ttk.Label(frm, text="Password").grid(column=0, row=2)
    password = Entry(frm)
    password.grid(column=1, row=2)
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


def signedIn_screen(errorcode=0):
    clear_screen(frm)
    ttk.Label(frm, text='Chats').grid(column=0, row=0)
    ttk.Button(frm, text='DM User').grid(column=0,row=0)



if __name__ == '__main__':
    title_screen()
