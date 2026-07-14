# function = A block of a reusable code(once i write it i will use whenever i wants to use it)
#         place () after the function name to invoke it


#def my_birthday(name, age):    #after the function we have to intend tha belong the fun
#we can use parameters in paranthesis they are used to like temporary variable means they store arguments
#if we say parameters are temp variable they don't use " "
# and also we use arguments to call the parameter and they are like values so they will use " "
#    print(f'Happy Birthday {name}, you are {age} years old')
#my_birthday("Beya", 23) #then we will call it by its name(function name)
#my_birthday("Habte", 20)
#my_birthday("Mekdi", 27)

def cap_of_coffee(quantity, amount ):
    print(f"you are ordered {quantity: .2f} coffee")
    print(f"your total amount of bill is  {amount} Birr")

cap_of_coffee(2, 15.45)