from remote.remote_decorator import remote_class
from remote.remote_base_class import RemoteObject
from remote.remote_metaclass import RemoteMetaclass


# Method 1: decorator
@remote_class
class Supplier:

# # Method 2: Inherit framework's base class
# class Supplier(RemoteObject):

# # Method 3: Specify metaclass = framework's metaclass
# class Supplier(metaclass=RemoteMetaclass):

    def __init__(self, name):
        self.name = name
        self.inventory = {"Tomatoes": 100, "Cheese": 50, "Bread": 200}

    def supply(self, item, quantity):
        if item in self.inventory and self.inventory[item] >= quantity:
            self.inventory[item] -= quantity
            return f"Supplied {quantity} of {item}"
        else:
            return f"Cannot supply {quantity} of {item}"


# Method 1: decorator
@remote_class
class Restaurant:

# # Method 2: Inherit framework's base class
# class Restaurant(RemoteObject):

# # Method 3: Specify metaclass = framework's metaclass
# class Restaurant(metaclass=RemoteMetaclass):


    def __init__(self, name):
        self.name = name
        self.menu = ["Pizza", "Burger", "Salad"]

    def display_menu(self):
        return f"{self.name}'s Menu:\n" + "\n".join(f"- {item}" for item in self.menu)

    def take_order(self, customer, item):
        if item in self.menu:
            return f"Order received: {item} for {customer}"
        else:
            return f"Sorry, {item} is not on our menu."

    def order_supplies(self, supplier, item, quantity):
        result = supplier.supply(item, quantity)
        return f"{self.name} ordered {quantity} of {item} from {supplier.name}: {result}"

class Customer:
    def __init__(self, name):
        self.name = name
        self.order_history = []

    def place_order(self, restaurant, item):
        order_result = restaurant.take_order(self.name, item)
        if "Order received" in order_result:
            self.order_history.append((restaurant.name, item))
            return f"{self.name} has ordered {item} from {restaurant.name}"
        else:
            return f"{self.name} failed to order {item}: {order_result}"

    def view_order_history(self):
        return f"{self.name}'s Order History:\n" + "\n".join(f"- {item} from {restaurant}" for restaurant, item in self.order_history)


# Usage: uncomment the method you want to try and run main.py
# Note: All methods achieve the same result
if __name__ == "__main__":
    # Create remote instances
    restaurant = Restaurant("Tasty Bites")
    supplier = Supplier("Fresh Supplies Co.")
    customer = Customer("Alice")

    # Customer interacts with Restaurant
    print("\n", restaurant.display_menu())
    print("\n", customer.place_order(restaurant, "Pizza"))
    print("\n", customer.place_order(restaurant, "Sushi"))
    print("\n", customer.view_order_history())

    # Restaurant interacts with Supplier
    print("\n", restaurant.order_supplies(supplier, "Tomatoes", 20))
    print("\n", restaurant.order_supplies(supplier, "Cheese", 60))