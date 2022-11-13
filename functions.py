import base64
import logging
import re
from datetime import datetime
from time import *
from tkinter import *
from tkinter import messagebox

import cv2
import pytz
from PIL import Image as IM
from PIL import ImageTk

root = Tk()
root.title("Face Recognition")
root.state("zoomed")
ysize = root.winfo_screenheight()
xsize = root.winfo_screenwidth()
face_cascade = cv2.CascadeClassifier("model.xml")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logger = logging.getLogger("EMPLOYEE ATTENDANCE")


# bg
loginbg = ImageTk.PhotoImage(IM.open("resources/login/bg.jpg"))
homebg = ImageTk.PhotoImage(IM.open("resources/home/home.jpg"))
mngbg = ImageTk.PhotoImage(IM.open("resources/manage/manage.jpg"))
newentry = ImageTk.PhotoImage(IM.open("resources/add/entry.jpg"))
searchbg = ImageTk.PhotoImage(IM.open("resources/search/search.jpg"))
opendbimg = ImageTk.PhotoImage(IM.open("resources/opendb/opendb.jpg"))
cambg = ImageTk.PhotoImage(IM.open("resources/camera/cambg.jpg"))

# box

loginbox = ImageTk.PhotoImage(IM.open("resources/login/login.jpg"))
managepanel = ImageTk.PhotoImage(IM.open("resources/home/box2.png"))
managepanel2 = ImageTk.PhotoImage(IM.open("resources/manage/box3.png"))
timepanel = ImageTk.PhotoImage(IM.open("resources/home/time.png"))
timepanel2 = ImageTk.PhotoImage(IM.open("resources/camera/time.png"))
addpanel = ImageTk.PhotoImage(IM.open("resources/add/addbox.png"))


# label
logopanel = ImageTk.PhotoImage(IM.open("resources/home/logo.jpg"))
logopanel1 = ImageTk.PhotoImage(IM.open("resources/home/logo.png"))
lolg = ImageTk.PhotoImage(IM.open("resources/login/lglo.png"))
countpanel = ImageTk.PhotoImage(IM.open("resources/home/box.png"))
addlg = ImageTk.PhotoImage(IM.open("resources/add/addlg.png"))
updtlg = ImageTk.PhotoImage(IM.open("resources/add/updtlg.png"))
passlb = ImageTk.PhotoImage(IM.open("resources/manage/pass.png"))
mnglogo = ImageTk.PhotoImage(IM.open("resources/manage/mnglogo.png"))
viewpnl = ImageTk.PhotoImage(IM.open("resources/camera/view.png"))

# button
login = ImageTk.PhotoImage(IM.open("resources/login/login.png"))
add = ImageTk.PhotoImage(IM.open("resources/add/add.png"))
updt = ImageTk.PhotoImage(IM.open("resources/add/update.png"))
chngimg = ImageTk.PhotoImage(IM.open("resources/add/change.png"))
search = ImageTk.PhotoImage(IM.open("resources/home/search.png"))
refresh = ImageTk.PhotoImage(IM.open("resources/home/refresh.png"))
backbtn = ImageTk.PhotoImage(IM.open("resources/manage/back.png"))
backbtn2 = ImageTk.PhotoImage(IM.open("resources/camera/back.png"))

# logo

start = ImageTk.PhotoImage(IM.open("resources/home/start.png"))
exit1 = ImageTk.PhotoImage(IM.open("resources/home/exit.png"))
stp = ImageTk.PhotoImage(IM.open("resources/home/stop.png"))
idsch = ImageTk.PhotoImage(IM.open("resources/home/id.png"))
dtsch = ImageTk.PhotoImage(IM.open("resources/home/date.png"))
manage = ImageTk.PhotoImage(IM.open("resources/manage/manage.png"))
empadd = ImageTk.PhotoImage(IM.open("resources/manage/add.png"))
empdel = ImageTk.PhotoImage(IM.open("resources/manage/delete.png"))
empupdate = ImageTk.PhotoImage(IM.open("resources/manage/update.png"))
back = ImageTk.PhotoImage(IM.open("resources/manage/add.png"))
unknownimg = ImageTk.PhotoImage(IM.open("resources/opendb/unknown.jpg"))

user = StringVar()
password = StringVar()

eid = StringVar()
ename = StringVar()
d_o_b = StringVar()
gndr = StringVar()
e_mail = StringVar()
ph_no = StringVar()
eposition = StringVar()
adrs = StringVar()

updateempid = StringVar()
updateename = StringVar()
updated_o_b = StringVar()
updategndr = StringVar()
updatee_mail = StringVar()
updateph_no = StringVar()
updateempostion = StringVar()
updateadrs = StringVar()

date_ = StringVar()
chk_ = IntVar()
chks_ = IntVar()
start_dt = StringVar()
end_dt = StringVar()
Id_ = StringVar()
adv_ = IntVar()

startdt = StringVar()
enddt = StringVar()
dtchk_ = IntVar()
adv1_ = IntVar()

tdy_ = StringVar()
opendbvar = StringVar()
position_match = StringVar()
verifyadmintxt = StringVar()
updatesearch = StringVar()
updateempid = StringVar()
updateename = StringVar()
updateempostion = StringVar()
datasdict = {}
selected_item = None
UPDATECAMERA = None


def handlererr(func) -> None:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException:
            pass

    return wrapper


def datematch(date: str) -> bool:
    return re.match(r"^\d{2}-\d{2}-\d{2}$", date) is not None


def int_match(int: str) -> bool:
    return re.match(r"^[0-9]+$", int) is not None


def name_match(name: str) -> bool:
    return re.match(r"^[A-z \.-]+$", name) is not None


def today() -> tuple:
    country_time_zone = pytz.timezone("Asia/Calcutta")
    country_time = datetime.now(country_time_zone)
    day, time = country_time.strftime("%d-%m-%y"), country_time.strftime("%H:%M:%S")
    return day, time


@handlererr
def Exit() -> None:
    if messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=root):
        cv2.destroyAllWindows()
        root.destroy()
    return


root.protocol("WM_DELETE_WINDOW", Exit)


def parse_month(date: str) -> str:
    return date.split("-")[1]


def dateEncodedTable(date: str) -> str:
    return base64.urlsafe_b64encode(date.encode()).decode("ascii").replace("=", "")


def dateDecodedTable(query: str) -> str:
    return base64.urlsafe_b64decode(query.encode() + b"=" * (-len(query) % 4)).decode(
        "ascii"
    )
