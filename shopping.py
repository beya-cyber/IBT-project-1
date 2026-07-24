catalog = {
    "apples": 435.23,
    "oranges": 210.00,
    "bananas": 300.25,
}

cart = []

for key, value in catalog.items():
    print(f"{key}: {value}")

while True:
    item_name = input("\nEnter item name to Buy or (or 'checkout' to finish): ").strip().lower()

    if item_name == "checkout":
        break
    if item_name in catalog:
        qty = int(input(f"How many {item_name}s do you have? : "))
        unit_price = catalog[item_name]
        item_total = qty * unit_price

    cart.append({
        "name": item_name,
        "qty": qty,
        "subtotal": item_total
    })
    print(f"Added {qty} x {item_name} (${item_total:.2f})")
else:
    print("Item not in catalog! Please choose apple, bread, or milk.")

print("\n" + "=" * 30)
print("       OFFICIAL RECEIPT       ")
print("=" * 30)

raw_total = 0.0

for entry in cart:
    print(f"{entry['qty']}x {entry['name'].capitalize():<10} - ${entry['subtotal']:.2f}")
    raw_total += entry['subtotal']

    tax = raw_total * 0.10
    grand_total = raw_total + tax

    print("-" * 30)
    print(f"Subtotal:    ${raw_total:.2f}")
    print(f"Tax (10%):   ${tax:.2f}")
    print(f"Grand Total: ${grand_total:.2f}")
    print("=" * 30)