# Lets make grade Displayer

print("=== PROCESSING APPLICATION RESULTS ===")

#Accept any letter and convert it to numbers
grade_number = int(input("Please enter your grade number: "))

#then display their grade status based on the mark list
if grade_number >= 90:
    print("Grade: A")
elif grade_number >= 80:
    print("Grade: B")
elif grade_number >= 70:
    print("Grade: C")
else:
    print("Grade: D")