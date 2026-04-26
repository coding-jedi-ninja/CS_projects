import random
import string

import pandas as pd

from backend.paths import data_file


class Customer:
    """
    Represents one customer in the loyalty program.
    """

    counter = 0

    def __init__(self, telephone, name="", points=0, id=None):
        if id is not None:
            self.customer_id = id
            Customer.counter = max(Customer.counter, int(id))
        else:
            Customer.counter += 1
            self.customer_id = str(Customer.counter).zfill(9)

        if name != "":
            self.name = name
        else:
            self.name = "".join(random.choices(string.ascii_letters + string.digits, k=9))

        self.telephone = telephone
        self.points = points
        self.earn_point_policy = 5
        self.use_point_policy = 1

    def __str__(self):
        return f"{self.customer_id}  {self.name}  {self.telephone}  {self.points:.2f}\n"

    def earn_points(self, consuming):
        """
        Award one point for every configured spending threshold.
        """
        self.points += consuming // self.earn_point_policy

    def use_points(self, consuming):
        """
        Deduct points using the configured points policy.
        """
        self.points -= consuming * self.use_point_policy

    def display_points(self):
        print(self)

    def reset_name(self, name):
        self.name = name

    def reset_telephone(self, num):
        self.telephone = num


class Customers:
    """
    Collection class that loads, stores, and updates Customer records.
    """

    def __init__(self, filename="Customers.xlsx"):
        self.filename = filename
        self.customers = self.load_from_excel()

    def check_customer(self, telephone):
        for customer in self.customers:
            if customer.telephone == telephone:
                return True
        return False

    def get_customer(self, telephone):
        for customer in self.customers:
            if customer.telephone == telephone:
                return customer
        return None

    def add_customer(self, customer):
        if not self.check_customer(customer.telephone):
            self.customers.append(customer)

    def update_customer(self, customer):
        for i in range(len(self.customers)):
            if self.customers[i].customer_id == customer.customer_id:
                self.customers[i] = customer

    def load_from_excel(self):
        customer_path = data_file(self.filename)
        if not customer_path.exists():
            return []

        df = pd.read_excel(customer_path)
        result = []
        for _, row in df.iterrows():
            result.append(
                Customer(
                    row["telephone"],
                    row["name"],
                    row["points"],
                    str(row["customer_id"]).zfill(9),
                )
            )
            Customer.counter = max(Customer.counter, int(row["customer_id"]))
        return result

    def save_to_excel(self):
        rows = []
        for customer in self.customers:
            rows.append([customer.customer_id, customer.name, customer.telephone, customer.points])
        df = pd.DataFrame(rows, columns=["customer_id", "name", "telephone", "points"])
        df.to_excel(data_file(self.filename), index=False)


if __name__ == "__main__":
    customers = Customers()
    print(customers.check_customer(123456789))
    nobody = Customer(123456789)
    customers.add_customer(nobody)
    nobody1 = customers.get_customer(123456789)
    nobody1.earn_points(100)
    customers.update_customer(nobody1)
    print(nobody1)
    customers.save_to_excel()
