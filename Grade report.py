students = [ ]

while True:
    print("Welcome to the Grade Report")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Show Top Student")
    print("4. Exit")

    choice = input("Enter your choice(1-4): ")

    if choice == "1":
        pass
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        print("Bye")
        break
    else:
        print("Invalid Choice try again(1-4)")


    def get_letter_grade(score):
        if score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        else:
            return 'C'


    if choice == '1':
        name = input("Enter student name: ")
        # Always cast score to float or int!
        score = float(input("Enter score (0-100): "))
        students.append({"name": name, "score": score})
        print(f"Added {name} successfully.")

    elif choice == '2':
        if not students:
            print("No records found.")
        else:
            print("\n--- ALL RECORDS ---")
            for s in students:
                grade = get_letter_grade(s["score"])
                print(f"{s['name']} - Score: {s['score']} | Grade: {grade}")

    elif choice == '3':
        if not students:
         print("No records found.")
        else:
        # Finding maximum element manually or using max() with a key
            top_student = max(students, key=lambda s: s["score"])
            print(f"Top Student: {top_student['name']} with {top_student['score']} points.")

