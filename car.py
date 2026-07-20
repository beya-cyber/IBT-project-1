from POOP import Car


car1 = Car ("BYD", 2026, "orange", True) #car1 is object
car2 = Car ("volswagen", 2024, "silver", True)
car3 = Car ("sinotruck", 2025, "red", False)

#    print(car3.model) #if we print only car1(object) it give us only memory allocate
#    print(car3.year)  # so if wants to access we have follow up (.attribute)
#    print(car3.color)  # the(.) is known as the attribute access operator
#    print(car3.for_sale)

car2.stop()
car3.drive()
car1.describe()