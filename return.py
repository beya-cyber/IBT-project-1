#return = satement used to end a function
#         and send a result back to the caller

def create_name(first_name, last_name):
    last_name = last_name.capitalize()
    first_name = first_name.capitalize()
    return first_name + " " + last_name

full_name = create_name("behailu", "tazi") #we assighn some data by arguments
#and we will call it by its variable instead of its own name.

print(full_name)
