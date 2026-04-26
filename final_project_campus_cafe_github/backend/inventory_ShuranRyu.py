from backend.menu import Menu
from backend.paths import data_file
import pandas as pd


class Inventory:
    """
    Inventory class adapted from Shuran and Ryu's Week 1 implementation.

    Our integration kept the original stock contract methods and extended the
    class so it works with MenuItem objects, Excel persistence, cart deletion,
    and deployment-safe data paths.
    """

    def __init__(self, filename="Inventory.xlsx"):
        """
        Initialize the inventory from Excel.

        Args:
            filename (str): Excel file that stores inventory stock counts
        """
        self.filename = filename
        self.stock = self.load_from_excel()

    def __str__(self):
        inventory = f"{'-' * 40}\n"
        for item_name, quantity in self.stock.items():
            inventory += f"* {item_name: <25}{int(quantity): >13d}\n"
        inventory += f"{'-' * 40}\n"
        return inventory

    def check_stock(self, item):
        """
        Return True if the item has stock remaining, otherwise False.
        """
        item_quantity = self.stock.get(item.name, 0)
        return item_quantity > 0

    def deduct_stock(self, item):
        """
        Reduce stock by one after a successful stock check.
        """
        if self.check_stock(item):
            self.stock[item.name] -= 1

    def restore_stock(self, item):
        """
        Increase stock by one when an item is removed from the cart.
        """
        self.stock[item.name] = self.stock.get(item.name, 0) + 1

    def restock(self, item_name, amount):
        """
        Increase stock for an item by the given amount.
        """
        self.stock[item_name] = self.stock.get(item_name, 0) + amount

    def stock_report(self):
        """
        Print all items and their current stock level.
        """
        print(f"{'INVENTORY': ^40}")
        print(self)

    def load_from_excel(self):
        """
        Convert the Inventory.xlsx sheet into a stock dictionary.
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
        Save the stock dictionary back to Excel.
        """
        df = pd.DataFrame(list(self.stock.items()), columns=["Item Name", "Stock Numbers"])
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
