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

    def to_dict(self):
        """
        Return a serializable view of the staff member.
        """
        return {
            "staff_id": self.staff_id,
            "name": self.name,
            "telephone": str(self.telephone),
            "password": self.password,
        }


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
            return True
        return False

    def delete_staff(self, staff):
        self.staffs.remove(staff)
        return True

    def update_staff(self, staff):
        for i in range(len(self.staffs)):
            if self.staffs[i].staff_id == staff.staff_id:
                self.staffs[i] = staff
                return True
        return False

    def list_staffs(self):
        """
        Return all staff records as dictionaries sorted by staff ID.
        """
        return [staff.to_dict() for staff in sorted(self.staffs, key=lambda s: s.staff_id)]

    def create_staff(self, name, telephone, password):
        """
        Create, store, and return a new staff member.
        """
        staff = Staff(name.strip(), str(telephone).strip(), password=str(password))
        self.add_staff(staff)
        return staff

    def delete_staff_by_id(self, staff_id):
        """
        Remove one staff member by ID.
        """
        staff = self.get_staff(staff_id)
        if staff is None:
            return False
        self.delete_staff(staff)
        return True

    def update_staff_record(self, staff_id, name=None, telephone=None, password=None):
        """
        Update selected fields for one staff member.
        """
        staff = self.get_staff(staff_id)
        if staff is None:
            return None

        if name is not None and str(name).strip():
            staff.name = str(name).strip()
        if telephone is not None and str(telephone).strip():
            staff.reset_telephone(str(telephone).strip())
        if password is not None and str(password).strip():
            staff.reset_password(str(password))

        self.update_staff(staff)
        return staff

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
