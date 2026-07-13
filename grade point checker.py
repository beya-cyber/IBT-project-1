grade = (int(input("Enter your grade: ")))
tutor_fee = 5600
if grade >= 72:
  print("Congragulations you are Qualified for the next year")
elif grade >= 60 <= 71:
  print("You have the remedial programm to upgrade your grade")
  print(f"But if you wants to take in private tutor you have a discount {tutor_fee * 0.55} birr")
elif grade >= 50 <= 59:
  print("You can use paid tutor programm to upgrade your grade")
  print(f"The tutor fee is {tutor_fee} birr")
else:
  print("Sorry, you are not qualified for the next year")
