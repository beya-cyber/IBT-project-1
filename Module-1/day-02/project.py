def split_bill():
    # 1. Take inputs inside the function (changed bill to float so it handles decimals/cents)
    bill_amount = float(input("Enter the total bill amount: "))
    num_people = int(input("Enter the number of people: "))

    # 2. Calculate the split
    amount_per_person = bill_amount / num_people

    # 3. Print the result FIRST before returning
    print(f"Each person should pay: {amount_per_person:.2f}")

    # 4. Return ends the function
    return amount_per_person


# 5. Call the function cleanly with empty parentheses to start the program
split_bill()