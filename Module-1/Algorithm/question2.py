def reverseCompare(num):
    num_str = str(num)
    reversed_num = int(num_str[::-1])

    if num > reversed_num:
        print("Ok")
    else:
        print("Not ok")

print("reverse the number compare result")
reverseCompare(72)
reverseCompare(23)