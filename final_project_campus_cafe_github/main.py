"""
Campus Cafe terminal application controller.

This file wires together the chosen Week 1 classes into the full Week 2/3
terminal app. It is responsible for the menu loop, input validation, checkout,
staff access, and session summary reporting.
"""

from backend.menu import MenuItem, Menu
from backend.order import Order
from backend.inventory_ShuranRyu import Inventory
from backend.customer import Customer, Customers
from backend.staff import Staff, Staffs
from getpass import getpass
from datetime import datetime

MENU = Menu()  # Load menu from Excel.
order = Order(MENU)  # Track the current customer order.
staffs = Staffs()  # Load staff credentials for the hidden staff mode.
session_orders = {}  # Track completed orders for the session summary.


def main_menu():
    """
    Display the main menu and route each choice to its handler.
    """
    while True:
        print("\n" * 10)
        print(f"{'CAMPUS CAFÉ': ^40}\n")
        print(
            f"{'[1]': >13}  {'VIEW MENU': <23}\n\n"
            f"{'[2]': >13}  {'ORDER ITEM': <23}\n\n"
            f"{'[3]': >13}  {'VIEW CART': <23}\n\n"
            f"{'[4]': >13}  {'CHECKOUT': <23}\n\n"
            f"{'[s]': >13}  {'STAFF MODE (BONUS)': <23}\n\n"
            f"{'[q]': >13}  {'QUIT': <23}\n\n"
        )

        choice = input("Please enter your choice: ").lower()

        if choice == "1":
            view_menu()
        elif choice == "2":
            order_item()
        elif choice == "3":
            view_cart()
        elif choice == "4":
            checkout()
        elif choice == "q":
            quit()
        elif choice == "s" or choice == "staff":
            # Visible bonus feature for inventory management.
            login_staff_system()
        else:
            print("Invalid input. Please enter 1, 2, 3, 4, s, or q.")


def view_menu():
    """
    Display the full menu until the user chooses to return.
    """
    MENU.display_menu()
    while True:
        choice1 = input("Enter R to return to homepage: ").lower()
        if choice1 == "r":
            return


def order_item():
    """
    Prompt for an item name and quantity, then add available units to the cart.
    """
    while True:
        item_name = input(
            "Enter the name of food you would like to order or R to return to homepage: "
        ).lower().strip()

        if item_name == "r":
            return

        item = MENU.get_item(item_name)
        if item is None:
            print("Invalid input, please try again!")
            continue

        while True:
            num = input(f"Enter the number of {item.name} you would like to order: ")

            try:
                num_int = int(num)
                if num_int <= 0:
                    print("Invalid input, please try again!")
                    continue
                break
            except ValueError:
                print("Invalid input, please try again!")
                continue

        inventory = Inventory()
        counter = 0
        for _ in range(num_int):
            if inventory.check_stock(item):
                counter += 1
                order.add_to_order(item)
                inventory.deduct_stock(item)
                inventory.save_to_excel()
            else:
                print("Sorry, this item is out of stock, please choose other item.")
                break
        print(f"You have ordered {counter} {item.name}.")


def delete_item():
    """
    Remove one or more items from the cart and restore the inventory stock.
    """
    while True:
        name = input(
            "Enter the name of the food you would like to delete or R to return to homepage: "
        ).lower().strip()
        if name == "r":
            return

        item = MENU.get_item(name)
        if item is None:
            print("Invalid input, please try again!")
            continue

        if item in order.items:
            while True:
                num = input(f"Enter the number of {item.name} you would like to delete: ")

                try:
                    num_int = int(num)
                    if num_int <= 0:
                        print("Invalid input, please try again!")
                        continue
                    break
                except ValueError:
                    print("Invalid input, please try again!")
                    continue

            num_max = min(num_int, order.get_items_num()[item])
            for _ in range(num_max):
                order.remove_from_order(item)
                inventory = Inventory()
                inventory.restore_stock(item)
                inventory.save_to_excel()
            print(f"You have deleted {num_max} {item.name}.")
        else:
            print("You didn't order this item or you have already deleted all of this item.")


def view_cart():
    """
    Show the current cart and allow the user to delete items if needed.
    """
    print(f"{'YOUR ORDER': ^40}")
    order.display_order()
    while True:
        choice1 = input("Enter D to delete an item or R to return to main menu: ").lower()
        if choice1 == "d":
            delete_item()
            print(f"{'YOUR ORDER': ^40}")
            order.display_order()
        elif choice1 == "r":
            return
        else:
            print("Invalid input, please try again!")


