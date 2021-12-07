from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Unread E-mail')

body = ttk.Frame(root, padding=10)
body.grid()

buttons = ttk.Frame(root, padding=10)
buttons.grid()

ttk.Label(body, text='From: Autumn').grid(row=0)
ttk.Label(body, text="You're cute!").grid(row=1)
ttk.Button(buttons, text='Remind me later').grid(column=0, row=0)
ttk.Button(buttons, text='Yes').grid(column=1, row=0)
ttk.Button(buttons, text='No').grid(column=2,row=0)

root.mainloop()