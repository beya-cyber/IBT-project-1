# Lets write our clothes object

class Clothes:
    def __init__(self, type, color, price): #This is known as (constructor function) used to to create our objecct
        self.type = type   #and also its have attributes to build our object init stands for initialization
        self.color = color  #self is referring to the object we're  currently working or creating on it
        self.price = price #these are attributes or variables that contain values
    def show(self):
        print(self.type)
        print(self.color)  #they are methods or functions
        print(self.price)
    def order(self):
        print(self.type)
        print(self.color)
        print(self.price)