def checkout():
    """
    Validate checkout, award loyalty points, print a receipt, and save the order.
    """
    if len(order.items) == 0:
        print("Sorry, you didn't order anything.")
        return

    subtotal = order.get_total()
    total_before_tax = order.get_total_after_discount()
    discount = subtotal - total_before_tax
    tax = order.TAX_RATE * total_before_tax
    total = total_before_tax + tax

    while True:
        telephone = input("Enter your telephone number: ")

        try:
            telephone_int = int(telephone)
            if telephone_int <= 0:
                print("Invalid input, please try again.")
                continue
            break
        except ValueError:
            print("Invalid input, please try again.")

    customers = Customers()
    if customers.check_customer(telephone_int):
        customer = customers.get_customer(telephone_int)
        customer.earn_points(total)
        customers.update_customer(customer)
    else:
        customer = Customer(telephone_int)
        customer.earn_points(total)
        customers.add_customer(customer)

    customers.save_to_excel()

    print("Money received.")
    print()
    print("=" * 40)
    print()
    print(f"{'CAMPUS CAFE': ^40}")
    print()
    print(f"{'4 N Second Street, San Jose, CA 95113': ^40}")
    print()
    print("-" * 40)
    print(
        f"Date: {datetime.now().strftime('%Y-%m-%d'): <20}"
        f"Time: {datetime.now().strftime('%H:%M:%S')}"
    )
    print(f"Customer ID: {customer.customer_id}    Points: {customer.points}")
    order.display_order()
    print(f"{'Subtotal:': <35}${subtotal:.2f}")
    print("-" * 40)
    if discount != 0:
        print(f"{'Daily special discount:': <35}${discount:.2f}")
    print(f"{'Tax:': <35}${tax:.2f}")
    print("-" * 40)
    print(f"{'Total:': <35}${total:.2f}")
    print("-" * 40)
    print(f"{'Thank you for dining with us!': ^40}")
    print("=" * 40)

    order.save_to_excel()
    session_orders[len(session_orders)] = {"Total": total, "Items": str(order)}
    order.clear_order()


def login_staff_system():
    """
    Authenticate staff before opening the staff inventory menu.
    """
    while True:
        id = input("Enter your staff id or R to return to homepage: ").lower()

        if id == "r":
            return

        if not staffs.check_staff(id):
            print("Invalid input, please try again.")
            continue

        staff = staffs.get_staff(id)
        while True:
            pwd = getpass("Enter the password or R to return to homepage:")
            print()

            if pwd == "r":
                return
            elif pwd == staff.password:
                staff_menu()
                return
            else:
                print("Invalid input, please try again!")


def staff_menu():
    """
    Staff-only menu for viewing and restocking inventory.
    """
    while True:
        print("\n" * 10)
        print(f"{'STAFF SYSTEM': ^40}\n")
        print(
            f"{'[1]': >13}  {'VIEW INVENTORY': <23}\n\n"
            f"{'[2]': >13}  {'RESTOCK INVENTORY': <23}\n\n"
            f"{'[Q]': >13}  {'QUIT': <23}\n\n\n"
            f"{'[R] RETURN': >40}\n\n"
        )
        choice = input("Please enter your choice: ").lower()

        if choice == "1":
            view_inventory()
        elif choice == "2":
            restock_inventory()
        elif choice == "q":
            quit()
        elif choice == "r":
            return
        else:
            print("Invalid input, please try again!")


def view_inventory():
    """
    Display the full inventory report for staff users.
    """
    inventory = Inventory()
    inventory.stock_report()
    while True:
        choice1 = input("Enter R to return to staff menu: ").lower()
        if choice1 == "r":
            break


def restock_inventory():
    """
    Prompt staff to restock one menu item by a chosen amount.
    """
    inventory = Inventory()
    while True:
        name = input(
            "Enter the name of the food you would like to restock or R to return to staff menu: "
        ).strip().title()
        if name == "R":
            break

        if name not in inventory.stock:
            print("Invalid input, please try again!")
            continue

        while True:
            num = input(f"Enter the number of {name} you would like to restock: ")

            try:
                num_int = int(num)
                if num_int <= 0:
                    print("Invalid input, please try again!")
                    continue

                inventory.restock(name, num_int)
                inventory.save_to_excel()
                print(f"You have restocked {num_int} {name}s.")
                break
            except ValueError:
                print("Invalid input, please try again!")
                continue


def quit():
    """
    Print the session summary and exit the program.
    """
    print("\n" * 10)
    print(f"{'CAMPUS CAFÉ': ^40}")
    session_orders_total = 0
    for _, info in session_orders.items():
        session_orders_total += info["Total"]
        print(info["Items"])

    print(f"{len(session_orders)} orders completed, {session_orders_total:.2f} dollars earned.")
    exit()


if __name__ == "__main__":
    main_menu()
