def format_currency(amount):
    return f"{amount:.2f} ETB"

balances = [1200, 450, 800]
for bal in balances:
    print(f"Balance: {format_currency(bal)}")

customers = [
    ("Almaz", 1500),
    ("Dawit", 700),
    ("Tigist", 200),
    ("Hanna", 1200),
    ("Samuel", 450),
]

def tier(balance):
    if balance >= 1000:
        return "Premium"
    elif balance >= 500:
        return "Standard"
    return "Basic"

counts = {"Premium": 0, "Standard": 0, "Basic": 0}

for name, balance in customers:
    customer_tier = tier(balance)
    counts[customer_tier] += 1
    print(f"{name}: {customer_tier} ({balance} ETB)")

print("\nSummary:")
for tier_name, count in counts.items():
    print(f"{tier_name}: {count}")
