import sqlite3

from functions import dateEncodedTable, logger, today


class databases:
    def __init__(self):
        self.db = sqlite3.connect("main.db", check_same_thread=False)
        self.dbname = dateEncodedTable(today()[0])
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS EMPLOYEE_INFO(Employeeid INTEGER PRIMARY KEY UNIQUE, EmployeeName TEXT, EmployeePosition TEXT, EmployeeProfile TEXT);"
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
        self, employee_id: int, name: str, position: str, profile: str
    ) -> str:
        query = "INSERT INTO EMPLOYEE_INFO(EmployeeId, EmployeeName, EmployeePosition, EmployeeProfile) VALUES (?, ?, ?, ?);"
        try:
            self.db.execute(query, [employee_id, name, position, profile])
            logger.info("New employee added")
            self.db.commit()
            return "SUCCESS"
        except BaseException:
            return "ERROR"

    def update_employee_info(self, eid, name, position, profile) -> None:
        query = "UPDATE EMPLOYEE_INFO SET EmployeeId = ?, EmployeeName = ?, EmployeePosition = ?, EmployeeProfile = ? WHERE EmployeeId = ?;"
        self.db.execute(query, [eid, name, position, profile, eid])
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

    def employee_entry(
        self,
        eid: int,
        ename: str,
        date: str,
        entry: str,
        leave: str = None,
        Time: float = None,
    ) -> None:
        if leave:
            query = f"UPDATE {self.dbname} SET leave=? WHERE entry=? AND EmployeeId=? AND date=? IF DATE IS NULL;"
            self.db.execute(query, [leave, entry, eid, date])
            return self.db.commit()
        query = f"INSERT INTO {self.dbname}(EmployeeId, EmployeeName, Date, Entry, Leave, Time) SELECT ?,?,?,?,?,? WHERE  NOT EXISTS (SELECT * FROM {self.dbname} WHERE EmployeeId=? AND Date=?);"
        self.db.execute(query, [eid, ename, date, entry, leave, Time, eid, date])
        logger.info("Employee entry added into %s", self.dbname)
        self.db.commit()
        return

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

    def get_entry_by_id(self, eid) -> list:
        values = self.db.execute(
            f"SELECT * FROM {self.dbname} WHERE EmployeeId = ?;", [eid]
        )
        self.db.commit()
        return list(values)

    def validate_date(self, date) -> bool:
        cur = self.db.execute(
            "SELECT name FROM sqlite_schema WHERE type = 'table';"
        )
        tot = [x[0] for x in cur if x[0] != "EMPLOYEE_INFO"]
        return date in tot

    def search_data_by_id(self, eid: int) -> list:
        cur = self.db.execute(
            "SELECT name FROM sqlite_schema WHERE type = 'table';"
        )
        tot = [x[0] for x in cur if x[0] != "EMPLOYEE_INFO"]
        query = "SELECT * FROM {} where EmployeeId=?;"
        l = []
        for x in tot:
            m = self.db.execute(query.format(x), [eid])
            for x in m:
                l.append(x)
        return l


db = databases()
