#step 1 collecting applican data  (variables, input, and output)
print ("Welcome to Tazi Security Scholarship Application Form")

#input() captures data always as a string, so we need to convert it to the appropriate data type if necessary. For example, if we want to collect the applicant's age, we can use:
name = input("Please enter your full name: ")
age = int(input("Please enter your age: "))  # Convert the input to an integer
## Convert input text to a float for decimal numbers
gpa = float(input("Please enter your GPA (e.g., 3.5): "))  # Convert the input to a float

# ----------------------------------------------------
# STEP 2: CHECKING ELIGIBILITY (Operators & Logic)
# ----------------------------------------------------
# The 'and' operator requires BOTH facts to be True
meets_citeria = (age >= 18) and (gpa >= 3.0)

# ----------------------------------------------------
# STEP 3: MAKING THE DECISION (Control Flow)
# ----------------------------------------------------

print("\n=== PROCESSING APPLICATION RESULTS ===")
if meets_citeria:
    print(f"Congratulations {name}! You meet the eligibility criteria for the Tazi Security Scholarship.")
else:
    print(f"Sorry {name}, you do not meet the eligibility criteria for the Tazi Security Scholarship.")
    