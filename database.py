import sqlite3
from datetime import timedelta

from functions import dateEncodedTable, logger, today


class databases:
    def __init__(self):
        self.db = sqlite3.connect("main.db", check_same_thread=False)
        self.dbname = dateEncodedTable(today()[0])
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS EMPLOYEE_INFO(Employeeid INTEGER PRIMARY KEY NOT NULL,EmployeeName TEXT NOT NULL,dob TEXT NOT NULL,gender TEXT NOT NULL,email TEXT NOT NULL,phno INTEGER UNIQUE NOT NULL, EmployeePosition TEXT NOT NULL,EmployeeProfile TEXT NOT NULL,address TEXT NOT NULL);"
        )
        logger.info("Database EMPLOYEE_INFO initialized")
        self.db.execute(
            f"CREATE TABLE IF NOT EXISTS {self.dbname}(Employeeid INTEGER,EmployeeName TEXT,Date TEXT,Entry TEXT,Leave TEXT,Time INTEGER,PRIMARY KEY (Employeeid) ,FOREIGN KEY (Employeeid) REFERENCES EMPLOYEE_INFO(Employeeid));"
        )
        logger.info("Database %s initialized", self.dbname)
        self.db.commit()

    def check_employee(self, employeeID: int) -> bool:
        query = "SELECT * FROM EMPLOYEE_INFO WHERE EmployeeId = ?;"
        msg = self.db.execute(query, [employeeID])
        self.db.commit()
        return len(list(msg)) != 0

    def newEmployee(
        self,
        employee_id: int,
        name: str,
        dob,
        gender: str,
        email: str,
        phno: int,
        position: str,
        profile: str,
        address: str,
    ) -> str:
        query = "INSERT INTO EMPLOYEE_INFO(EmployeeId, EmployeeName,dob ,gender ,email ,phno, EmployeePosition, EmployeeProfile,address) VALUES (?, ?, ?, ?,?, ?, ?, ?,?);"
        try:
            self.db.execute(
                query,
                [
                    employee_id,
                    name,
                    dob,
                    gender,
                    email,
                    phno,
                    position,
                    profile,
                    address,
                ],
            )
            logger.info("New employee added")
            self.db.commit()
            return "SUCCESS"
        except BaseException:
            return "ERROR"

    def update_employee_info(
        self, eid, name, dob, gender, email, phno, position, profile, address
    ) -> None:
        query = "UPDATE EMPLOYEE_INFO SET EmployeeId = ?, EmployeeName = ?,dob = ?,gender= ? ,email = ? ,phno= ?, EmployeePosition = ?, EmployeeProfile = ? ,address =? WHERE EmployeeId = ?;"
        self.db.execute(
            query,
            [eid, name, dob, gender, email, phno, position, profile, address, eid],
        )
        self.db.commit()
        return

    def employeecount(self) -> int:
        query = "SELECT * FROM EMPLOYEE_INFO;"
        msg = self.db.execute(query)
        return len(list(msg))

    def get_today_employee_count(self) -> int:
        values = self.db.execute(f"SELECT * FROM {self.dbname};")
        self.db.commit()
        return len(list(values))

    def getemployee(self, employee_id: int) -> list:
        if not self.check_employee(employee_id):
            return None
        query = "SELECT * FROM EMPLOYEE_INFO WHERE EmployeeId = ?;"
        msg = self.db.execute(query, [employee_id])
        self.db.commit()
        return list(msg)[0]

    def delete_employee(self, employee_id: int):
        if not self.check_employee(employee_id):
            return None
        query = "DELETE FROM EMPLOYEE_INFO WHERE EmployeeId = ?;"
        self.db.execute(query, [employee_id])
        self.db.commit()
        return

    def employees_sorted_by_id_entries(self):
        query = "SELECT * FROM EMPLOYEE_ENTRY ORDER BY EmployeeId;"
        sorted = self.db.execute(query)
        self.db.commit()
        return list(sorted)

    def get_entry_time(self, eid: int, date: str):
        query = f"SELECT * FROM {self.dbname} WHERE EmployeeId = ? AND Date = ?;"
        try:
            values = self.db.execute(query, [eid, date])
            self.db.commit()
            datas = list(values)
            return datas[0][5]
        except Exception:
            return 0

    def get_emp_entry_time(self, eid: int, date: str):
        query = f"SELECT * FROM {self.dbname} WHERE EmployeeId = ? AND Date = ?;"
        try:
            values = self.db.execute(query, [eid, date])
            self.db.commit()
            datas = list(values)
            return datas[0][3]
        except Exception:
            return None

    def entryemp(
        self,
        eid: int,
        ename: str,
        date: str,
        entry: str,
        leave: str = None,
        Time: float = None,
    ) -> None:
        logger.info("Employee entry added into %s", self.dbname)
        query = f"INSERT INTO {self.dbname}(EmployeeId, EmployeeName, Date, Entry, Leave, Time) SELECT ?,?,?,?,?,? WHERE  NOT EXISTS (SELECT * FROM {self.dbname} WHERE EmployeeId=? AND Date=?);"
        self.db.execute(query, [eid, ename, date, entry, leave, Time, eid, date])
        logger.info("Employee entry added into %s", self.dbname)
        self.db.commit()

    def leaveemp(
        self,
        eid: int,
        ename: str,
        date: str,
        entry: str,
        leave: str,
        Time: float = None,
    ) -> None:
        logger.info("Employee leave added into %s", self.dbname)
        query = f"UPDATE {self.dbname} SET leave=? WHERE EmployeeId=? AND Entry IS NOT NULL AND  Leave IS NULL;"
        self.db.execute(query, [leave, eid])
        self.db.commit()

    def get_employee_info_by_id(self, eid) -> list:
        values = self.db.execute(
            "SELECT * FROM EMPLOYEE_INFO WHERE EmployeeId = ?;", [eid]
        )
        self.db.commit()
        return list(values)

    def get_employee_by_position(self, position) -> list:
        query = "SELECT * FROM EMPLOYEE_INFO WHERE EmployeePosition = ?;"
        self.db.execute(query, [position])
        self.db.commit()
        return list(query)

    def get_all_employee_info(self) -> list:
        query = " SELECT * FROM EMPLOYEE_INFO;"
        msg = self.db.execute(query)
        self.db.commit()
        return list(msg)

    def get_entry_by_date(self, date) -> list:
        values = self.db.execute(f"SELECT * FROM {date};")
        self.db.commit()
        return list(values)

    def search_date_by_range(self, start_dt, end_dt):
        def daterange(date1, date2):
            for n in range(int((date2 - date1).days) + 1):
                yield date1 + timedelta(n)

        w = []
        for dt in daterange(start_dt, end_dt):
            w.append(dateEncodedTable(dt.strftime("%d-%m-%y")))
        cur = self.db.execute(
            "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%'ORDER BY 1;"
        )
        tot = [x[0] for x in cur if x[0] != "EMPLOYEE_INFO"]
        query = "SELECT * FROM {} ;"
        s = set(w) & set(tot)
        p = list(s)
        l = []
        for x in p:
            m = self.db.execute(query.format(x))
            for x in m:
                l.append(x)
        return l

    def get_entry_by_id(self, eid) -> list:
        values = self.db.execute(
            f"SELECT * FROM {self.dbname} WHERE EmployeeId = ?;", [eid]
        )
        self.db.commit()
        return list(values)

    def get_id_date(self, date, eid) -> list:
        date = date[0:6] + "22"
        a = dateEncodedTable(date)
        values = self.db.execute(f"SELECT * FROM {a} WHERE EmployeeId = ? ;", [eid])
        self.db.commit()
        l = list(values)
        return l

    def validate_date(self, date) -> bool:
        values = self.db.execute(
            "SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?;", [date]
        )
        return list(values) != 0

    def search_data_by_id(self, eid: int) -> list:
        cur = self.db.execute(
            "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%'ORDER BY 1;"
        )
        tot = [x[0] for x in cur if x[0] != "EMPLOYEE_INFO"]
        query = "SELECT * FROM {} where EmployeeId=?;"
        l = []
        for x in tot:
            m = self.db.execute(query.format(x), [eid])
            for x in m:
                l.append(x)
        return l

    def search_date_by_id(self, start_dt, end_dt, eid: int):
        def daterange(date1, date2):
            for n in range(int((date2 - date1).days) + 1):
                yield date1 + timedelta(n)

        w = []
        for dt in daterange(start_dt, end_dt):
            w.append(dateEncodedTable(dt.strftime("%d-%m-%y")))
        cur = self.db.execute(
            "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%'ORDER BY 1;"
        )
        tot = [x[0] for x in cur if x[0] != "EMPLOYEE_INFO"]
        query = "SELECT * FROM {} where EmployeeId=?;"
        s = set(w) & set(tot)
        p = list(s)
        l = []
        for x in p:
            m = self.db.execute(query.format(x), [eid])
            for x in m:
                l.append(x)
        return l


db = databases()
