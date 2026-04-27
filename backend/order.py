from datetime import datetime

import pandas as pd

from backend.menu import Menu
from backend.paths import data_file


class Order:
    """
    Represents a customer's order, storing items and handling checkout.
    """

    def __init__(self, menu, filename="Orders.xlsx"):
        self.filename = filename
        self.items = []  # list of MenuItem objects in the order
        self.menu = menu
        self.TAX_RATE = 0.1  # 10% tax rate

    def __str__(self):
        """
        Return a formatted string of the order with item names, quantities, and prices.
        """
        order = f"{'-' * 40}\n  {'Item': <26}{'Num'}{'Price': >8}\n{'-' * 40}\n"
        item_counts = self.get_items_num()

        for item, quantity in item_counts.items():
            order += f"* {item.name: <25}  {quantity}    ${item.price * quantity: >5.2f}\n"

        order += f"{'-' * 40}\n"
        order += f"{'Total:': <35}${self.get_total_after_discount():.2f}\n"
        order += f"{'-' * 40}\n"
        return order

    def add_to_order(self, item):
        """
        Add a MenuItem to the order.
        """
        self.items.append(item)

    def remove_from_order(self, item):
        """
        Remove one instance of a MenuItem from the order.
        """
        self.items.remove(item)

    def get_total(self):
        """
        Calculate and return the subtotal (before tax) of all items.
        """
        total = 0.00
        for item in self.items:
            total += item.price
        return total

    def get_total_after_discount(self):
        """
        Calculate and return the subtotal after the daily special discount.
        """
        total = 0.00
        for item in self.items:
            if item == self.menu.special_item:
                total += item.price * (1 - self.menu.special_discounted_rate)
            else:
                total += item.price
        return total

    def display_order(self):
        """
        Print the order summary to the console.
        """
        print(self)

    def clear_order(self):
        """
        Clear all items from the order.
        """
        self.items = []

    def get_items_num(self):
        """
        Count how many of each MenuItem appears in the order.
        """
        item_counter = {}
        for item in self.items:
            if item not in item_counter:
                item_counter[item] = 1
            else:
                item_counter[item] += 1
        return item_counter

    def save_to_excel(self):
        """
        Save the completed order to Excel with timestamps and item quantities.
        """
        if len(self.items) == 0:
            return

        order_path = data_file(self.filename)

        if order_path.exists():
            df_old = pd.read_excel(order_path)
            if df_old.empty:
                order_id = 1
            else:
                order_id = int(df_old["order_id"].max()) + 1
        else:
            df_old = None
            order_id = 1

        row = {
            "order_id": order_id,
            "total": self.get_total_after_discount() * (self.TAX_RATE + 1),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
        }

        for item, quantity in self.get_items_num().items():
            row[item.name] = quantity

        df = pd.DataFrame([row])
        if df_old is not None:
            df = pd.concat([df_old, df], ignore_index=True)
        df.to_excel(order_path, index=False)


if __name__ == "__main__":
    menu = Menu()
    order = Order(menu)
    americano = menu.get_item("Americano")
    chicken_salad = menu.get_item("chicken salad")

    order.add_to_order(americano)
    order.add_to_order(americano)
    order.add_to_order(chicken_salad)
    order.remove_from_order(americano)
    print(f"Current total: ${order.get_total():.2f}")
    order.display_order()
    order.clear_order()
    print("Cart after clear:")
    order.display_order()
