import os

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
        self.tm = Label(self.hpage, bg="#6991C7")
        self.tm.place(x=xsize - 100, y=10)
        self.my_time()
        self.mng1 = Label(self.hpage, image=managepanel, bg="#6991C7", bd="0")
        self.mng1.place(x=1, y=300)
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
            command=self.openmainemployeeinfo,
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
        self.tab = self.entry_table()
        self.count_label_func()

    @handlererr
    def count_label_func(self):
        logger.info("Count label function initiated")
        self.box = Label(self.hpage, image=countpanel, bg="#6991C7", bd="0")
        self.box.place(x=1, y=100)
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

    def my_time(self):
        time_string = strftime("%H:%M:%S %p \n %A \n %x")
        self.tm.config(text=time_string)
        self.tm.after(1000, self.my_time)

    def openmainemployeeinfo(self):
        logger.info("Open main employee info function initiated")
        self.up.withdraw()
        self.mainemployeewindow = Toplevel()
        self.mainemployeewindow.protocol("WM_DELETE_WINDOW", self.mainhome_back)
        self.mainemployeewindow.title("Employee Info")
        self.mainemployeewindow.state("zoomed")
        self.mainemployeewindow.resizable(False, False)
        self.mpage = Label(
            self.mainemployeewindow, image=homebg, width=xsize, height=ysize
        )
        self.mpage.pack()
        self.mainempaddbtn = customtkinter.CTkButton(
            self.mainemployeewindow,
            command=self.new_entry,
            image=empadd,
            width=50,
            height=50,
            text="",
            fg_color="#6991C7",
            bg_color="#6991C7",
        )
        self.mainempbckbtn = customtkinter.CTkButton(
            self.mainemployeewindow,
            command=self.mainhome_back,
            # image=empwindowbck,
            text="back",
            width=50,
            height=50,
            fg_color="#6991C7",
            bg_color="#6991C7",
        )
        self.mainempbckbtn.place(x=0, y=0)
        self.mainempaddbtn.place(x=100, y=100)
        self.mainempupdbtn = customtkinter.CTkButton(
            self.mainemployeewindow,
            command=self.deleteemployee,
            image=empupdate,
            width=25,
            height=25,
            text="",
            fg_color="#6991C7",
            bg_color="#6991C7",
        )
        self.mainempupdbtn.place(x=100, y=300)
        self.mainempdelbtn = customtkinter.CTkButton(
            self.mainemployeewindow,
            command=self.deleteemployee,
            image=empdel,
            width=25,
            height=25,
            text="",
            fg_color="#6991C7",
            bg_color="#6991C7",
        )
        self.mainempdelbtn.place(x=100, y=500)

        # self.opendblabel = Label(self.mainemployeewindow, image=opendbimg)
        #  self.opendblabel.place(x=xsize-100, y=20)
        self.opendbscroller = Scrollbar(self.mainemployeewindow, orient=VERTICAL)
        self.opendbentry = Entry(self.mainemployeewindow, textvariable=opendbvar)
        self.opendbentry.place(x=xsize / 2 - 100, y=80, width=500, height=30)
        self.opendbsearch = customtkinter.CTkButton(
            self.mainemployeewindow, text="Search", command=self.search_db, height=30
        )
        self.opendbsearch.place(x=xsize / 2 + xsize / 2 - 250, y=80)
        self.opendbtable = ttk.Treeview(
            self.mainemployeewindow, yscrollcommand=self.opendbscroller.set
        )
        self.opendbtable.place(
            x=xsize / 2 - 100, y=120, width=xsize / 2, height=ysize - 200
        )
        self.opendbscroller.config(command=self.opendbtable.yview)
        self.opendbscroller.place(
            x=xsize / 2 - 100 + xsize / 2, y=120, height=ysize - 200
        )
        self.opendbtable.configure(columns=("ID", "Name", "Position", "Profile"))
        self.opendbtable.heading("#0", text="ID", anchor=W)
        self.opendbtable.heading("#1", text="Name", anchor=W)
        self.opendbtable.heading("#2", text="Position", anchor=W)
        self.opendbtable.heading("#3", text="Profile", anchor=W)
        self.opendbtable.column("#0", minwidth=60, width=100)
        self.opendbtable.column("#1", minwidth=60, width=100)
        self.opendbtable.column("#2", minwidth=60, width=100)
        self.opendbtable.column("#3", minwidth=60, width=100)
        for x in db.get_all_employee_info():
            self.opendbtable.insert("", "end", text=x[0], values=(x[1], x[2], x[3]))

    def mainhome_back(self):
        self.mainemployeewindow.destroy()
        self.up.deiconify()
        return

    def deleteemployee(self):
        return messagebox.showinfo("Info", "This feature is not available yet")

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
        self.entrybar.place(x=xsize / 2, y=80, width=xsize / 4, height=30)
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
        self.entsearch.place(x=xsize / 2 + xsize / 4 + 25, y=76)
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
        self.refresh.place(x=xsize / 2 + xsize / 4 + 160, y=76)

        self.style.map("Treeview.Heading", background=[("active", "#3484F0")])
        self.tree = ttk.Treeview(
            self.up, yscrollcommand=self.scroolbarentryy.set, style="Treeview"
        )
        self.tree.place(x=xsize / 2, y=120, width=xsize / 2 - 100, height=ysize - 200)
        self.scroolbarentryy.place(
            x=xsize / 2 + xsize / 2 - 100, y=120, width=20, height=ysize - 200
        )
        self.scroolbarentryy.config(command=self.tree.yview)
        self.tree.configure(columns=("ID", "Name", "Date", "Entry Time", "Exit Time"))
        self.tree.heading("#0", text="ID", anchor=W)
        self.tree.heading("#1", text="Name", anchor=W)
        self.tree.heading("#2", text="Date", anchor=W)
        self.tree.heading("#3", text="Entry Time", anchor=W)
        self.tree.heading("#4", text="Exit Time", anchor=W)
        self.tree.column("#0", minwidth=60, width=100)
        self.tree.column("#1", minwidth=60, width=100)
        self.tree.column("#2", minwidth=60, width=100)
        self.tree.column("#3", minwidth=60, width=100)
        self.tree.column("#4", minwidth=60, width=100)
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
        for i in self.tree.get_children():
            self.tree.delete(i)

        for val in db.get_entry_by_id(id__):
            self.tree.insert(
                "", "end", text=val[0], values=(val[1], val[2], val[3], val[4])
            )

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        daterr = dateEncodedTable(today()[0])
        for x in db.get_entry_by_date(daterr):
            self.tree.insert("", "end", text=x[0], values=(x[1], x[2], x[3], x[4]))

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
        check = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if check:
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
        if not db.validate_date(dat__):
            messagebox.showerror("Error", "No entry found")
            return
        for i in self.tree2.get_children():
            self.tree2.delete(i)
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
            print(db.check_employee(id__))
            messagebox.showerror("Error", "No entry found")
            return
        for x in self.tree3.get_children():
            self.tree3.delete(x)
        for val in db.get_entry_by_id(id__):
            self.tree3.insert(
                "", "end", text=val[0], values=(val[1], val[2], val[3], val[4])
            )

    @handlererr
    def today_entry(self):
        for x in self.tree.get_children():
            self.tree.delete(x)
        tddate = dateEncodedTable(today()[0])
        for x in db.get_entry_by_date(tddate):
            self.tree.insert("", "end", text=x[0], values=(x[1], x[2], x[3], x[4]))

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
        self.submit.place(relx=0.60, rely=0.80)
        self.submit.configure(
            relief="flat",
            cursor="hand2",
            borderwidth="0",
            image=add,
            command=self.on_new_employee,
        )
        self.camlabel = Label(self.window, bg="black", borderwidth=3)
        self.camlabel.place(x=50, y=76, width=346, height=356)
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

    # @handlererr
    def employee_arrived(self, eid):
        data = db.getemployee(eid)
        if dat := db.get_entry_time(eid, today()[0]):
            Rtime = time() - dat
            if Rtime < 7200:
                logger.info(f"{data[1]} already arrived at {today()[1]}")
                return self.empid.config(text=f"{eid} already arrived at {today()[1]}")
            timer = db.get_emp_entry_time(eid, today()[0])
            db.employee_entry(
                eid=eid,
                ename=data[0],
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

    #   @handlererr
    def camrecogniser(self):
        self.window = Toplevel()
        self.window.state("zoomed")
        self.cam = cv2.VideoCapture(0)
        self.window.geometry(f"{xsize}x{ysize}")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.title("Recogniser")

        self.camrbg = Label(self.window, image=cambg, width=xsize, height=ysize)
        self.camrbg.pack()
        self.exit_ = customtkinter.CTkButton(
            self.camrbg,
            command=self.close,
            image=exit1,
            text="",
            fg_color="#779BCB",
            bg_color="#779BCB",
        )
        self.exit_.place(x=1, y=100)

        self.camlabel = Label(self.camrbg, width=600, height=470)
        self.camlabel.place(x=xsize / 2 - 250, y=ysize / 2 - 250)
        self.empid = Entry(self.camrbg)
        self.empid = Label(self.camrbg, font=("Poppins", 30), bg="#00FFDD")
        self.empid.place(x=xsize / 2 - 250, y=ysize / 2 - 320, width=600, height=60)
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
