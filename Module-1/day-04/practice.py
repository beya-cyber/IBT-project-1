class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def describe(self):
        print(f"'{self.title}' by {self.author} ({self.pages} pages)")

b1 = Book("Fikir Eske Mekabr", "Haddis Alemayehu", 500)
b2 = Book("Alemenor", "DR Dawit Wendmagegn", 352)
b1.describe()
b2.describe()


print("\n--- Exercises 2, 3 & 4 ---")
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.__quantity = max(0, quantity)

    @property
    def quantity(self):
        return self.__quantity

    def restock(self, n):
        if n > 0:
            self.__quantity += n

    def sell(self, n):
        if n <= 0:
            print("Quantity must be positive.")
        elif n > self.__quantity:
            print(f"Cannot sell {n}: Only {self.__quantity} in stock.")
        else:
            self.__quantity -= n


p1 = Product("Laptop", 45000, 10)
p1.restock(5)
p1.sell(3)
print(f"{p1.name} stock:", p1.quantity)
p1.sell(20)  # Validation test



print("\n--- Exercise 5 ---")
prod1 = Product("Item A", 100, 5)
prod2 = Product("Item B", 200, 10)
prod3 = Product("Item C", 300, 15)

# Change only prod1
prod1.sell(2)

print(f"Prod 1 Quantity: {prod1.quantity} (Updated)")
print(f"Prod 2 Quantity: {prod2.quantity} (Unaffected)")
print(f"Prod 3 Quantity: {prod3.quantity} (Unaffected)")