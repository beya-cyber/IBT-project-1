def load_stock(filename):
    """Read stock from file into a dictionary using try/except."""
    stock = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                if "," in line:
                    item, qty = line.strip().split(",")
                    stock[item.strip()] = int(qty.strip())
        print(f"[+] Loaded stock from {filename}")
    except FileNotFoundError:
        print(f"[!] Warning: {filename} not found. Starting with empty stock.")
    return stock

def save_stock(stock, filename):
    """Save dictionary stock back to the text file."""
    with open(filename, "w") as f:
        for item, qty in stock.items():
            f.write(f"{item},{qty}\n")
    print(f"[+] Saved updated stock to {filename}")

def adjust(stock, item, amount):
    """Increase or decrease an item's stock quantity."""
    stock[item] = stock.get(item, 0) + amount
    print(f"[->] Adjusted {item} by {amount}. New total: {stock[item]}")

# --- Execution Flow ---
if __name__ == "__main__":
    # 1. Load existing stock from file
    stock = load_stock(FILE_PATH)

    # 2. Update stock quantities
    adjust(stock, "Amoxicillin", 10)  # Restock (+10)
    adjust(stock, "Paracetamol", -20) # Sale (-20)
    adjust(stock, "Aspirin", 15)      # New item (+15)

    # 3. Report low-stock items (< 10) using list comprehension
    low_stock = [item for item, qty in stock.items() if qty < 10]
    print("\nLow Stock Items (<10 units):", low_stock)