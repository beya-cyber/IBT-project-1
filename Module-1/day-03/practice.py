cities = ["Addis Ababa", "Hawassa", "Addis Ababa", "Adama", "Hawassa", "Gonder"]
unique_cities = set(cities)
print("Distinct cities:", unique_cities)
print("Count:", len(unique_cities))

# --- Exercise 2: Price Report ---
print("\n--- Exercise 2 ---")
groceries = {
    "Injera": 15,
    "Coffee": 350,
    "Sugar": 120,
    "Milk": 90,
    "Oil": 450
}
for item, price in groceries.items():
    print(f"{item}: {price} ETB")

# --- Exercise 3: Tax Comprehension ---
print("\n--- Exercise 3 ---")
prices = [100, 250, 400, 80]
prices_with_tax = [p * 1.15 for p in prices]
print("Prices with 15% tax:", prices_with_tax)

# --- Exercise 4: Cheap Items ---
print("\n--- Exercise 4 ---")
cheap_prices = [p for p in prices if p < 200]
print("Prices under 200 ETB:", cheap_prices)

# --- Exercise 5: Write & Read ---
print("\n--- Exercise 5 ---")
with open("names.txt", "w") as f:
    f.write("Almaz\nDawit\nTigist\n")

with open("names.txt", "r") as f:
    for line in f:
        print(line.strip())

# --- Exercise 6: Safe Division ---
print("\n--- Exercise 6 ---")
try:
    user_input = input("Enter a number to divide 1000 by: ")
    number = float(user_input)
    result = 1000 / number
    print(f"Result: {result}")
except ValueError:
    print("Error: Please enter a valid number.")
except ZeroDivisionError:
    print("Error: Cannot divide by zero.")