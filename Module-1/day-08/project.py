def binary_search(sorted_keys, target):
    """Custom iterative binary search over a sorted list of account numbers."""
    low = 0
    high = len(sorted_keys) - 1

    while low <= high:
        mid = (low + high) // 2
        if sorted_keys[mid] == target:
            return mid
        elif sorted_keys[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


class Account:
    def __init__(self, owner, number, balance=0):
        self.owner = owner
        self.account_number = number
        self._balance = max(0, balance)
        self.history = []  # List of transaction values, e.g., [1000, -200, 500]

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self._balance += amount
        self.history.append(amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
        self.history.append(-amount)

    def __repr__(self):
        return f"Account({self.account_number}, {self.owner}, {self._balance:.2f} ETB)"


class AccountRegistry:
    def __init__(self):
        self.by_number = {}

    def add(self, acc):
        self.by_number[acc.account_number] = acc

    # 1. Balance Leaderboard
    def top_by_balance(self, n=5):
        """Returns top n accounts sorted by balance descending using key=lambda."""
        accts = sorted(self.by_number.values(), key=lambda a: a.balance, reverse=True)
        return accts[:n]

    # 2. Fast Binary Search by Account Number
    def find_by_number(self, number):
        """Finds account using binary_search on sorted keys without using 'in' or loops."""
        nums = sorted(self.by_number)  # Sorted list of keys
        idx = binary_search(nums, number)
        return self.by_number[nums[idx]] if idx >= 0 else None

    # 3. Recursive Total Transactions
    def total_transactions(self, number):
        """Recursively sums the transaction history for a given account number."""
        acc = self.find_by_number(number)
        if not acc:
            return 0

        def _sum_recursive(tx_list):
            if not tx_list:  # Base case
                return 0
            return tx_list[0] + _sum_recursive(tx_list[1:])  # Recursive step

        return _sum_recursive(acc.history)


# --- Test Script ---
if __name__ == "__main__":
    registry = AccountRegistry()

    # Create & register test accounts
    a1 = Account("Almaz", "CBE-1001", 1500)
    a2 = Account("Dawit", "CBE-1002", 700)
    a3 = Account("Tigist", "CBE-1003", 3200)
    a4 = Account("Samuel", "CBE-1004", 450)

    for acc in [a1, a2, a3, a4]:
        registry.add(acc)

    # Perform transactions for recursive total testing
    a3.deposit(500)   # +500
    a3.withdraw(200)  # -200

    # Test 1: Leaderboard
    print("--- Top 2 Leaderboard ---")
    for acc in registry.top_by_balance(2):
        print(acc)

    # Test 2: Binary Search
    print("\n--- Binary Search for CBE-1002 ---")
    found = registry.find_by_number("CBE-1002")
    print("Found:", found)

    # Test 3: Recursive Total
    print("\n--- Recursive Total Transactions for CBE-1003 ---")
    total = registry.total_transactions("CBE-1003")
    print(f"Net Transaction Sum: {total} ETB")