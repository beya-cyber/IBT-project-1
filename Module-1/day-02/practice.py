temp = float(input("Enter temperature in °C: "))
if temp < 15:
    print("cold")
elif temp <= 28:
    print("warm")
else:
    print("hot")

# --- Exercise 2: Receipt Loop ---
print("\n--- Exercise 2 ---")
for i in range(1, 11):
    print(f"Receipt #{i}")

# --- Exercise 3: Even Numbers ---
print("\n--- Exercise 3 ---")
for num in range(1, 21):
    if num % 2 == 0:
        print(num)

# --- Exercise 4: Discount Function ---
print("\n--- Exercise 4 ---")
def apply_discount(price, percent=10):
    return price * (1 - percent / 100)

print("Default (10% off $100):", apply_discount(100))
print("Custom (20% off $100):", apply_discount(100, 20))

# --- Exercise 5: Countdown ---
print("\n--- Exercise 5 ---")
count = 5
while count > 0:
    print(count)
    count -= 1
print("Liftoff!")