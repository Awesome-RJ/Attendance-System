import os
from datetime import date
from tkinter import *
from tkinter import messagebox, ttk

import customtkinter
import cv2
import face_recognition
import numpy as np
import pandas as pd
from tkcalendar import DateEntry

from database import db
from functions import *


class HomePage:
    @handlererr
    def __init__(self, up):
        logger.info("HomePage class initiated")
        self.up = up
        self.up.state("zoomed")
        os.makedirs("employees", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        self.up.title("Home Page")
        self.hpage = Label(self.up, image=homebg, width=xsize, height=ysize)
        self.hpage.pack()
        style = ttk.Style()
        self.style = style
        style.theme_use("clam")
        self.up.protocol("WM_DELETE_WINDOW", Exit)
        self.tab = self.entry_table()
        self.reload()

    # message box

    def popupwn(self, msg, msg1):
        popup = Toplevel()
        popup.title(msg)
        popup.geometry("300x150+400+300")

        def prsok(event):
            popup.destroy()

        msglabel = Label(popup, text=msg1, font=("Poppins", 15))
        B1 = Button(popup, text="Okay", command=popup.destroy)
        msglabel.pack(side="top", fill="x", pady=15)
        B1.place(x=130, y=100)
        popup.bind("<Return>", prsok)
        popup.mainloop()
        return

    # reload

    def reload(self):
        self.today_entry()
        self.count_label_func()
        self.manage_panel()
        self.logo_label()
        self.entry_table_refresh()

    # logo

    @handlererr
    def logo_label(self):
        logger.info("LOGO label initiated")
        self.logo = Label(self.hpage, bg="#ABE9FE", image=logopanel)
        self.logo1 = Label(self.hpage, bg="#ABE9FE", image=logopanel1)
        self.tbox = Label(self.hpage, image=timepanel, bg="#6991C7", bd="0")
        self.tm = Label(self.tbox, bg="#779BCB", font=("Poppins", 12))
        self.logo.place(x=1, y=10, width=500, height=84)
        self.logo1.place(x=xsize / 2 - 250)
        self.tbox.place(x=xsize - 125, width=120, height=80)
        self.tm.place(x=8, y=10)
        self.my_time()

    # count label

    def count_label_func(self):
        logger.info("Count label function initiated")
        self.box = Label(self.hpage, image=countpanel, bg="#6991C7", bd="0")
        self.total_count = Label(
            self.box, text=str(db.employeecount()), font=("Poppins", 35), bg="#455B74"
        )
        self.present = Label(
            self.box,
            text=str(db.get_today_employee_count()),
            font=("Poppins", 35),
            bg="#5CDB8B",
        )
        self.R = db.employeecount() - db.get_today_employee_count()
        self.remaining = Label(
            self.box, text=str(self.R), font=("Poppins", 35), bg="#E82C2C"
        )
        self.box.place(x=1, y=150, width=600, height=186)
        self.total_count.place(x=88, y=98)
        self.present.place(x=274, y=98)
        self.remaining.place(x=459, y=98)
        return

    # manage panel

    def manage_panel(self):
        logger.info("Manage label function initiated")
        self.mng1 = Label(self.hpage, image=managepanel, bg="#6991C7", bd="0")
        self.cam_start = customtkinter.CTkButton(
            self.mng1,
            command=self.camrecogniser,
            image=start,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.manage_button = customtkinter.CTkButton(
            self.mng1,
            command=self.verifyadmin,
            image=manage,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.exit_button = customtkinter.CTkButton(
            self.mng1,
            command=root.quit,
            image=exit1,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.id_button = customtkinter.CTkButton(
            self.mng1,
            command=self.search_by_id,
            image=idsch,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.date_button = customtkinter.CTkButton(
            self.mng1,
            command=self.search_by_date,
            image=dtsch,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.mng1.place(x=1, y=350, width=600, height=380)
        self.cam_start.place(x=47, y=33, width=150, height=150)
        self.manage_button.place(x=236, y=33, width=150, height=150)
        self.exit_button.place(x=425, y=197, width=150, height=150)
        self.id_button.place(x=47, y=197, width=150, height=150)
        self.date_button.place(x=236, y=197, width=150, height=150)
        return

    def my_time(self):
        time_string = strftime("%I:%M:%S %p \n %A \n %d/%m/%y")
        self.tm.config(text=time_string)
        self.tm.after(1000, self.my_time)

    def verifyadmin(self):
        self.openverify = Toplevel(self.up)
        self.openverify.title("Verify Yourself")
        logger.info("Verify admin initiated")
        self.openverify.geometry("345x169+500+300")
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
        self.openverifyentry.place(x=52, y=63, width=233, height=28)
        self.openverifybtn = Button(
            self.openverifylb,
            relief="flat",
            text="Verify",
            background="#A6BDDC",
            command=self.verifyadminbutton,
        )
        self.openverifybtn.place(x=128, y=112, width=72, height=26)
        self.openverify.destroy()
        self.openmainemployeeinfo()

    def verifyadminbutton(self):
        if verifyadmintxt.get() == "admin":
            self.openverifyentry.delete(0, END)
            self.openverify.destroy()
            self.openmainemployeeinfo()

        else:
            self.popupwn("Error", "Wrong Password..")
            self.openverifyentry.delete(0, END)

    # manage Employee

    @handlererr
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
        self.mng2 = Label(
            self.mainemployeewindow, image=managepanel2, bg="#6991C7", bd="0"
        )
        self.logo1 = Label(self.mpage, bg="#ABE9FE", image=mnglogo)
        self.mainempaddbtn = customtkinter.CTkButton(
            self.mng2,
            command=self.new_entry,
            image=empadd,
            width=50,
            height=50,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.mainempbckbtn = customtkinter.CTkButton(
            self.mpage,
            command=self.mainhome_back,
            image=backbtn,
            text="",
            width=50,
            height=50,
            fg_color="#ABE9FE",
            bg_color="#ABE9FE",
        )
        self.mainempupdbtn = customtkinter.CTkButton(
            self.mng2,
            command=self.checkforupdate,
            image=empupdate,
            width=25,
            height=25,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.mainempdelbtn = customtkinter.CTkButton(
            self.mng2,
            command=self.deleteemployee,
            image=empdel,
            width=25,
            height=25,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.opendbscroller = Scrollbar(self.mpage, orient=VERTICAL)
        self.opendbentry = Entry(self.mpage, textvariable=opendbvar)
        self.opendbentry.configure(
            font="-family {Poppins} -size 15",
            relief="solid",
            bg="#ABE9FE",
            highlightbackground="black",
        )
        self.opendbsearch = customtkinter.CTkButton(
            self.mpage,
            text="",
            command=self.search_db,
            width=130,
            height=38,
            image=search,
            bg_color="#ABE9FE",
            fg_color="#ABE9FE",
        )
        self.refresh1 = customtkinter.CTkButton(
            self.mpage,
            text="",
            command=self.refresh12,
            width=130,
            height=38,
            image=refresh,
            bg_color="#ABE9FE",
            fg_color="#ABE9FE",
        )
        self.opendbtable = ttk.Treeview(
            self.mpage, yscrollcommand=self.opendbscroller.set
        )
        self.opendbscroller.config(command=self.opendbtable.yview)
        self.opendbtable.configure(
            columns=(
                "SNO",
                "ID",
                "Name",
                "D.O.B",
                "Gender",
                "E-mail",
                "Phone No",
                "Position",
                "Profile",
                "Address",
            )
        )
        self.opendbtable.heading("#0", text="SNO", anchor=W)
        self.opendbtable.heading("#1", text="ID", anchor=W)
        self.opendbtable.heading("#2", text="Name", anchor=W)
        self.opendbtable.heading("#3", text="D.O.B", anchor=W)
        self.opendbtable.heading("#4", text="Gender", anchor=W)
        self.opendbtable.heading("#5", text="E-mail", anchor=W)
        self.opendbtable.heading("#6", text="Phone No", anchor=W)
        self.opendbtable.heading("#7", text="Position", anchor=W)
        self.opendbtable.heading("#8", text="Profile", anchor=W)
        self.opendbtable.heading("#9", text="Address", anchor=W)
        self.opendbtable.column("#0", minwidth=60, width=80)
        self.opendbtable.column("#1", minwidth=80, width=60)
        self.opendbtable.column("#2", minwidth=80, width=140)
        self.opendbtable.column("#3", minwidth=60, width=100)
        self.opendbtable.column("#4", minwidth=60, width=40)
        self.opendbtable.column("#5", minwidth=60, width=150)
        self.opendbtable.column("#6", minwidth=60, width=100)
        self.opendbtable.column("#7", minwidth=60, width=150)
        self.opendbtable.column("#8", minwidth=60, width=150)
        self.opendbtable.column("#9", minwidth=60, width=150)
        for x, y in enumerate(db.get_all_employee_info(), 1):
            self.opendbtable.insert(
                "",
                "end",
                text=x,
                values=(y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8]),
            )
        self.opendbtable.bind("<<TreeviewSelect>>", self.select)

        self.mpage.pack()
        self.mng2.place(x=20, y=140)
        self.logo1.place(x=xsize / 2 - 250)
        self.mainempbckbtn.place(x=0, y=0, width=144, height=55)
        self.mainempaddbtn.place(x=44, y=38, width=150, height=150)
        self.mainempupdbtn.place(x=42, y=215, width=150, height=150)
        self.mainempdelbtn.place(x=42, y=400, width=150, height=150)
        self.opendbentry.place(x=xsize / 2, y=90, width=xsize / 4, height=30)
        self.opendbsearch.place(
            x=xsize / 2 + xsize / 4 + 25, y=86, width=130, height=38
        )
        self.refresh1.place(x=xsize / 2 + xsize / 4 + 160, y=86, width=130, height=38)
        self.opendbtable.place(
            x=xsize / 2 - 450, y=130, width=xsize - 400, height=ysize - 200
        )
        self.opendbscroller.place(
            x=xsize / 2 - 450 + xsize - 400, y=130, width=20, height=ysize - 200
        )

    def click(self, opt):
        if opt == 1:
            self.mpage.pack_forget()

        elif opt == 2:
            self.mpage.pack()
            self.refresh12()
            self.cam.release()

    def refresh12(self):
        self.opendbtable.delete(*self.opendbtable.get_children())
        for x, y in enumerate(db.get_all_employee_info(), 1):
            self.opendbtable.insert(
                "",
                "end",
                text=x,
                values=(y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8]),
            )

    def mainhome_back(self):
        self.mainemployeewindow.destroy()
        self.up.deiconify()
        self.up.state("zoomed")
        self.reload()
        self.cam.release()
        return

    def select(self, event):
        global selected_item
        selected_item = (
            self.opendbtable.item(self.opendbtable.focus())["values"] or None
        )
        return

    # new Employee

    @handlererr
    def new_entry(self):
        self.click(1)
        self.bg = Label(self.mainemployeewindow, image=newentry)

        # self.mainemployeewindow.protocol("WM_DELETE_WINDOW", self.close)
        if not self.camera_not_found():
            self.popupwn("Camera not found")
            return self.mainemployeewindow.destroy()
        cv2.destroyAllWindows()
        self.nwlg = Label(self.bg, bg="#009EFD", image=addlg)
        self.nwbx = Label(self.bg, bg="#009EFD", image=addpanel)
        self.bckbtn = customtkinter.CTkButton(
            self.bg,
            command=self.clear_entry,
            image=backbtn,
            text="",
            width=50,
            height=50,
            fg_color="#ABE9FE",
            bg_color="#ABE9FE",
        )
        self.EID = Entry(self.nwbx)
        self.ENAME = Entry(self.nwbx)
        self.DOB = Entry(self.nwbx)
        self.GENDER = Entry(self.nwbx)
        self.EMAIL = Entry(self.nwbx)
        self.PHNO = Entry(self.nwbx)
        self.EPOSITION = Entry(self.nwbx)
        self.ADDRESS = Entry(self.nwbx)
        self.submit = Button(self.bg)

        self.EID.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=eid,
        )
        self.ENAME.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=ename,
        )
        self.DOB.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=d_o_b,
        )
        self.GENDER.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=gndr,
        )
        self.EMAIL.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=e_mail,
        )
        self.PHNO.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=ph_no,
        )
        self.EPOSITION.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=eposition,
        )
        self.ADDRESS.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=adrs,
        )

        self.submit.configure(
            relief="flat",
            cursor="hand2",
            borderwidth="0",
            image=add,
            background="#009EFD",
            command=self.on_new_employee,
        )
        self.bg.pack()
        self.nwlg.place(x=450, y=17)
        self.nwbx.place(x=xsize / 2 - 100, y=100)
        self.bckbtn.place(x=1, y=1)
        self.EID.place(x=46, y=116, width=228, height=44)
        self.ENAME.place(x=46, y=250, width=228, height=44)
        self.DOB.place(x=46, y=375, width=228, height=44)
        self.GENDER.place(x=46, y=498, width=228, height=44)
        self.EMAIL.place(x=353, y=119, width=228, height=44)
        self.PHNO.place(x=353, y=250, width=228, height=44)
        self.EPOSITION.place(x=353, y=375, width=228, height=44)
        self.ADDRESS.place(x=353, y=498, width=230, height=44)

        self.submit.place(x=xsize / 2 + 100, y=ysize - 150, width=176, height=56)

        self.camlabel = Label(self.bg, bg="black", borderwidth=3)
        self.camlabel.place(x=40, y=150, width=500, height=450)
        self.cam = cv2.VideoCapture(0)
        while True:
            img1 = self.cam.read()[1]
            gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 0, 0), 2)
            img = ImageTk.PhotoImage(IM.fromarray(img1))
            self.camlabel["image"] = img
            self.bg.update()

    @handlererr
    def clear_entry(self):
        self.EID.delete(0, END)
        self.ENAME.delete(0, END)
        self.DOB.delete(0, END)
        self.GENDER.delete(0, END)
        self.EMAIL.delete(0, END)
        self.PHNO.delete(0, END)
        self.EPOSITION.delete(0, END)
        self.ADDRESS.delete(0, END)
        self.bg.pack_forget()
        self.click(2)
        self.cam.release()
        return

    @handlererr
    def on_new_employee(self):
        Eid = eid.get()
        Ename = ename.get()
        D_o_b = d_o_b.get()
        Gndr = gndr.get()
        E_mail = e_mail.get()
        Ph_no = ph_no.get()
        Eposition = eposition.get()
        Adrs = adrs.get()
        print(Eid, Ename, D_o_b, Gndr, E_mail, Ph_no, Eposition, Adrs)
        if db.check_employee(Eid):
            self.popupwn("error", "Employee already exists")
            return
        if (
            (Eid != "")
            and (Ename != "")
            and (D_o_b != "")
            and (Gndr != "")
            and (E_mail != "")
            and (Ph_no != "")
            and (Eposition != "")
            and (Adrs != "")
        ):
            print("passed")
            name = f"employees/{Eid}.jpg"
            image = IM.fromarray(self.cam.read()[1])
            image.save(name)
            value = db.newEmployee(
                Eid, Ename, D_o_b, Gndr, E_mail, Ph_no, Eposition, Adrs, name
            )
            self.popupwn("success", "Employee added successfully")
            self.clear_entry()

        else:
            self.popupwn("error", "FILL ALL Data ")
            print("failed")
            return

        if value == "ERROR":
            self.popupwn("error", "Invalid Data Entry")
            return self.clear_entry()

        return

    def deleteemployee(self):
        if selected_item:
            db.delete_employee(selected_item[0])
            logger.info("Employee %s deleted", selected_item[0])
            self.opendbtable.delete(self.opendbtable.selection())
            self.selected_item = None
            self.popupwn("Success", "Employee deleted successfully")
        else:
            self.popupwn("Error", "Please select an employee")

    def checkforupdate(self):
        if selected_item:
            datasdict.update(
                {
                    "id": selected_item[0],
                    "name": selected_item[1],
                    "dob": selected_item[2],
                    "gender": selected_item[3],
                    "email": selected_item[4],
                    "phno": selected_item[5],
                    "position": selected_item[6],
                    "profile": selected_item[7],
                    "address": selected_item[8],
                }
            )
            self.updateemployee()
        else:
            self.popupwn("Error", "Please select an employee")

    # update employee
    def updateemployee(self):
        self.click(1)
        self.upbg = Label(self.mainemployeewindow, image=newentry)
        self.mainemployeewindow.protocol("WM_DELETE_WINDOW", self.updateclose)
        self.mainemployeewindow.title("Employee Update")
        self.uplg = Label(self.upbg, bg="#009EFD", image=updtlg)
        self.upbx = Label(self.upbg, bg="#009EFD", image=addpanel)
        self.upbckbtn = customtkinter.CTkButton(
            self.upbg,
            command=self.updateclose,
            image=backbtn,
            text="",
            width=50,
            height=50,
            fg_color="#ABE9FE",
            bg_color="#ABE9FE",
        )
        self.updateEID = Entry(self.upbx)
        self.updateENAME = Entry(self.upbx)
        self.updateDOB = Entry(self.upbx)
        self.updateGENDER = Entry(self.upbx)
        self.updateEMAIL = Entry(self.upbx)
        self.updatePHNO = Entry(self.upbx)
        self.updateEPOSITION = Entry(self.upbx)
        self.updateADDRESS = Entry(self.upbx)

        self.updatesubmit = Button(
            self.upbg,
            relief="flat",
            cursor="hand2",
            borderwidth="0",
            image=updt,
            background="#009EFD",
            command=self.on_emp_update,
        )
        self.updatecambutton = Button(
            self.upbg,
            image=chngimg,
            background="#009EFD",
            text="Change Image",
            relief="flat",
            command=self.update_open_camera,
        )

        self.updateEID.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=updateempid,
        )
        self.updateENAME.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=updateename,
        )
        self.updateDOB.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=updated_o_b,
        )
        self.updateGENDER.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=updategndr,
        )
        self.updateEMAIL.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=updatee_mail,
        )
        self.updatePHNO.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=updateph_no,
        )
        self.updateEPOSITION.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=updateempostion,
        )
        self.updateADDRESS.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=updateadrs,
        )

        self.pht = [datasdict["profile"]]
        self.imgbox = ImageTk.PhotoImage(IM.open(self.pht[0]))

        self.updatecamlabel = Label(
            self.upbg, bg="black", borderwidth=3, image=self.imgbox
        )

        self.upbg.pack()
        self.uplg.place(x=450, y=17)
        self.upbx.place(x=xsize / 2 - 100, y=100)
        self.upbckbtn.place(x=1, y=1)
        self.updateEID.place(x=46, y=116, width=228, height=44)
        self.updateENAME.place(x=46, y=250, width=228, height=44)
        self.updateDOB.place(x=46, y=375, width=228, height=44)
        self.updateGENDER.place(x=46, y=498, width=228, height=44)
        self.updateEMAIL.place(x=353, y=119, width=228, height=44)
        self.updatePHNO.place(x=353, y=250, width=228, height=44)
        self.updateEPOSITION.place(x=353, y=375, width=228, height=44)
        self.updateADDRESS.place(x=353, y=498, width=230, height=44)

        self.updatesubmit.place(x=xsize / 2 + 100, y=ysize - 150, width=176, height=56)
        self.updatecambutton.place(x=85, y=ysize - 250, width=364, height=46)
        self.updatecamlabel.place(x=40, y=150, width=500, height=450)

        self.updateEID.insert(0, datasdict["id"])
        self.updateENAME.insert(0, datasdict["name"])
        self.updateDOB.insert(0, datasdict["dob"])
        self.updateGENDER.insert(0, datasdict["gender"])
        self.updateEMAIL.insert(0, datasdict["email"])
        self.updatePHNO.insert(0, datasdict["phno"])
        self.updateEPOSITION.insert(0, datasdict["position"])
        self.updateADDRESS.insert(0, datasdict["address"])

    def on_emp_update(self):

        if (
            updateempid.get() == ""
            or updateename.get() == ""
            or updateempostion.get() == ""
        ):
            self.popupwn("Error", "Please fill all the fields")

        elif (
            updateempid.get() == str(datasdict["id"])
            and updateename.get() == datasdict["name"]
            and updateempostion.get() == datasdict["position"]
        ):
            self.popupwn("Error", "No changes made")

        if datasdict["camera"]:
            updatednewimage2 = IM.fromarray(self.updateempcam.read()[1])
            updatename = f"employees/{updateempid.get()}.jpg"
            updatednewimage2.save(updatename)
            db.update_employee_info(
                updateempid.get(),
                updateename.get(),
                updated_o_b.get(),
                updategndr.get(),
                updatee_mail.get(),
                updateph_no.get(),
                updateempostion.get(),
                updateadrs.get(),
            )
            logger.info("Employee %s updated", updateempid.get())
            self.popupwn("Success", "Employee updated successfully")
        db.update_employee_info(
            updateempid.get(),
            updateename.get(),
            updated_o_b.get(),
            updategndr.get(),
            updatee_mail.get(),
            updateph_no.get(),
            updateempostion.get(),
            datasdict["profile"],
            updateadrs.get(),
        )

        logger.info("Employee %s updated", updateempid.get())
        self.popupwn("Success", "Employee updated successfully")
        return

    def updateclose(self):
        self.updateEID.delete(0, END)
        self.updateENAME.delete(0, END)
        self.updateDOB.delete(0, END)
        self.updateGENDER.delete(0, END)
        self.updateEMAIL.delete(0, END)
        self.updatePHNO.delete(0, END)
        self.updateEPOSITION.delete(0, END)
        self.updateEID.delete(0, END)
        datasdict.clear()
        datasdict["camera"] = False
        cv2.destroyAllWindows()
        self.upbg.pack_forget()
        self.click(2)

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
            self.mainemployeewindow.update()

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
            bg="#ABE9FE",
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
            bg_color="#ABE9FE",
            fg_color="#ABE9FE",
        )
        self.refresh = customtkinter.CTkButton(
            self.up,
            text="",
            command=self.refresh,
            width=130,
            height=38,
            image=refresh,
            bg_color="#ABE9FE",
            fg_color="#ABE9FE",
        )
        self.entsearch.place(x=xsize / 2 + xsize / 4 + 25, y=86, width=130, height=38)
        self.refresh.place(x=xsize / 2 + xsize / 4 + 160, y=86, width=130, height=38)

    def entry_table_refresh(self):
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
            self.popupwn("Error", "Please enter a ID")
            self.popupwn("Error", "Please enter a ID")
            return
        elif not db.check_employee(id__):
            self.popupwn("Error", "No entry found")
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
        self.reload()

    @handlererr
    def search_db(self):
        opendbtxt = opendbvar.get()
        if not opendbtxt:
            return self.popupwn("Error", "Please enter a Input")
        elif name_match(opendbtxt):
            if position_match(opendbtxt):
                self.opendbtable.delete(*self.opendbtable.get_children())
                for x in db.get_employee_by_position(opendbtxt):
                    self.opendbtable.insert(
                        "",
                        "end",
                        text=x[0],
                        values=(x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]),
                    )
            return self.popupwn("Error", "Please enter a valid Input")
        elif int_match(opendbtxt):
            if not db.check_employee(opendbtxt):
                return self.popupwn("Error", "Employee not found")
            self.opendbtable.delete(*self.opendbtable.get_children())
            for x in db.get_employee_info_by_id(opendbtxt):
                self.opendbtable.insert(
                    "",
                    "end",
                    text=x[0],
                    values=(x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]),
                )
        self.popupwn("Success", "Employee found")

    def opendatabaseExit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.opendbentry.delete(0, END)
            self.opendatabase.destroy()
            self.up.deiconify()

    def search_by_date(self):
        self.dateWindow = Toplevel()
        self.dateWindow.title("Search by DATE")
        self.dateWindow.geometry("1000x650+100+50")
        self.dateWindow.configure(bg="black")
        self.dateWindow.resizable(False, False)
        self._dateWindow = Label(self.dateWindow, image=searchbg)
        self._dateWindow.place(x=0, y=0)
        self.dtlist = []
        self.cal = DateEntry(
            self._dateWindow,
            selectmode="day",
            date_pattern="dd-mm-yy",
            textvariable=date_,
            font="-family {Poppins} -size 15",
            relief="flat",
        )
        self.cal.place(x=59, y=149, width=188, height=27)

        self.scroolbardatey = Scrollbar(self._dateWindow, orient=VERTICAL)
        self.tree2 = ttk.Treeview(
            self._dateWindow, yscrollcommand=self.scroolbardatey.set
        )
        self.tree2.place(x=300, y=35, width=600, height=556)
        self.scroolbardatey.place(x=900, y=35, width=20, height=556)
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
        self.dtprnt_button = customtkinter.CTkButton(
            master=self._dateWindow,
            width=120,
            height=32,
            border_width=2,
            fg_color=("#66A4DA"),
            text="print",
            bg="#66A4DA",
            command=self.dt_prnt,
        )
        self.dtprnt_button.place(x=85, y=250)
        self.dtadsrh_ = Checkbutton(
            self._dateWindow,
            text="Advance Search",
            onvalue=1,
            offvalue=0,
            variable=adv1_,
            command=self.enablecal,
            bg="#66A4DA",
        )
        self.dtadsrh_.place(x=50, y=300)
        self.check2_ = Checkbutton(
            self._dateWindow,
            bg="#66A4DA",
            text="Click To Date Range",
            state="disabled",
            onvalue=1,
            offvalue=0,
            variable=dtchk_,
            command=self.enablecal,
        )
        self.check2_.place(x=85, y=350)
        self.dtcal1 = DateEntry(
            self._dateWindow,
            selectmode="day",
            date_pattern="dd-mm-yyyy",
            textvariable=startdt,
            font="-family {Poppins} -size 10",
            relief="flat",
            state="disabled",
        )
        self.dtcal1.place(x=59, y=380, width=188, height=27)
        self.dtcal2 = DateEntry(
            self._dateWindow,
            selectmode="day",
            date_pattern="dd-mm-yyyy",
            textvariable=enddt,
            font="-family {Poppins} -size 10",
            relief="flat",
            state="disabled",
        )
        self.dtcal2.place(x=59, y=449, width=188, height=27)
        return

    def on_date_search(self):
        date__ = date_.get()
        self.dtchk__ = dtchk_.get()
        self.dtlist.clear()
        if not date__:
            self.popupwn("Error", "Please enter a date")
            return
        dat__ = dateEncodedTable(date__)
        if not db.validate_date(dat__):
            self.popupwn("Error", "No entry found")
            return
        if self.dtchk__ == 1:
            x = startdt.get()
            y = enddt.get()
            date_1 = date(int(x[6:]), int(x[3:5]), int(x[:2]))
            date_2 = date(int(y[6:]), int(y[3:5]), int(y[:2]))
            self.tree2.delete(*self.tree2.get_children())
            for val in db.search_date_by_range(date_1, date_2):
                self.tree2.insert(
                    "", "end", text=val[0], values=(val[1], val[2], val[3], val[4])
                )
                a = list(val)
                del a[5]
                self.dtlist.append(a)
        else:
            self.tree2.delete(*self.tree2.get_children())
            for val in db.get_entry_by_date(dat__):
                self.tree2.insert(
                    "", "end", text=val[0], values=(val[1], val[2], val[3], val[4])
                )
                a = list(val)
                del a[5]
                self.dtlist.append(a)

    def dt_prnt(self):
        time_string = strftime("%d-%m-%y - %I%M")
        if self.dtchk__ == 1:
            if len(self.dtlist) != 0:
                x = "data/{} to {} - {}.xlsx".format(
                    startdt.get(), startdt.get(), time_string
                )
                for vals in self.dtlist:
                    df = pd.DataFrame.from_records(
                        self.dtlist,
                        columns=["ID", "Name", "Date", "Entry Time", "Exit Time"],
                    )
                    df.to_excel(x)
                self.popupwn("Success", "Successfully saved")
        elif self.dtchk__ == 0:
            x = "data/{}.xlsx".format(date_.get())
            for vals in self.dtlist:
                df = pd.DataFrame.from_records(
                    self.dtlist,
                    columns=["ID", "Name", "Date", "Entry Time", "Exit Time"],
                )
                df.to_excel(x)
            self.popupwn("Success", "Successfully saved")

        else:
            self.popupwn("Error", "Table is Empty")

    def enablecal(self):
        if adv1_.get():
            self.check2_.configure(state="normal")
            if dtchk_.get():
                self.dtcal1.configure(state="normal")
                self.dtcal2.configure(state="normal")
            else:
                self.dtcal1.configure(state="disabled")
                self.dtcal2.configure(state="disabled")
        else:
            self.check2_.configure(state="disabled")

    def search_by_id(self):
        self.idWindow = Toplevel()
        self.idWindow.title("Search by ID")
        self.idWindow.geometry("1000x650+100+50")
        self.idWindow.configure(bg="black")
        self.idWindow.resizable(False, False)
        self._idWindow = Label(self.idWindow, image=searchbg)
        self._idWindow.place(x=0, y=0)
        self.identry = Entry(self._idWindow)
        self.identry.place(x=59, y=149, width=188, height=27)
        self.identry.configure(
            font="-family {Poppins} -size 15",
            relief="flat",
            textvariable=Id_,
            bg="#66A4DA",
        )
        self.scroolbaridy = Scrollbar(self._idWindow, orient=VERTICAL)
        self.tree3 = ttk.Treeview(self._idWindow, yscrollcommand=self.scroolbaridy.set)
        self.tree3.place(x=300, y=35, width=600, height=556)
        self.scroolbaridy.place(x=900, y=35, width=20, height=556)
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
        self.identry.bind("<Return>", self.on_id_search)
        self.prnt_button = customtkinter.CTkButton(
            master=self._idWindow,
            width=120,
            height=32,
            border_width=2,
            fg_color=("#66A4DA"),
            text="print",
            bg="#66A4DA",
            command=self.id_prnt,
        )
        self.prnt_button.place(x=85, y=250)
        self.tpy = []
        self.adsrh_ = Checkbutton(
            self._idWindow,
            text="Advance Search",
            onvalue=1,
            offvalue=0,
            variable=adv_,
            command=self.enablecal1,
            bg="#66A4DA",
        )
        self.adsrh_.place(x=50, y=300)
        self.check_ = Checkbutton(
            self._idWindow,
            text="Custom Date",
            onvalue=1,
            offvalue=0,
            variable=chk_,
            command=self.enablecal1,
            state="disabled",
            bg="#66A4DA",
        )
        self.check_.place(x=85, y=330)
        self.check1_ = Checkbutton(
            self._idWindow,
            text="Custom Date Range",
            onvalue=1,
            offvalue=0,
            state="disabled",
            variable=chks_,
            command=self.enablecal1,
            bg="#66A4DA",
        )
        self.check1_.place(x=85, y=360)
        self.cal1 = DateEntry(
            self._idWindow,
            selectmode="day",
            date_pattern="dd-mm-yyyy",
            textvariable=start_dt,
            font="-family {Poppins} -size 10",
            relief="flat",
            state="disabled",
        )
        self.cal1.place(x=59, y=400, width=188, height=27)
        self.cal2 = DateEntry(
            self._idWindow,
            selectmode="day",
            date_pattern="dd-mm-yyyy",
            textvariable=end_dt,
            font="-family {Poppins} -size 10",
            relief="flat",
            state="disabled",
        )
        self.cal2.place(x=59, y=449, width=188, height=27)

        return

    def on_id_search(self):
        id__ = Id_.get()
        chck_ = chk_.get()
        check__ = chks_.get()
        x = start_dt.get()
        y = end_dt.get()
        self.tpy.clear()

        if not id__:
            self.popupwn("Error", "Please enter a ID")
            return
        elif not db.check_employee(id__):
            self.tree3.delete(*self.tree3.get_children())
            self.popupwn("Error", "No entry found")
            return
        if chck_ == 0 and check__ == 0:
            self.tree3.delete(*self.tree3.get_children())
            for val in db.search_data_by_id(id__):
                self.tree3.insert(
                    "", "end", text=val[0], values=(val[1], val[2], val[3], val[4])
                )
                a = list(val)
                del a[5]
                self.tpy.append(a)

        if chck_ == 1 and check__ == 0:
            self.tree3.delete(*self.tree3.get_children())
            for val in db.get_id_date(x, id__):
                self.tree3.insert(
                    "", "end", text=val[0], values=(val[1], val[2], val[3], val[4])
                )
                a = list(val)
                del a[5]
                self.tpy.append(a)

        if chck_ == 0 and check__ == 1:
            date_1 = date(int(x[6:]), int(x[3:5]), int(x[:2]))
            date_2 = date(int(y[6:]), int(y[3:5]), int(y[:2]))
            self.tree3.delete(*self.tree3.get_children())
            for val in db.search_date_by_id(date_1, date_2, id__):
                self.tree3.insert(
                    "", "end", text=val[0], values=(val[1], val[2], val[3], val[4])
                )
                a = list(val)
                del a[5]
                self.tpy.append(a)

    def id_prnt(self):
        time_string = strftime("%d-%m-%y - %I %M")
        if len(self.tpy) != 0:
            x = "data/{}-{}-{} .xlsx".format(
                self.tpy[0][0], self.tpy[0][1], time_string
            )
            for vals in self.tpy:
                df = pd.DataFrame.from_records(
                    self.tpy, columns=["ID", "Name", "Date", "Entry Time", "Exit Time"]
                )
                df.to_excel(x)
            self.popupwn("Success", "Successfully saved")

        else:
            self.popupwn("Error", "Table is Empty")

    def enablecal1(self):
        if adv_.get():
            self.check_.configure(state="normal")
            self.check1_.configure(state="normal")

            if chk_.get():
                self.check1_.configure(state="disabled")
                self.cal1.configure(state="normal")
            else:
                self.cal1.configure(state="disabled")
                self.check1_.configure(state="normal")
            if chks_.get():
                self.cal1.configure(state="normal")
                self.cal2.configure(state="normal")
                self.check_.config(state="disabled")
            else:
                self.cal2.configure(state="disabled")
                self.check_.config(state="normal")
        else:
            self.check_.configure(state="disabled")
            self.check1_.configure(state="disabled")

    @handlererr
    def today_entry(self):
        self.tree.delete(*self.tree.get_children())
        tddate = dateEncodedTable(today()[0])
        for x in db.get_entry_by_date(tddate):
            self.tree.insert("", "end", text=x[0], values=(x[1], x[2], x[3], x[4]))

    @handlererr
    def close(self):
        self.cam.release()
        cv2.destroyAllWindows()
        self.mainemployeewindow.destroy()
        self.reload()

    @handlererr
    def employee_arrived(self, eid):
        data = db.getemployee(eid)
        for val in db.get_entry_by_id(eid):
            self.empid_frame.config(text=val[0])
            self.ename_frame.config(text=val[1])
            self.entry_frame.config(text=val[3])
            self.leave_frame.config(text=val[4])
        if dat := db.get_entry_time(eid, today()[0]):
            Rtime = time() - dat
            if Rtime > 600:
                timer = db.get_emp_entry_time(eid, today()[0])
                logger.info(f"{data[1]} already left at {today()[1]}")
                logger.info(f"{eid} Left")
                self.empid.config(text=f"{eid} - {data[1]} already left ")
                db.leaveemp(
                    eid=eid,
                    ename=data[1],
                    date=today()[0],
                    entry=timer,
                    leave=today()[1],
                    Time=time(),
                )
                self.refresh1()
        logger.info(f"{data[1]} already arrived at {today()[1]}")
        logger.info(f"{eid} arrived")
        self.empid.config(text=f"{eid} is arrived")
        self.empid.config(text=f"{eid} - {data[1]} already arrived ")
        db.entryemp(
            eid=eid, ename=data[1], date=today()[0], entry=today()[1], Time=time()
        )
        self.reload()

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
            image=backbtn2,
            text="",
            fg_color="#00C6FB",
            bg_color="#00C6FB",
        )
        self.exit_.place(x=0, y=0)
        self.tbox = Label(self.camrbg, image=timepanel2, bg="#6991C7", bd="0")
        self.tbox.place(x=xsize - 115)
        self.tm = Label(self.tbox, bg="#fff1eb", font=("Poppins", 12))
        self.tm.place(x=5, y=8)
        self.camlabel = Label(self.camrbg, width=600, height=470)
        self.camlabel.place(x=xsize / 2 - 250, y=ysize / 2 - 250)
        self.empview = Label(self.camrbg, bg="#00C6FB", image=viewpnl)
        self.empview.place(x=10, y=ysize / 2 - 284)

        self.empid_frame = Label(self.empview, font=("Poppins", 25), bg="#47D6FC")
        self.ename_frame = Label(self.empview, font=("Poppins", 25), bg="#47D6FC")
        self.entry_frame = Label(self.empview, font=("Poppins", 25), bg="#47D6FC")
        self.leave_frame = Label(self.empview, font=("Poppins", 25), bg="#47D6FC")
        self.empid_frame.place(x=73, y=137)
        self.ename_frame.place(x=73, y=255)
        self.entry_frame.place(x=73, y=373)
        self.leave_frame.place(x=73, y=491)
        self.empid = Label(self.camrbg, font=("Poppins", 30), bg="#00FFDD")
        self.empid.place(x=xsize / 2 - 249, y=ysize / 2 - 315, width=602, height=60)
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
                self.empid_frame.config(text="")
                self.ename_frame.config(text=" ")
                self.entry_frame.config(text=" ")
                self.leave_frame.config(text=" ")

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

    def camera_not_found(self):
        try:
            cv2.VideoCapture(0)
            return True
        except BaseException:
            return False


# page = HomePage(root)
# root.mainloop()
