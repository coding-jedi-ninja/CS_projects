#test part
class Item:
    def __init__(self, name):
        self.name = name

class Inventory:
    def __init__(self):
        """
        type:dict
        Keys are item names (str), values are quantities (int)
        """
        self.stock={
            "Latte":5,
            "Espresso":10,
            "Green Tea":8,
            "Orange Juice":6,
            "Croissant":4,
            "Bagel":7,
            "Muffin":1,
            "Sandwich":0
            }
        
    def check_stock(self,item):
        """
        returns:bool
        if has stock return True, if not, return False
        """
        item_quantity = self.stock.get(item.name, 0)
        if item_quantity > 0:
            print(f"The quantity of {item.name}: {item_quantity}")
            return True
        else:
            print(f"{item.name} is out of stock")
            return False

    def deduct_stock(self,item):
        """
        Only call after check_stock() returns True.
        returns: None
        Reduces stock for item.name by 1.
        """
        if self.check_stock(item):
           self.stock[item.name] -= 1
        
    def restock(self, item_name:str, amount:int):
        """
        returns: None
        Increases stock for item_name by amount.
        """
        self.stock[item_name] = self.stock.get(item_name, 0) + amount

    def stock_report(self):
        """
        Prints all items and their current stock level
        """
        for item_name in self.stock.keys():
            print(f"{item_name} remains:{self.stock[item_name]}")

#test part
inv1 = Inventory()
sandwich = Item("Sandwich")
inv1.stock_report()

inv1.check_stock(sandwich)

# inv1.deduct_stock(sandwich)

# inv1.restock(sandwich.name, 10)
# inv1.check_stock(sandwich)
# inv1.stock_report()
# inv1.deduct_stock(sandwich)
# inv1.stock_report()