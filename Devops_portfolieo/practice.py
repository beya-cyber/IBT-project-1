class Account:
    def __init__(self, account_number, holder_name, balance=0.0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance
        # Step 4: Each account gets a transaction-history stack (LIFO list)
        self.history_stack = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        # Push transaction to stack: (type, amount)
        self.history_stack.append(('deposit', amount))
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        # Push transaction to stack: (type, amount)
        self.history_stack.append(('withdraw', amount))
        return self.balance

    def undo_last(self):
        """
        Step 5: Pops the most recent transaction from the stack and reverts the balance.
        """
        if not self.history_stack:
            print(f"No transactions to undo for Account {self.account_number}.")
            return None

        # Pop the last transaction from the stack (LIFO)
        last_tx_type, amount = self.history_stack.pop()

        if last_tx_type == 'deposit':
            self.balance -= amount
            print(f"Undid Deposit of ${amount:.2f}. New Balance: ${self.balance:.2f}")
        elif last_tx_type == 'withdraw':
            self.balance += amount
            print(f"Undid Withdrawal of ${amount:.2f}. New Balance: ${self.balance:.2f}")

        return last_tx_type, amount

    def __repr__(self):
        return f"Account({self.account_number}, '{self.holder_name}', Balance: ${self.balance:.2f})"


class AccountRegistry:
    def __init__(self):
        # Step 2: Store accounts in a dictionary keyed by account number for O(1) lookup
        self.accounts = {}

    def add(self, account):
        """
        Step 3: Add an account to the registry. O(1)
        """
        if account.account_number in self.accounts:
            raise ValueError(f"Account number {account.account_number} already exists.")
        self.accounts[account.account_number] = account

    def find(self, account_number):
        """
        Step 3: Lookup an account by number. O(1) time complexity.
        """
        return self.accounts.get(account_number, None)

    def list_all(self):
        """
        Step 3: Return an ordered list of all accounts.
        """
        return [self.accounts[acc_num] for acc_num in sorted(self.accounts.keys())]


# ==========================================
# Example Usage & Testing
# ==========================================
if __name__ == "__main__":
    registry = AccountRegistry()

    # Step 2 & 3: Creating and Adding Accounts
    acc1 = Account(101, "Alice", 500.0)
    acc2 = Account(102, "Bob", 1000.0)

    registry.add(acc1)
    registry.add(acc2)

    # Step 3: O(1) Lookup Test
    found_acc = registry.find(101)
    print("Found Account:", found_acc)

    # Step 4: Deposit and Withdraw (Pushes onto history stack)
    print("\n--- Performing Transactions ---")
    found_acc.deposit(200.0)   # Balance: 700.0
    found_acc.withdraw(50.0)   # Balance: 650.0
    print("Current Balance:", found_acc.balance)
    print("Transaction History Stack:", found_acc.history_stack)

    # Step 5: Undo Last Transaction (Pops from history stack)
    print("\n--- Undoing Transactions ---")
    found_acc.undo_last()  # Undoes $50 withdrawal -> Balance becomes 700.0
    found_acc.undo_last()  # Undoes $200 deposit -> Balance becomes 500.0

    # Step 3: Ordered List All
    print("\n--- All Accounts (Ordered) ---")
    for acc in registry.list_all():
        print(acc)