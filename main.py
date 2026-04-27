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
    Staff-only menu for inventory and staff account management.
    """
    while True:
        print("\n" * 10)
        print(f"{'STAFF SYSTEM': ^40}\n")
        print(
            f"{'[1]': >13}  {'VIEW INVENTORY': <23}\n\n"
            f"{'[2]': >13}  {'RESTOCK INVENTORY': <23}\n\n"
            f"{'[3]': >13}  {'VIEW STAFF ACCOUNTS': <23}\n\n"
            f"{'[4]': >13}  {'ADD STAFF ACCOUNT': <23}\n\n"
            f"{'[5]': >13}  {'UPDATE STAFF ACCOUNT': <23}\n\n"
            f"{'[6]': >13}  {'DELETE STAFF ACCOUNT': <23}\n\n"
            f"{'[Q]': >13}  {'QUIT': <23}\n\n\n"
            f"{'[R] RETURN': >40}\n\n"
        )
        choice = input("Please enter your choice: ").lower()

        if choice == "1":
            view_inventory()
        elif choice == "2":
            restock_inventory()
        elif choice == "3":
            view_staff_accounts()
        elif choice == "4":
            add_staff_account()
        elif choice == "5":
            update_staff_account()
        elif choice == "6":
            delete_staff_account()
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


def view_staff_accounts():
    """
    Display all staff account records in a readable table.
    """
    print(f"\n{'STAFF ACCOUNTS': ^70}")
    print("-" * 70)
    print(f"{'STAFF ID': <12}{'NAME': <20}{'TELEPHONE': <18}{'PASSWORD': <20}")
    print("-" * 70)
    for info in staffs.list_staffs():
        print(
            f"{info['staff_id']: <12}"
            f"{info['name'][:18]: <20}"
            f"{info['telephone'][:16]: <18}"
            f"{info['password'][:18]: <20}"
        )
    print("-" * 70)

    while True:
        choice = input("Enter R to return to the staff menu: ").lower()
        if choice == "r":
            return


def add_staff_account():
    """
    Create a new staff account and save it to Excel.
    """
    print(f"\n{'ADD STAFF ACCOUNT': ^40}")
    while True:
        name = input("Enter the new staff member's name or R to return: ").strip()
        if name.lower() == "r":
            return
        if name:
            break
        print("Invalid input, please try again!")

    while True:
        telephone = input("Enter the telephone number: ").strip()
        if telephone.lower() == "r":
            return
        if telephone.isdigit() and int(telephone) > 0:
            break
        print("Invalid input, please try again!")

    while True:
        password = getpass("Enter the password: ").strip()
        print()
        if password.lower() == "r":
            return
        if password:
            break
        print("Invalid input, please try again!")

    staff = staffs.create_staff(name, telephone, password)
    staffs.save_to_excel()
    print(f"Staff account created. New staff ID: {staff.staff_id}")


def update_staff_account():
    """
    Update one existing staff account.
    """
    print(f"\n{'UPDATE STAFF ACCOUNT': ^40}")
    while True:
        staff_id = input("Enter the staff ID to update or R to return: ").strip()
        if staff_id.lower() == "r":
            return
        if staffs.check_staff(staff_id):
            break
        print("Invalid input, please try again!")

    staff = staffs.get_staff(staff_id)
    print("Press Enter to keep the current value.")

    new_name = input(f"Name [{staff.name}]: ").strip()
    new_telephone = input(f"Telephone [{staff.telephone}]: ").strip()
    new_password = getpass("Password [hidden]: ").strip()
    print()

    staffs.update_staff_record(
        staff_id,
        name=new_name or None,
        telephone=new_telephone or None,
        password=new_password or None,
    )
    staffs.save_to_excel()
    print("Staff account updated.")


def delete_staff_account():
    """
    Delete one staff account after confirmation.
    """
    print(f"\n{'DELETE STAFF ACCOUNT': ^40}")
    while True:
        staff_id = input("Enter the staff ID to delete or R to return: ").strip()
        if staff_id.lower() == "r":
            return
        if staffs.check_staff(staff_id):
            break
        print("Invalid input, please try again!")

    if len(staffs.staffs) == 1:
        print("You must keep at least one staff account in the system.")
        return

    staff = staffs.get_staff(staff_id)
    confirm = input(
        f"Delete staff account for {staff.name} ({staff.staff_id})? Enter Y to confirm: "
    ).strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return

    staffs.delete_staff_by_id(staff_id)
    staffs.save_to_excel()
    print("Staff account deleted.")


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
