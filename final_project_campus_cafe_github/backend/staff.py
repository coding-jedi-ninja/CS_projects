import pandas as pd

from backend.paths import data_file


class Staff:
    """
    Represents one staff member who can access the restock system.
    """

    counter = 0

    def __init__(self, name, telephone, id=None, password=""):
        if id is not None:
            self.staff_id = id
            Staff.counter = max(Staff.counter, int(id))
        else:
            Staff.counter += 1
            self.staff_id = str(Staff.counter).zfill(9)

        self.name = name
        self.telephone = telephone
        self.password = password

    def __str__(self):
        return f"{self.staff_id}  {self.name}  {self.telephone}  {self.password}\n"

    def reset_telephone(self, telephone):
        self.telephone = telephone

    def reset_password(self, password):
        self.password = password


class Staffs:
    """
    Collection class that loads, stores, and updates Staff records.
    """

    def __init__(self, filename="Staffs.xlsx"):
        self.filename = filename
        self.staffs = self.load_from_excel()

    def check_staff(self, id):
        for staff in self.staffs:
            if str(staff.staff_id) == str(id):
                return True
        return False

    def get_staff(self, id):
        for staff in self.staffs:
            if str(staff.staff_id) == str(id):
                return staff
        return None

    def add_staff(self, staff):
        if not self.check_staff(staff.staff_id):
            self.staffs.append(staff)

    def delete_staff(self, staff):
        self.staffs.remove(staff)

    def update_staff(self, staff):
        for i in range(len(self.staffs)):
            if self.staffs[i].staff_id == staff.staff_id:
                self.staffs[i] = staff

    def load_from_excel(self):
        staff_path = data_file(self.filename)
        if not staff_path.exists():
            return []

        df = pd.read_excel(staff_path)
        result = []
        for _, info in df.iterrows():
            result.append(
                Staff(
                    info["name"],
                    info["telephone"],
                    str(info["staff_id"]).zfill(9),
                    info["password"],
                )
            )
            Staff.counter = max(Staff.counter, int(info["staff_id"]))
        return result

    def save_to_excel(self):
        rows = []
        for staff in self.staffs:
            rows.append(
                {
                    "staff_id": staff.staff_id,
                    "name": staff.name,
                    "telephone": staff.telephone,
                    "password": staff.password,
                }
            )
        df = pd.DataFrame(rows, columns=["staff_id", "name", "telephone", "password"])
        df.to_excel(data_file(self.filename), index=False)


if __name__ == "__main__":
    elena = Staff("elena", 6693733975)
    print(elena)
    elena.reset_password("123456")
    print(elena)

    staffs = Staffs()
    print(staffs.check_staff("000000001"))
    staffs.add_staff(elena)
    print(staffs.check_staff("000000001"))
    elena = staffs.get_staff("000000001")
    elena.reset_password("abcdef")
    print(elena)
    staffs.update_staff(elena)
    staffs.save_to_excel()
