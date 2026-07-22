class Account:
    def __init__(self, owner, number, balance=0):
        self.owner = owner
        self.account_number = number
        self._balance = max(0, balance)
        self.history = []  # Stack for transaction history (LIFO)

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        self.history.append(("DEPOSIT", amount))  # Push to stack
        print(f"[+] Deposited {amount:.2f} ETB into {self.account_number}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
        self.history.append(("WITHDRAWAL", amount))  # Push to stack
        print(f"[-] Withdrew {amount:.2f} ETB from {self.account_number}")

    def undo_last(self):
        """Pops the most recent transaction and reverses its effect."""
        if not self.history:
            print(f"[!] No transactions to undo for {self.account_number}")
            return

        tx_type, amount = self.history.pop()  # Pop from stack
        if tx_type == "DEPOSIT":
            self._balance -= amount
            print(f"[Undo] Reversed deposit of {amount:.2f} ETB from {self.account_number}")
        elif tx_type == "WITHDRAWAL":
            self._balance += amount
            print(f"[Undo] Reversed withdrawal of {amount:.2f} ETB to {self.account_number}")

    def __repr__(self):
        return f"Account({self.account_number}, {self.owner}, {self._balance:.2f} ETB)"


class AccountRegistry:
    def __init__(self):
        self.by_number = {}  # Dict for O(1) lookups
        self.order = []      # List to preserve insertion order

    def add(self, acc):
        """Adds account to registry in O(1) time."""
        self.by_number[acc.account_number] = acc
        self.order.append(acc.account_number)

    def find(self, number):
        """O(1) account lookup."""
        return self.by_number.get(number)

    def list_all(self):
        """Returns accounts in insertion order."""
        return [self.by_number[num] for num in self.order]


# --- Execution Test ---
if __name__ == "__main__":
    registry = AccountRegistry()

    # Create & Register Accounts
    a1 = Account("Almaz", "CBE-1001", 1000)
    a2 = Account("Dawit", "CBE-1002", 500)
    registry.add(a1)
    registry.add(a2)

    # O(1) Lookup Test
    found = registry.find("CBE-1001")
    print(f"\nFound Account: {found}")

    # Transactions & History Stack
    found.deposit(500)   # Balance -> 1500
    found.withdraw(200)  # Balance -> 1300
    print(f"Current Balance: {found.balance} ETB")

    # Undo Last Action (Reverses 200 ETB withdrawal)
    found.undo_last()
    print(f"Balance after undo: {found.balance} ETB")

    # List All Accounts
    print("\nAll Registered Accounts (Insertion Order):")
    for acc in registry.list_all():
        print(acc)