#Lets import our main module and begin our object

class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        self.balance -= amount
    def statement(self):
        print(f"{self.owner} {self.balance})

Beya = Account("Beya", 1000)
Beya.deposit(1030)
Beya.withdraw(10)
Beya.deposit(1220)
Beya.withdraw(520)
print(Beya.balance)