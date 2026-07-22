#Type conversion
age_text = input("your age: ")         #e.g "24" (a string)
age = int(age_text)                    # 24 (now an int)
next_year = age + 1                    #works only after int()

#Logical operators
balance = 1500
is_member = True

is_member == 1500
balance > 1000 and is_member
not is_member

#Loops while and for
#while-> repeat on a condition 
count = 3
while count > o:
    print(f"sending...{count}")
    count = count - 1

#for-> walk a range or a list
for i in range(1, 4):     #1,2,3 (stops before 4)
    print(f"Receipt #{i}")

for name in ["Almaz", "Dawit", "Tigist"]:
    print(f"Selam, {name}")

#function
def add_tax(price, rate=0.5):
    return price + price * rate

total = add_tax(1000)       #1150.0  (uses default rate)
total = add_tax(1000, rate=0.10)  #1150.0 (keyword argument)

#scope

tax_rate = 0.5     #global - readable anywhere

def total(price):  #local - exists only in here
    fee = 50
    return price + fee
    print(total(1000))

print(tax_rate)
print(fee)