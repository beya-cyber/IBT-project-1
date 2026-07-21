#Transaction log reader

def load_transactions(filename="telebirr transactions.txt"):
    customer_totals = {}

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # skip blank lines

            customer, amount = line.split(",")
            amount = float(amount)

            # Add to total (uses dict.get to handle new or existing customers)
            customer_totals[customer] = (
                customer_totals.get(customer, 0) + amount
            )

    return customer_totals


# Load and display results
totals = load_transactions()

print("--- TELEBIRR TRANSACTION SUMMARY ---")
for customer, total in totals.items():
    print(f"Customer: {customer} | Total: {total} Birr")