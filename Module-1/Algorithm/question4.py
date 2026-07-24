
def checkMeera(lst):
    num_set = set(lst)
    is_meera = True

    for num in lst:
        if num == 0:
            if is_meera:
                print("I am a Meera array")
            else:
                print("I am NOT a Meera array")

checkMeera([7, 4, 9])
checkMeera([1, -6, 4, -3])
checkMeera([10, 4, 0, 5])


