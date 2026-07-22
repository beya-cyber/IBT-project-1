class BankConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.interest_rate = 0.05
            cls._instance.overdraft_limit = 1000.0
        return cls._instance

# 2. Base Account Class with Observer Support (SRP & Decoupling)
class Account:
    def __init__(self, owner, number, balance=0):
        self.owner = owner
        self.account_number = number
        self._balance = max(0, balance)
        self._observers = []

    @property
    def balance(self):
        return self._balance

    def subscribe(self, observer):
        self._observers.append(observer)

    def _notify(self, message):
        for observer in self._observers:
            observer.update(message)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        self._notify(f"Deposited {amount:.2f} ETB. New Balance: {self._balance:.2f} ETB")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
        self._notify(f"Withdrew {amount:.2f} ETB. New Balance: {self._balance:.2f} ETB")

# 3. Subclasses utilizing BankConfig (OCP)
class SavingsAccount(Account):
    def apply_interest(self):
        config = BankConfig()
        interest = self._balance * config.interest_rate
        self._balance += interest
        self._notify(f"Interest Applied ({config.interest_rate*100}%): +{interest:.2f} ETB")

class CurrentAccount(Account):
    def withdraw(self, amount):
        config = BankConfig()
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > (self._balance + config.overdraft_limit):
            raise ValueError("Exceeds overdraft limit.")
        self._balance -= amount
        self._notify(f"Withdrew {amount:.2f} ETB (Overdraft allowed). Balance: {self._balance:.2f} ETB")

# 4. Factory Pattern for Account Creation
class AccountFactory:
    @staticmethod
    def create(kind, owner, number, balance=0):
        kind = kind.lower()
        if kind == "savings":
            return SavingsAccount(owner, number, balance)
        elif kind == "current":
            return CurrentAccount(owner, number, balance)
        raise ValueError(f"Unknown account type: {kind}")

# 5. Observer Concrete Classes
class SMSAlert:
    def update(self, message):
        print(f"[TeleBirr SMS] {message}")

class AuditLog:
    def update(self, message):
        print(f"[Audit Log] {message}")

# --- Execution Test ---
if __name__ == "__main__":
    # Test Singleton
    c1, c2 = BankConfig(), BankConfig()
    print("Same Config Instance?", c1 is c2)

    # Test Factory
    acc = AccountFactory.create("savings", "Almaz", "CBE-1001", 2000)

    # Test Observers
    acc.subscribe(SMSAlert())
    acc.subscribe(AuditLog())

    # Operations
    acc.deposit(500)
    acc.apply_interest()
    acc.withdraw(300)