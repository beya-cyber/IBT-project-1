
class Account:
    def __init__(self, owner, account_no, balance):
        self.owner = owner
        self.account_no = account_no
        #  We changed "__balance" to "_balance" (single underscore).
        # This tells Python it is "protected" so our child classes can access it.
        self._balance = balance

    @property
    def statement_balance(self):
        """A helper property to read the balance value if needed."""
        return self._balance

    
    @property
    def statement(self):
        return f"Standard Account | Owner: {self.owner} | No: {self.account_no} | Balance: ${self._balance:.2f}"

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount


# Putting (Account) in parentheses means SavingsAccount inherits everything from Account
class SavingsAccount(Account):
    def __init__(self, owner, account_no, balance, rate):
        # 💡 super().__init__ sends the owner, account_no, and balance up to the parent class
        super().__init__(owner, account_no, balance)
        self.rate = rate  # e.g., 0.05 for 5% interest rate

    def add_interest(self):
        """Calculates interest and deposits it directly into the account."""
        interest = self._balance * self.rate
        self.deposit(interest)  # We can call the parent's deposit method directly!
        print(f"Added ${interest:.2f} interest to Savings Account {self.account_no}")

    # Overriding the statement property to label it as Savings Account
    @property
    def statement(self):
        return f"Savings Account  | Owner: {self.owner} | No: {self.account_no} | Balance: ${self._balance:.2f} (Interest Rate: {self.rate * 100:.1f}%)"


#CurrentAccount inherits from Account
class CurrentAccount(Account):
    def __init__(self, owner, account_no, balance, overdraft):
        super().__init__(owner, account_no, balance)
        self.overdraft = overdraft  # Allowed negative limit (e.g., 500.00)

    #  Overriding the withdraw method to allow overdraft limits
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        # Overdraft allows us to withdraw up to (balance + overdraft limit)
        if amount > self._balance + self.overdraft:
            raise ValueError("Insufficient funds: Exceeds overdraft limit")
        
        self._balance -= amount

    # Overriding the statement property to label it as Current Account
    @property
    def statement(self):
        return f"Current Account  | Owner: {self.owner} | No: {self.account_no} | Balance: ${self._balance:.2f} (Overdraft Limit: ${self.overdraft:.2f})"

#Polymorphic loop demonstration
if __name__ == "__main__":
    # Create a mixed list containing one instance of each type of account
    accounts_list = [
        Account("Beya", "123456789", 1000.00),                    # Standard
        SavingsAccount("Almaz", "987654321", 5000.00, 0.05),     # Savings (5% interest)
        CurrentAccount("Dawit", "555666777", 200.00, 500.00)     # Current ($500 overdraft)
    ]

    print("--- Performing Actions ---")
    
    # 1. Add interest to Almaz's Savings Account (Index 1 in list)
    accounts_list[1].add_interest()

    # 2. Dawit (Index 2) only has $200 but wants to withdraw $400
    try:
        print(f"Attempting to withdraw $400 from Dawit's Current Account (Balance: ${accounts_list[2].statement_balance})...")
        accounts_list[2].withdraw(400.00)
        print(f"Withdrawal successful! New balance: ${accounts_list[2].statement_balance}")
    except ValueError as e:
        print(f"Error: {e}")

    print("\n--- Step 5: Polymorphic Statement Loop ---")
    # 3. This is the polymorphic loop!
    # It loops through the list and runs .statement without caring which specific class it is.
    for account in accounts_list:
        print(account.statement)