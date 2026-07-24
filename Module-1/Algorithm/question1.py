def getOnlyEvens(lst):
    result = []
    for index, val in enumerate(lst):
        if index % 2 == 0 and val % 2 == 0:
            result.append(val)
    print(result)


getOnlyEvens([1, 2, 3, 6, 4, 8])
getOnlyEvens([0, 1, 2, 3, 4])