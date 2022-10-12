import os
from tkinter import *
from tkinter import messagebox, ttk

import awesometkinter as atk
import customtkinter
import cv2
import face_recognition
import numpy as np

from database import db
from functions import *



class HomePage:
    @handlererr
    def __init__(self, up):
        logger.info("HomePage class initiated")
        self.up = up
        self.up.state("zoomed")
        os.makedirs("employees", exist_ok=True)
        self.up.title("Home Page")
        self.hpage = Label(self.up, image=homebg, width=xsize, height=ysize)
        self.hpage.pack()
        style = ttk.Style()
        self.style = style
        style.theme_use("clam")
        self.up.protocol("WM_DELETE_WINDOW", Exit)
        self.menu = Menu(
            up,
            bg=atk.DEFAULT_COLOR,
            fg="black",
            activebackground="black",
            activeforeground="black",
            background="black",
            foreground="black",
            bd=0,
            font=("Poppins", 15),
        )
        self.up.config(menu=self.menu)
        self.file_menu = Menu(
            self.menu,
            background=atk.DEFAULT_COLOR,
            fg="black",
            activebackground="black",
            activeforeground="white",
        )

        self.tab = self.entry_table()
        self.logo_label()
        self.count_label_func()
        self.manage_panel()

    @handlererr
    def logo_label(self):
        logger.info("LOGO label initiated")
        self.logo = Label(self.hpage, bg="#6991C7")
        self.logo.configure(image=logopanel)
        self.logo.place(x=xsize / 2 - 250)
        self.tbox = Label(self.hpage, image=timepanel, bg="#6991C7", bd="0")
        self.tbox.place(x=xsize - 115)
        self.tm = Label(self.tbox, bg="#fff1eb", font=("Poppins", 12))
        self.tm.place(x=5, y=8)
        self.my_time()

    def count_label_func(self):
        logger.info("Count label function initiated")
        self.box = Label(self.hpage, image=countpanel, bg="#6991C7", bd="0")
        self.box.place(x=1, y=150)
        self.total_count_frame = Label(
            self.box, text=str(db.employeecount()), font=("Poppins", 30), bg="#00FFDD"
        )
        self.total_count_frame.place(x=80, y=98)
        self.present = Label(
            self.box,
            text=str(db.get_today_employee_count()),
            font=("Poppins", 30),
            bg="#5CDB8B",
        )
        self.present.place(x=274, y=98)
        self.R = db.employeecount() - db.get_today_employee_count()
        self.count_labels = Label(
            self.box, text=str(self.R), font=("Poppins", 30), bg="#F15757"
        )
        self.count_labels.place(x=459, y=98)
        return

    def manage_panel(self):
        logger.info("Manage label function initiated")
        self.mng1 = Label(self.hpage, image=managepanel, bg="#6991C7", bd="0")
        self.mng1.place(x=1, y=350)
        self.cam_start = customtkinter.CTkButton(
            self.mng1,
            command=self.camrecogniser,
            image=start,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.cam_start.place(x=47, y=33)
        self.manage_button = customtkinter.CTkButton(
            self.mng1,
            command=self.verifyadmin,
            image=manage,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.manage_button.place(x=236, y=33)
        self.exit_button = customtkinter.CTkButton(
            self.mng1,
            command=root.quit,
            image=exit1,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.exit_button.place(x=425, y=197)
        self.id_button = customtkinter.CTkButton(
            self.mng1,
            command=self.search_by_id,
            image=idsch,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.id_button.place(x=47, y=197)
        self.date_button = customtkinter.CTkButton(
            self.mng1,
            command=self.search_by_date,
            image=dtsch,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.date_button.place(x=236, y=197)
        return

    def my_time(self):
        time_string = strftime("%H:%M:%S %p \n %A \n %x")
        self.tm.config(text=time_string)
        self.tm.after(1000, self.my_time)

    def verifyadmin(self):
        self.openverify = Toplevel(self.up)
        self.openverify.title("Verify Yourself")
        logger.info("Verify admin initiated")
        self.openverify.geometry("345x169")
        self.openverify.resizable(False, False)
        self.openverifylb = Label(self.openverify, text="Enter Password", image=passlb)
        self.openverifylb.place(x=0, y=0)
        self.openverifyentry = Entry(
            self.openverifylb,
            font="-family {Poppins} -size 20",
            show="*",
            background="#BCCEE6",
            relief="flat",
            textvariable=verifyadmintxt,
        )
        self.openverifyentry.place(x=57, y=66, width=224, height=19)
        self.openverifybtn = Button(
            self.openverifylb,
            relief="flat",
            text="Verify",
            background="#A6BDDC",
            command=self.verifyadminbutton,
        )
        self.openverifybtn.place(x=132, y=113, width=62, height=20)

    def verifyadminbutton(self):
        if verifyadmintxt.get() == UPASS:
            self.openverifyentry.delete(0, END)
            self.openverify.destroy()
            self.openmainemployeeinfo()
        else:
            messagebox.showerror("Error", "Wrong Password")
            self.openverifyentry.delete(0, END)

    def openmainemployeeinfo(self):
        logger.info("Open main employee info function initiated")
        self.up.withdraw()
        self.mainemployeewindow = Toplevel()
        datasdict["camera"] = False
        self.mainemployeewindow.protocol("WM_DELETE_WINDOW", self.mainhome_back)
        self.mainemployeewindow.title("Employee Info")
        self.mainemployeewindow.state("zoomed")
        self.mainemployeewindow.resizable(False, False)
        self.mpage = Label(
            self.mainemployeewindow, image=homebg, width=xsize, height=ysize
        )
        self.mpage.pack()
        self.logo1 = Label(self.mpage, bg="#6991C7")
        self.logo1.configure(image=mnglogo)
        self.logo1.place(x=xsize / 2 - 250)
        self.mainempaddbtn = customtkinter.CTkButton(
            self.mpage,
            command=self.new_entry,
            image=empadd,
            width=50,
            height=50,
            text="",
            fg_color="#6991C7",
            bg_color="#6991C7",
        )
        self.mainempbckbtn = customtkinter.CTkButton(
            self.mpage,
            command=self.mainhome_back,
            image=backbtn,
            text="",
            width=50,
            height=50,
            fg_color="#6991C7",
            bg_color="#6991C7",
        )
        self.mainempbckbtn.place(x=0, y=0)
        self.mainempaddbtn.place(x=100, y=100)
        self.mainempupdbtn = customtkinter.CTkButton(
            self.mpage,
            command=self.checkforupdate,
            image=empupdate,
            width=25,
            height=25,
            text="",
            fg_color="#6991C7",
            bg_color="#6991C7",
        )
        self.mainempupdbtn.place(x=100, y=300)
        self.mainempdelbtn = customtkinter.CTkButton(
            self.mpage,
            command=self.deleteemployee,
            image=empdel,
            width=25,
            height=25,
            text="",
            fg_color="#6991C7",
            bg_color="#6991C7",
        )

        self.mainempdelbtn.place(x=100, y=500)
        self.opendbscroller = Scrollbar(self.mpage, orient=VERTICAL)
        self.opendbentry = Entry(self.mpage, textvariable=opendbvar)
        self.opendbentry.configure(
            font="-family {Poppins} -size 15",
            relief="solid",
            bg="#6991C7",
            highlightbackground="black",
        )
        self.opendbentry.place(x=xsize / 2, y=90, width=xsize / 4, height=30)
        self.opendbsearch = customtkinter.CTkButton(
            self.mpage,
            text="",
            command=self.search_db,
            width=130,
            height=38,
            image=search,
            bg_color="#6991C7",
            fg_color="#6991C7",
        )
        self.opendbsearch.place(x=xsize / 2 + xsize / 4 + 25, y=86)
        self.refresh1 = customtkinter.CTkButton(
            self.mpage,
            text="",
            command=self.refresh1,
            width=130,
            height=38,
            image=refresh,
            bg_color="#6991C7",
            fg_color="#6991C7",
        )
        self.refresh1.place(x=xsize / 2 + xsize / 4 + 160, y=86)
        self.opendbtable = ttk.Treeview(
            self.mpage, yscrollcommand=self.opendbscroller.set
        )
        self.opendbtable.place(
            x=xsize / 2, y=130, width=xsize / 2 - 100, height=ysize - 200
        )
        self.opendbscroller.config(command=self.opendbtable.yview)
        self.opendbscroller.place(
            x=xsize / 2 + xsize / 2 - 100, y=130, width=20, height=ysize - 200
        )
        self.opendbtable.configure(columns=("SNO", "ID", "Name", "Position", "Profile"))
        self.opendbtable.heading("#0", text="SNO", anchor=W)
        self.opendbtable.heading("#1", text="ID", anchor=W)
        self.opendbtable.heading("#2", text="Name", anchor=W)
        self.opendbtable.heading("#3", text="Position", anchor=W)
        self.opendbtable.heading("#4", text="Profile", anchor=W)
        self.opendbtable.column("#0", minwidth=60, width=80)
        self.opendbtable.column("#1", minwidth=60, width=100)
        self.opendbtable.column("#2", minwidth=60, width=100)
        self.opendbtable.column("#3", minwidth=60, width=100)
        self.opendbtable.column("#4", minwidth=60, width=150)
        for x, y in enumerate(db.get_all_employee_info(), 1):
            self.opendbtable.insert("", "end", text=x, values=(y[0], y[1], y[2], y[3]))
        self.opendbtable.bind("<<TreeviewSelect>>", self.select)

    def refresh1(self):
        self.opendbtable.delete(*self.opendbtable.get_children())
        for x, y in enumerate(db.get_all_employee_info(), 1):
            self.opendbtable.insert("", "end", text=x, values=(y[0], y[1], y[2], y[3]))

    def mainhome_back(self):
        self.mainemployeewindow.destroy()
        self.up.deiconify()
        self.up.state("zoomed")
        self.logo_label()
        return

    def select(self, event):
        global selected_item
        selected_item = (
            self.opendbtable.item(self.opendbtable.focus())["values"] or None
        )
        return

    def deleteemployee(self):
        if selected_item:
            db.delete_employee(selected_item[0])
            logger.info("Employee %s deleted", selected_item[0])
            self.opendbtable.delete(self.opendbtable.selection())
            self.selected_item = None
            messagebox.showinfo("Success", "Employee deleted successfully")
        else:
            messagebox.showerror("Error", "Please select an employee")

    def checkforupdate(self):
        if selected_item:
            datasdict.update(
                {
                    "id": selected_item[0],
                    "name": selected_item[1],
                    "position": selected_item[2],
                    "profile": selected_item[3],
                }
            )
            self.updateemployee()
        else:
            messagebox.showerror("Error", "Please select an employee")

    # update employee
    def updateemployee(self):
        self.updatewindow = Toplevel(self.up)
        self.updatewindow.geometry("900x550")
        self.upbg = Label(self.updatewindow, image=newentry, width=900, height=550)
        self.upbg.pack()
        self.updatewindow.protocol("WM_DELETE_WINDOW", self.updateclose)
        self.updatewindow.title("Employee Update")
        self.updatewindow.resizable(0, 0)
        self.uplg = Label(self.updatewindow, bg="#009EFD")
        self.uplg.configure(image=updtlg)
        self.uplg.place(x=450, y=17)
        self.updateEID = Entry(self.updatewindow)
        self.updateEID.place(x=607, y=164, width=230, height=45)
        self.updateEID.configure(
            font="-family {Poppins} -size 20",
            relief="flat",
            textvariable=updateempid,
        )
        self.updateENAME = Entry(self.updatewindow)
        self.updateENAME.place(x=607, y=255, width=230, height=45)
        self.updateENAME.configure(
            font="-family {Poppins} -size 20",
            relief="flat",
            textvariable=updateename,
        )
        self.updateEPOSITION = Entry(self.updatewindow)
        self.updateEPOSITION.place(x=607, y=353, width=230, height=45)
        self.updateEPOSITION.configure(
            font="-family {Poppins} -size 20",
            relief="flat",
            textvariable=updateempostion,
        )
        self.updatesubmit = Button(self.updatewindow)
        self.updatesubmit.place(x=649, y=444, width=176, height=56)
        self.updatesubmit.configure(
            relief="flat",
            cursor="hand2",
            borderwidth="0",
            image=updt,
            command=self.on_emp_update,
            background="#009EFD",
        )
        self.updatecamlabel = Label(self.updatewindow, bg="black", borderwidth=3)
        self.updatecamlabel.place(x=46, y=80, width=346, height=356)
        self.updatecambutton = Button(
            self.updatewindow,
            image=chngimg,
            background="#009EFD",
            text="Change Image",
            relief="flat",
            command=self.update_open_camera,
        )
        self.updatecambutton.place(x=39, y=488, width=364, height=46)
        self.updateEID.insert(0, datasdict["id"])
        self.updateENAME.insert(0, datasdict["name"])
        self.updateEPOSITION.insert(0, datasdict["position"])
        self.updatecamlabel.image = ImageTk.PhotoImage(IM.open(datasdict["profile"]))

    def on_emp_update(self):
        print(datasdict)
        print(updateempid.get(), updateename.get(), updateempostion.get())
        if (
            updateempid.get() == ""
            or updateename.get() == ""
            or updateempostion.get() == ""
        ):
            messagebox.showerror("Error", "Please fill all the fields")
        elif (
            updateempid.get() == str(datasdict["id"])
            and updateename.get() == datasdict["name"]
            and updateempostion.get() == datasdict["position"]
        ):
            messagebox.showerror("Error", "No changes made")
        if datasdict["camera"]:
            updatednewimage2 = IM.fromarray(self.updateempcam.read()[1])
            updatename = f"employees/{updateempid.get()}.jpg"
            updatednewimage2.save(updatename)
            db.update_employee_info(
                updateempid.get(),
                updateename.get(),
                updateempostion.get(),
                updatename,
            )
            logger.info("Employee %s updated", updateempid.get())
            messagebox.showinfo("Success", "Employee updated successfully")
        db.update_employee_info(
            updateempid.get(),
            updateename.get(),
            updateempostion.get(),
            datasdict["profile"],
        )
        logger.info("Employee %s updated", updateempid.get())
        messagebox.showinfo("Success", "Employee updated successfully")
        return

    def updateclose(self):
        self.updateEID.delete(0, END)
        self.updateENAME.delete(0, END)
        self.updateEPOSITION.delete(0, END)
        datasdict.clear()
        datasdict["camera"] = False
        cv2.destroyAllWindows()
        self.updatewindow.destroy()

    def update_search(self):
        if not updatesearch.get():
            messagebox.showerror("Error", "Please enter an ID")
            return
        elif not db.check_employee(updatesearch.get()):
            messagebox.showerror("Error", "Employee not found")
            self.updateemployeefindentry.delete(0, END)
            return
        updatedatas = db.getemployee(updatesearch.get())
        messagebox.showinfo("Success", "Employee found")
        self.updateemployeefindentry.delete(0, END)
        self.updateEID.delete(0, END)
        self.updateENAME.delete(0, END)
        self.updateEPOSITION.delete(0, END)
        datasdict.update(
            {"id": updatedatas[0], "name": updatedatas[1], "position": updatedatas[2]}
        )
        self.updateEID.insert(0, updatedatas[0])
        self.updateENAME.insert(0, updatedatas[1])
        self.updateEPOSITION.insert(0, updatedatas[2])
        newupdatedimage = ImageTk.PhotoImage(IM.open(updatedatas[3]))
        self.updatecameraopen = Button(
            self.updatewindow, text="Open Camera", command=self.update_open_camera
        )
        self.updatecameraopen.place(x=50, y=420, width=230, height=45)
        self.updatecamlabel["image"] = newupdatedimage
        return

    def update_open_camera(self):
        cv2.destroyAllWindows()
        datasdict["camera"] = True
        self.updateempcam = cv2.VideoCapture(0)
        while True:
            updateimg1 = self.updateempcam.read()[1]
            gray = cv2.cvtColor(updateimg1, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(updateimg1, (x, y), (x + w, y + h), (255, 0, 0), 2)
            updateimg = ImageTk.PhotoImage(IM.fromarray(updateimg1))
            self.updatecamlabel["image"] = updateimg
            self.updatewindow.update()

    @handlererr
    def entry_table(self):
        logger.info("Entry table function initiated")
        self.scroolbarentryy = Scrollbar(self.up, orient=VERTICAL)
        self.style.configure(
            "Treeview",
            background="#2a2d2e",
            foreground="white",
            rowheight=25,
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0,
        )
        self.entrybar = Entry(self.up, bd="2")
        self.entrybar.place(x=xsize / 2, y=90, width=xsize / 4, height=30)
        self.entrybar.configure(
            font="-family {Poppins} -size 15",
            relief="solid",
            textvariable=tdy_,
            bg="#6991C7",
            highlightbackground="black",
        )
        self.style.map("Treeview", background=[("selected", "#22559b")])
        self.style.configure(
            "Treeview.Heading", background="#565b5e", foreground="white", relief="flat"
        )

        self.entsearch = customtkinter.CTkButton(
            self.up,
            text="",
            command=self.id_search,
            width=130,
            height=38,
            image=search,
            bg_color="#6991C7",
            fg_color="#6991C7",
        )
        self.entsearch.place(x=xsize / 2 + xsize / 4 + 25, y=86)
        self.refresh = customtkinter.CTkButton(
            self.up,
            text="",
            command=self.refresh,
            width=130,
            height=38,
            image=refresh,
            bg_color="#6991C7",
            fg_color="#6991C7",
        )
        self.refresh.place(x=xsize / 2 + xsize / 4 + 160, y=86)

        self.style.map("Treeview.Heading", background=[("active", "#3484F0")])
        self.tree = ttk.Treeview(
            self.up, yscrollcommand=self.scroolbarentryy.set, style="Treeview"
        )
        self.tree.place(x=xsize / 2, y=130, width=xsize / 2 - 100, height=ysize - 200)
        self.scroolbarentryy.place(
            x=xsize / 2 + xsize / 2 - 100, y=130, width=20, height=ysize - 200
        )
        self.scroolbarentryy.config(command=self.tree.yview)
        self.tree.configure(columns=("ID", "Name", "Date", "Entry Time", "Exit Time"))
        self.tree.heading("#0", text="ID", anchor=W)
        self.tree.heading("#1", text="Name", anchor=W)
        self.tree.heading("#2", text="Date", anchor=W)
        self.tree.heading("#3", text="Entry Time", anchor=W)
        self.tree.heading("#4", text="Exit Time", anchor=W)
        self.tree.column("#0", minwidth=60, width=120)
        self.tree.column("#1", minwidth=60, width=120)
        self.tree.column("#2", minwidth=60, width=120)
        self.tree.column("#3", minwidth=60, width=120)
        self.tree.column("#4", minwidth=60, width=120)
        daterr = dateEncodedTable(today()[0])
        for x in db.get_entry_by_date(daterr):
            self.tree.insert("", "end", text=x[0], values=(x[1], x[2], x[3], x[4]))

    def id_search(self):
        id__ = tdy_.get()
        if not id__:
            messagebox.showerror("Error", "Please enter a ID")
            return
        elif not db.check_employee(id__):
            print(db.check_employee(id__))
            messagebox.showerror("Error", "No entry found")
            return
        self.tree.delete(*self.tree.get_children())
        for val in db.get_entry_by_id(id__):
            self.tree.insert(
                "", "end", text=val[0], values=(val[1], val[2], val[3], val[4])
            )

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        daterr = dateEncodedTable(today()[0])
        for x in db.get_entry_by_date(daterr):
            self.tree.insert("", "end", text=x[0], values=(x[1], x[2], x[3], x[4]))
        self.up.state("zoomed")
        self.logo_label()
        self.count_label_func()
        self.manage_panel()

    @handlererr
    def search_db(self):
        opendbtxt = opendbvar.get()
        if not opendbtxt:
            return messagebox.showerror("Error", "Please enter a Input")
        elif name_match(opendbtxt):
            if position_match(opendbtxt):
                self.opendbtable.delete(*self.opendbtable.get_children())
                for x in db.get_employee_by_position(opendbtxt):
                    self.opendbtable.insert(
                        "", "end", text=x[0], values=(x[1], x[2], x[3])
                    )
            return messagebox.showerror("Error", "Please enter a valid Input")
        elif int_match(opendbtxt):
            if not db.check_employee(opendbtxt):
                return messagebox.showerror("Error", "Employee not found")
            self.opendbtable.delete(*self.opendbtable.get_children())
            for x in db.get_employee_info_by_id(opendbtxt):
                self.opendbtable.insert("", "end", text=x[0], values=(x[1], x[2], x[3]))
        messagebox.showinfo("Success", "Employee found")

    def opendatabaseExit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.opendbentry.delete(0, END)
            self.opendatabase.destroy()
            self.up.deiconify()

    @handlererr
    def search_by_date(self):
        self.dateWindow = Toplevel()
        self.dateWindow.title("Search by DATE")
        self.dateWindow.geometry("900x550")
        self.dateWindow.configure(bg="black")
        self.dateWindow.resizable(False, False)
        self._dateWindow = Label(self.dateWindow, image=searchbg)
        self._dateWindow.place(x=0, y=0)

        self.date__entry = Entry(self._dateWindow)
        self.date__entry.place(x=59, y=149, width=188, height=27)
        self.date__entry.configure(
            font="-family {Poppins} -size 20",
            relief="flat",
            textvariable=date_,
            bg="#66A4DA",
        )
        self.scroolbardatey = Scrollbar(self._dateWindow, orient=VERTICAL)
        self.tree2 = ttk.Treeview(
            self._dateWindow, yscrollcommand=self.scroolbardatey.set
        )
        self.tree2.place(x=300, y=35, width=546, height=456)
        self.scroolbardatey.place(x=845, y=35, width=20, height=460)
        self.scroolbardatey.config(command=self.tree2.yview)
        self.tree2.configure(columns=("ID", "Name", "Date", "Entry Time", "Exit Time"))
        self.tree2.heading("#0", text="ID", anchor=W)
        self.tree2.heading("#1", text="Name", anchor=W)
        self.tree2.heading("#2", text="Date", anchor=W)
        self.tree2.heading("#3", text="Entry Time", anchor=W)
        self.tree2.heading("#4", text="Exit Time", anchor=W)
        self.tree2.column("#0", minwidth=60, width=100)
        self.tree2.column("#1", minwidth=60, width=100)
        self.tree2.column("#2", minwidth=60, width=100)
        self.tree2.column("#3", minwidth=60, width=100)
        self.tree2.column("#4", minwidth=60, width=100)
        self.date_button = customtkinter.CTkButton(
            master=self._dateWindow,
            width=120,
            height=32,
            border_width=2,
            fg_color=("#66A4DA"),
            text="Search",
            bg="#66A4DA",
            command=self.on_date_search,
        )
        self.date_button.place(x=85, y=207)
        return

    @handlererr
    def on_date_search(self):
        date__ = date_.get()
        if not date__:
            messagebox.showerror("Error", "Please enter a date")
            return
        dat__ = dateEncodedTable(date__)
        if not datematch(date__):
            return messagebox.showerror("Error", "Please enter a valid date")
        if not db.validate_date(dat__):
            messagebox.showerror("Error", "No entry found")
            return
        self.tree2.delete(*self.tree2.get_children())
        for val in db.get_entry_by_date(dat__):
            self.tree2.insert(
                "", "end", text=val[0], values=(val[1], val[2], val[3], val[4])
            )

    @handlererr
    def search_by_id(self):
        self.idWindow = Toplevel()
        self.idWindow.title("Search by ID")
        self.idWindow.geometry("900x550")
        self.idWindow.configure(bg="black")
        self.idWindow.resizable(False, False)
        self._idWindow = Label(self.idWindow, image=searchbg)
        self._idWindow.place(x=0, y=0)
        self.identry = Entry(self._idWindow)
        self.identry.place(x=59, y=149, width=188, height=27)
        self.identry.configure(
            font="-family {Poppins} -size 20",
            relief="flat",
            textvariable=Id_,
            bg="#66A4DA",
        )
        self.scroolbaridy = Scrollbar(self._idWindow, orient=VERTICAL)
        self.tree3 = ttk.Treeview(self._idWindow, yscrollcommand=self.scroolbaridy.set)
        self.tree3.place(x=300, y=35, width=546, height=456)
        self.scroolbaridy.place(x=845, y=35, width=20, height=460)
        self.scroolbaridy.config(command=self.tree.yview)
        self.tree3.configure(columns=("ID", "Name", "Date", "Entry Time", "Exit Time"))
        self.tree3.heading("#0", text="ID", anchor=W)
        self.tree3.heading("#1", text="Name", anchor=W)
        self.tree3.heading("#2", text="Date", anchor=W)
        self.tree3.heading("#3", text="Entry Time", anchor=W)
        self.tree3.heading("#4", text="Exit Time", anchor=W)
        self.tree3.column("#0", minwidth=60, width=100)
        self.tree3.column("#1", minwidth=60, width=100)
        self.tree3.column("#2", minwidth=60, width=100)
        self.tree3.column("#3", minwidth=60, width=100)
        self.tree3.column("#4", minwidth=60, width=100)
        self.id_button = customtkinter.CTkButton(
            master=self._idWindow,
            width=120,
            height=32,
            border_width=2,
            fg_color=("#66A4DA"),
            text="Search",
            bg="#66A4DA",
            command=self.on_id_search,
        )
        self.id_button.place(x=85, y=207)
        return

    @handlererr
    def on_id_search(self):
        id__ = Id_.get()
        if not id__:
            messagebox.showerror("Error", "Please enter a ID")
            return
        elif not db.check_employee(id__):
            self.tree3.delete(*self.tree3.get_children())
            messagebox.showerror("Error", "No entry found")
            return
        self.tree3.delete(*self.tree3.get_children())
        for val in db.search_data_by_id(id__):
            self.tree3.insert(
                "", "end", text=val[0], values=(val[1], val[2], val[3], val[4])
            )

    @handlererr
    def today_entry(self):
        self.tree.delete(*self.tree.get_children())
        tddate = dateEncodedTable(today()[0])
        for x in db.get_entry_by_date(tddate):
            self.tree.insert("", "end", text=x[0], values=(x[1], x[2], x[3], x[4]))

    # new Employee
    @handlererr
    def new_entry(self):
        self.window = Toplevel(self.up)
        self.window.geometry("900x550")
        self.bg = Label(self.window, image=newentry, width=900, height=550)
        self.bg.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.title("New Employee Entry")
        self.window.resizable(0, 0)
        if not self.camera_not_found():
            messagebox.showerror("Error", "Camera not found")
            return self.window.destroy()
        cv2.destroyAllWindows()
        self.nwlg = Label(self.window, bg="#009EFD")
        self.nwlg.configure(image=addlg)
        self.nwlg.place(x=450, y=17)
        self.EID = Entry(self.window)
        self.EID.place(x=607, y=164, width=230, height=45)
        self.EID.configure(
            font="-family {Poppins} -size 20",
            relief="flat",
            textvariable=eid,
        )
        self.ENAME = Entry(self.window)
        self.ENAME.place(x=607, y=255, width=230, height=45)
        self.ENAME.configure(
            font="-family {Poppins} -size 20",
            relief="flat",
            textvariable=ename,
        )
        self.EPOSITION = Entry(self.window)
        self.EPOSITION.place(x=607, y=353, width=230, height=45)
        self.EPOSITION.configure(
            font="-family {Poppins} -size 20",
            relief="flat",
            textvariable=eposition,
        )
        self.submit = Button(self.window)
        self.submit.place(x=649, y=444, width=176, height=56)
        self.submit.configure(
            relief="flat",
            cursor="hand2",
            borderwidth="0",
            image=add,
            background="#009EFD",
            command=self.on_new_employee,
        )
        self.camlabel = Label(self.window, bg="black", borderwidth=3)
        self.camlabel.place(x=46, y=80, width=346, height=356)
        self.cam = cv2.VideoCapture(0)
        while True:
            img1 = self.cam.read()[1]
            gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 0, 0), 2)
            img = ImageTk.PhotoImage(IM.fromarray(img1))
            self.camlabel["image"] = img
            self.window.update()

    @handlererr
    def close(self):
        self.cam.release()
        cv2.destroyAllWindows()
        self.window.destroy()
        self.count_label_func()
        self.manage_panel()
        self.logo_label()

    @handlererr
    def employee_arrived(self, eid):
        data = db.getemployee(eid)
        if dat := db.get_entry_time(eid, today()[0]):
            Rtime = time() - dat
            if Rtime < 7200:
                logger.info(f"{data[1]} already arrived at {today()[1]}")
                return self.empid.config(text=f"{eid} - {data[1]} already arrived ")
            timer = db.get_emp_entry_time(eid, today()[0])
            db.employee_entry(
                eid=eid,
                ename=data[1],
                date=today()[0],
                entry=timer,
                leave=today()[1],
                Time=time(),
            )
            self.empid.config(text=f"{eid} Left")
            logger.info(f"{eid} Left")

        db.employee_entry(
            eid=eid, ename=data[1], date=today()[0], entry=today()[1], Time=time()
        )
        logger.info(f"{eid} arrived")
        self.empid.config(text=f"{eid} is arrived")
        self.today_entry()
        self.count_label_func()

    @handlererr
    def camrecogniser(self):
        self.window = Toplevel()
        self.window.state("zoomed")
        cv2.destroyAllWindows()
        self.cam = cv2.VideoCapture(0)
        self.window.geometry(f"{xsize}x{ysize}")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.title("Recogniser")

        self.camrbg = Label(self.window, image=cambg, width=xsize, height=ysize)
        self.camrbg.pack()
        self.exit_ = customtkinter.CTkButton(
            self.camrbg,
            command=self.close,
            image=stp,
            text="",
            fg_color="#00C6FB",
            bg_color="#00C6FB",
        )
        self.exit_.place(x=xsize / 2 - 75, y=ysize / 2 + 150)

        self.camlabel = Label(self.camrbg, width=600, height=470)
        self.camlabel.place(x=xsize / 2 - 250, y=ysize / 2 - 350)
        self.empid = Entry(self.camrbg)
        self.empid = Label(self.camrbg, font=("Poppins", 30), bg="#00FFDD")
        self.empid.place(x=xsize / 2 - 250, y=10, width=600, height=60)
        known_face_encodings = []
        known_face_names = []
        for image in os.listdir("./employees"):
            face = face_recognition.load_image_file(f"./employees/{image}")
            face_encoding = face_recognition.face_encodings(face)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(image.split(".")[0])
        face_locations = []
        face_encodings = []
        face_names = []

        process_this_frame = True
        while True:
            img1 = self.cam.read()[1]
            if process_this_frame:
                small_frame = cv2.resize(img1, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations
                )
                face_names = []
                self.empid.config(text="No Face detected")

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        known_face_encodings,
                        face_encoding,
                    )
                    name = "Unknown"
                    self.empid.config(text="Unknown Face detected")
                    face_distances = face_recognition.face_distance(
                        known_face_encodings,
                        face_encoding,
                    )
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        logger.info("Employee %s detected", name)
                        self.employee_arrived(name)
                    face_names.append(name)
            process_this_frame = not process_this_frame
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(img1, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(
                    img1, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
                )
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(
                    img1, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
                )
                break
            img = ImageTk.PhotoImage(IM.fromarray(img1))
            self.camlabel["image"] = img
            self.window.update()

    @handlererr
    def home_back(self):
        self.frame.pack_forget()

    @handlererr
    def clear_entry(self):
        self.EID.delete(0, END)
        self.ENAME.delete(0, END)
        self.EPOSITION.delete(0, END)
        return

    @handlererr
    def on_new_employee(self):
        Eid = eid.get()
        Ename = ename.get()
        Eposition = eposition.get()
        name = f"employees/{Eid}.jpg"
        image = IM.fromarray(self.cam.read()[1])
        image.save(name)
        if db.check_employee(Eid):
            messagebox.showinfo("Error", "Employee already exists")
            return self.clear_entry()
        value = db.newEmployee(Eid, Ename, Eposition, name)
        if value == "ERROR":
            messagebox.showerror("Error", "Invalid Data Entry")
            return self.clear_entry()
        self.clear_entry()
        messagebox.showinfo("Success", "Employee added successfully")
        return

    def camera_not_found(self):
        try:
            cv2.VideoCapture(0)
            return True
        except BaseException:
            return False
