# Lists, tuples, and sets     note to print loops mostly we use index
#List[] mutable(it can be change), flexible
#Tiple() imutable(unchangable), faster
#Set{} mutable (add/remove), unordered, no duplicates
"""
Lists
fruits = ["apple", "banana", "cherry", "mango", "papaya", "watermelon"]
fruits[3] = "pineaples"
fruits.pop(3)
fruits.insert(3, "pineaples")
fruits.remove("pineaples")
fruits.sort()
fruits.reverse()
fruits.append("pineaples")

for fruit in fruits:  #note for makes these lists properly
    print(fruit, end="  ")
"""
from enum import member

"""
Tuples are the same to lists but they are not changable and use ()

citys = ("Addis abeba", "adama", "mekele", "jima", "jijiga")
for city in citys:
    print(city, end="   ")
"""

#set uses {} to assighn we can't access them by index bc they will be changed each time(unordered)
#best for membership testing

members = {"Eden", "ketema", "hiwot", "meseret"}
members.add("Mekdi")

member = input("Please enter your name: ")

if member in members:
    print(f"{member} is in the list")
else:
    print(f"{member} is not in the list")

#for member in members:
#    print(member, end="  ")