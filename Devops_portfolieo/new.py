# =====================================================================
# 1. BASE CLASS (Your original Account class)
# =====================================================================
class Account:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        else:
            print(f"Account {self.account_number}: Insufficient funds!")
            return False

    def statement(self):
        return f"Standard Account {self.account_number} | Balance: ${self.balance:.2f}"


# =====================================================================
# 2. SAVINGS ACCOUNT (Inherits from Account)
# =====================================================================
class SavingsAccount(Account):
    def __init__(self, account_number, balance, rate):
        # super().__init__ calls the constructor of the parent Account class
        super().__init__(account_number, balance)
        self.rate = rate  # Interest rate (e.g., 0.05 for 5%)

    def add_interest(self):
        """Calculates interest and deposits it directly into the account."""
        interest = self.balance * self.rate
        self.deposit(interest)
        print(f"Added ${interest:.2f} interest to Savings Account {self.account_number}")

    # Overriding the statement() method to label the account type
    def statement(self):
        return f"Savings Account {self.account_number}  | Balance: ${self.balance:.2f} (Interest Rate: {self.rate * 100:.1f}%)"


# =====================================================================
# 3. CURRENT ACCOUNT (Inherits from Account)
# =====================================================================
class CurrentAccount(Account):
    def __init__(self, account_number, balance, overdraft):
        super().__init__(account_number, balance)
        self.overdraft = overdraft  # Allowed negative balance limit (e.g., 500)

    # Overriding withdraw() to allow spending into the overdraft limit
    def withdraw(self, amount):
        if amount <= self.balance + self.overdraft:
            self.balance -= amount
            return True
        else:
            print(f"Current Account {self.account_number}: Overdraft limit of ${self.overdraft:.2f} exceeded!")
            return False

    # Overriding the statement() method to label the account type
    def statement(self):
        return f"Current Account {self.account_number}  | Balance: ${self.balance:.2f} (Overdraft Limit: ${self.overdraft:.2f})"


# =====================================================================
# 5. POLYMORPHIC LOOP (Testing the code)
# =====================================================================
if __name__ == "__main__":
    # Create a mixed list of different account objects
    accounts_list = [
        Account("ACT-101", 1000.00),
        SavingsAccount("SAV-202", 5000.00, 0.05),  # 5% interest
        CurrentAccount("CUR-303", 200.00, 500.00)   # $500 overdraft limit
    ]

    print("--- Running Special Account Actions ---")
    # Call a specific method on the Savings Account (index 1)
    accounts_list[1].add_interest()

    # Try to withdraw past the regular balance but within overdraft limit on Current Account (index 2)
    print(f"Withdrawing $400 from Current Account (Balance is $200, Overdraft is $500)...")
    accounts_list[2].withdraw(400.00)

    print("\n--- Polymorphic Statement Loop ---")
    # This is the polymorphic loop. It treats every object as an "Account"
    # and calls .statement() without caring which specific subclass it is!
    for account in accounts_list:
        print(account.statement())