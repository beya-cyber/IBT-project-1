def returnFactorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
print(returnFactorial(5))
print(returnFactorial(6))
print(returnFactorial(0))