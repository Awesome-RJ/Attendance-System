from tkinter import *
from tkinter import messagebox

from functions import *
from homepage import HomePage


def on_login_click():
    username = user.get()
    pwd = password.get()
    if username.lower() == UNAME and pwd.lower() == UPASS:
        messagebox.showinfo("Success", "You have successfully logged in")
        page.userEntry.delete(0, END)
        page.pwdEntry.delete(0, END)
        root.withdraw()
        homeup = Toplevel()
        HomePage(homeup)
    else:
        messagebox.showerror("Error", "Incorrect username or password.")
        page.userEntry.delete(0, END)
        page.pwdEntry.delete(0, END)


class LoginPage:
    def __init__(self, main):
        self.main = main
        self.label = Label(self.main, image=loginbg, width=xsize, height=ysize)
        self.label.pack()
        self.loginimage2 = Label(self.main, image=loginbox, bg="#66A6FF")
        self.loginimage2.place(x=xsize - 700, y=ysize - 700)
        self.userEntry = Entry(self.loginimage2)
        self.userEntry.place(x=154, y=194, width=320, height=52)
        self.userEntry.configure(
            font="-family {Poppins} -size 25",
            relief="flat",
            textvariable=user,
        )
        self.pwdEntry = Entry(self.loginimage2)
        self.pwdEntry.place(x=153, y=315, width=320, height=52)
        self.pwdEntry.configure(
            font="-family {Poppins} -size 25",
            relief="flat",
            show="*",
            textvariable=password,
        )
        self.button1 = Button(self.loginimage2)
        self.button1.place(x=228, y=439)
        self.button1.configure(
            relief="flat",
            cursor="hand2",
            bg="#B8CEFE",
            borderwidth="0",
            image=login,
            command=on_login_click,
        )


page = LoginPage(root)
root.mainloop()
