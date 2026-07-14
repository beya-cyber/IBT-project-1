# Dictionaries are a collection of {key: value} pairs and also ordered and changable, no duplicates allowed
# we use {} for dictionaries like set

capital_citys = {"Addis abeba": "Ethiopia",
    "Debrebirhan": "Semen shewa",
    "Azezo": "Gonder",
     "Dese": "wolo"            }
#the first one is key and the second value
#print(help(capital_citys))
#print(capital_citys.get("Azeszo"))
#print(capital_citys.get("Dese"))
#if capital_citys.get("Dese"):
#    print("The zone Name is Exist")
#else:
#    print("The zone Name does not Exist")
#capital_citys.update({"Nazret": "Adama"}) #to add new value
#capital_citys.update({"Nazret": "Bishoftu"}) #or we can use update to edit our value
#capital_citys.pop("Nazret") #pop then name then it will be delete
#capital_citys.popitem()
#keys = capital_citys.keys()
#for key in keys:
#    print(key)
#values = capital_citys.values()
#for value in values:
#    print(value, end="  ")
items = capital_citys.items()
for key, value in capital_citys.items():
    print(f"{key}: {value}", end="  ")