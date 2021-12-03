from tkinter import *
from tkinter import messagebox

ws = Tk()
ws.title('pythonguides')
ws.geometry('250x200')

def usrnm(name):
    name = name_Tf.get()
    print(name)


def getpass(passw):
    passw = passw_Tf.get()
    print(passw)

Label(ws, text='Enter Name & hit Enter Key').pack(pady=20)
name_Tf = Entry(ws)
name_Tf.bind('<Return>', usrnm)
name_Tf.pack()

ws.mainloop()