#This is a simple implementation of a Addis Bank account class in Python. The class has an owner, account number, and balance. The balance is a private attribute, and it can be accessed through the statement property. The deposit method allows adding funds to the account, while the withdraw method allows removing funds, with checks for sufficient balance.


class Account:
    def __init__(self, owner, account_no, balance):
        self.owner = owner
        self.account_no = account_no
        self.__balance = balance
        @property
    def statement(self): 
        return self.__balance 
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += amount
    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount


beya = Account("Beya", "123456789", 1000)
beya.deposit(500)
print(beya.statement)  # Output: 1500

        
