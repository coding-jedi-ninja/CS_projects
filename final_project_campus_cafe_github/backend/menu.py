import pandas as pd
import random

from backend.paths import data_file


def _normalize_name(name):
    """
    Normalize an item name for case-insensitive, space-insensitive matching.
    """
    return name.lower().strip().replace(" ", "")


def _format_menu_items(menu_items, special_item=None, discount_rate=None):
    """
    Build a grouped menu string for either the Menu object or the contract wrapper.
    """
    category_order = ["Drinks", "Desserts", "Salads", "Sandwiches"]
    categories = []

    for category in category_order:
        if any(item.category == category for item in menu_items):
            categories.append(category)

    for item in menu_items:
        if item.category not in categories:
            categories.append(item.category)

    result = f"{'MENU':=^40}\n"
    for category in categories:
        result += f"{category:-^40}\n"
        for item in menu_items:
            if item.category == category:
                result += str(item)
        result += f"{'-' * 40}\n\n"

    if special_item is not None and discount_rate is not None:
        result += f"Daily special: {special_item.name}\n"
        result += f"Discounted rate: {discount_rate:.0%}\n"
    result += f"{'=' * 40}\n"
    return result


class MenuItem:
    """
    Represents a single menu item with name, price, and category.
    """

    def __init__(self, name, price, category):
        """
        Initialize a MenuItem.

        Args:
            name (str): the name of the item
            price (float): the price of the item
            category (str): the category (e.g. "Drinks", "Desserts")
        """
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        """
        Return formatted string with name and price.

        Returns:
            str: formatted string like "Americano                    $5.00"
        """
        return f"{self.name: <34}${self.price: >5.2f}\n"


class Menu:
    """
    Represents the full cafe menu, supporting display and search.
    """

    def __init__(self, filename="Menu.xlsx", rate=0.2):
        """
        Initialize the Menu.

        Args:
            filename (str): Excel file that stores menu data
            rate (float): discount rate applied to the daily special
        """
        self.filename = filename
        self.menu = self.load_from_excel()
        self.special_item = self.daily_special()
        self.special_discounted_rate = rate

    def __str__(self):
        return _format_menu_items(
            self.menu,
            special_item=self.special_item,
            discount_rate=self.special_discounted_rate,
        )

    def display_menu(self):
        """
        Print the menu to the console, grouped by category.
        """
        print(self)

    def get_item(self, name):
        """
        Search for a menu item by name.

        Args:
            name (str): the name of the item to search for

        Returns:
            MenuItem or None: the matching item, or None if not found
        """
        normalized_name = _normalize_name(name)
        for item in self.menu:
            if _normalize_name(item.name) == normalized_name:
                return item
        return None

    def daily_special(self):
        """
        Pick one daily special for the current session.

        Returns:
            MenuItem or None: randomly selected special item
        """
        if not self.menu:
            return None
        return random.choice(self.menu)

    def load_from_excel(self):
        """
        Load menu items from Excel into MenuItem objects.
        """
        menu_path = data_file(self.filename)
        if not menu_path.exists():
            return []

        df = pd.read_excel(menu_path)
        menu = []
        for _, row in df.iterrows():
            menu.append(MenuItem(row["item_name"], row["price"], row["category"]))
        return menu

    def save_to_excel(self):
        """
        Save the current menu items back to Excel.
        """
        rows = []
        for item in self.menu:
            rows.append([item.name, item.price, item.category])
        df = pd.DataFrame(rows, columns=["item_name", "price", "category"])
        df.to_excel(data_file(self.filename), index=False)


MENU_MANAGER = Menu()
MENU = MENU_MANAGER.menu


def display_menu(menu):
    """
    Contract-compatible standalone menu display function.
    """
    print(_format_menu_items(menu))


def get_item(menu, name):
    """
    Contract-compatible standalone menu lookup function.
    """
    normalized_name = _normalize_name(name)
    for item in menu:
        if _normalize_name(item.name) == normalized_name:
            return item
    return None


if __name__ == "__main__":
    menu = Menu()
    menu.display_menu()
    print()
    print(menu.get_item("fruitsalad"))
    print()
    special = menu.daily_special()
    if special is not None:
        print(f"Daily special: {special.name} - ${special.price:.2f}")
    print()
    display_menu(MENU)
    print(get_item(MENU, "Latte"))
