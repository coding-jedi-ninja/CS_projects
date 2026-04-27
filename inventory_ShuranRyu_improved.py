"""
Inventory management for Campus Cafe.

This module was adapted from the Week 1 inventory implementation shared by
Shuran and Ryu. The original logic for checking, deducting, and restocking
stock was preserved, then extended so it works with the rest of our system:

- inventory data is loaded from and saved to Excel,
- MenuItem objects from backend.menu are accepted directly,
- deleted cart items can restore stock,
- file paths are shared with the deployment-safe data helper.
"""

from backend.menu import Menu
from backend.paths import data_file
import pandas as pd


class Inventory:
    """
    Track stock counts for each menu item and persist them to Excel.
    """

    def __init__(self, filename="Inventory.xlsx"):
        """
        Load the inventory from the given Excel file.

        Args:
            filename (str): Excel file used for inventory persistence.
        """
        self.filename = filename
        self.stock = self.load_from_excel()

    def __str__(self):
        """
        Return a printable inventory report.

        Returns:
            str: formatted inventory table
        """
        inventory = f"{'-' * 40}\n"
        for item_name, quantity in self.stock.items():
            inventory += f"* {item_name: <25}{int(quantity): >13d}\n"
        inventory += f"{'-' * 40}\n"
        return inventory

    def check_stock(self, item):
        """
        Check whether at least one unit of the given item is available.

        Args:
            item (MenuItem): the menu item being ordered

        Returns:
            bool: True when stock is available, otherwise False
        """
        return self.stock.get(item.name, 0) > 0

    def deduct_stock(self, item):
        """
        Reduce stock for an item by one unit.

        This should only be called after ``check_stock(item)`` returns True.

        Args:
            item (MenuItem): the menu item being ordered
        """
        if self.check_stock(item):
            self.stock[item.name] -= 1

    def restore_stock(self, item):
        """
        Add one unit back to stock when an item is removed from the cart.

        Args:
            item (MenuItem): the menu item being restored
        """
        self.stock[item.name] = self.stock.get(item.name, 0) + 1

    def restock(self, item_name, amount):
        """
        Increase stock for an item by the given amount.

        Args:
            item_name (str): item name in the stock dictionary
            amount (int): quantity to add
        """
        self.stock[item_name] = self.stock.get(item_name, 0) + amount

    def stock_report(self):
        """
        Print the current inventory in a user-friendly format.
        """
        print(f"{'INVENTORY': ^40}")
        print(self)

    def load_from_excel(self):
        """
        Load stock data from Excel into a dictionary.

        Returns:
            dict[str, int]: mapping of item name to stock quantity
        """
        inventory_path = data_file(self.filename)
        if not inventory_path.exists():
            return {}

        df = pd.read_excel(inventory_path)
        result = {}
        for _, row in df.iterrows():
            result[row["Item Name"]] = int(row["Stock Numbers"])
        return result

    def save_to_excel(self):
        """
        Persist the current stock dictionary to Excel.
        """
        df = pd.DataFrame(
            list(self.stock.items()),
            columns=["Item Name", "Stock Numbers"],
        )
        df.to_excel(data_file(self.filename), index=False)


if __name__ == "__main__":
    inventory = Inventory()
    menu = Menu()
    sandwich = menu.get_item("Chicken Sandwich")

    print(inventory)
    print(f"In stock before deduct: {inventory.check_stock(sandwich)}")
    inventory.deduct_stock(sandwich)
    inventory.restore_stock(sandwich)
    inventory.restock(sandwich.name, 2)
    inventory.stock_report()
