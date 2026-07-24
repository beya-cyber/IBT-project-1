
def checkMeera(lst):
    num_set = set(lst)
    is_meera = True

    for num in lst:
        if num == 0:
            # If 0 is in the array, 0 * 2 = 0.
            # It only breaks the rule if 0 appears more than once.
            if lst.count(0) > 1:
                is_meera = False
                break
        elif (num * 2) in num_set:
            is_meera = False
            break

    if is_meera:
        print("I am a Meera array")
    else:
        print("I am NOT a Meera array")

checkMeera([7, 4, 9])
checkMeera([1, -6, 4, -3])
checkMeera([10, 4, 0, 5])


