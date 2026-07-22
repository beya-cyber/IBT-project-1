class Account:

    def __init__(self, account_number, holder_name, balance=0.0):
        self.acc_num = account_number
        self.name = holder_name
        self.balance = balance
        self.history = []  # Stack for undoing transactions

    def deposit(self, amount):
        self.balance += amount
        self.history.append(("deposit", amount))

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.history.append(("withdraw", amount))

    def undo_last(self):
        if not self.history:
            return

        action, amount = self.history.pop()
        # Invert the amount: subtract if deposit, add if withdraw
        self.balance += -amount if action == "deposit" else amount

    def __repr__(self):
        return f"Account({self.acc_num}, '{self.name}', Balance: ${self.balance:.2f})"


class AccountRegistry:

    def __init__(self):
        self.accounts = {}

    def add(self, account):
        self.accounts[account.acc_num] = account

    def find(self, account_number):
        return self.accounts.get(account_number)

    def list_all(self):
        return [self.accounts[k] for k in sorted(self.accounts)]


# Usage
registry = AccountRegistry()

acc1 = Account(101, "Alice", 500.0)
acc2 = Account(102, "Bob", 1000.0)

registry.add(acc1)
registry.add(acc2)

acc = registry.find(101)
acc.deposit(200.0)  # Balance: 700.0
acc.withdraw(50.0)  # Balance: 650.0
print("Before undo:", acc)

acc.undo_last()  # Undoes $50 withdrawal -> Balance: 700.0
acc.undo_last()  # Undoes $200 deposit -> Balance: 500.0
print("After undoing twice:", acc)