#Addis Banking program

def show_balance(balance):
    print(f"Your balance is  {balance:.2f} birr")

def deposit():
    amount = float(input("Enter your deposit amount: "))

    if amount <= 0:
        print("Please enter a positive amount")
        return 0
    else:
        return amount

def withdraw(balance):
    amount = float(input("Enter your withdraw amount: "))
    if amount > balance:
        print("Insufficient Balance")
        return 0
    elif amount <= 0:
        print("Please enter a positive amount")
        return 0
    else:
        return amount


def main():
    balance = 0
    is_running = True

    while is_running:
        print( "**********************************************")

        print("<<      Welcome to the Addis Bank     >>")
        print("**********************************************")
        print("1. Show balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")

        print("****************************************************")

        choice = (input("Enter your choice (1-4): "))

        if choice == '1':
            show_balance(balance)
        elif choice == '2':
            balance += deposit()
        elif choice == '3':
            balance -= withdraw(balance)
        elif choice == '4':
            is_running = False
        else:
            print("Please enter a valid choice")

if __name__ == "__main__":
       main()

