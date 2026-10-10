"""
Student Record and Academic Management System
Data Organization using Python
BANDARU CHANDU | B.Tech AIML | FY AIML - A | Division A
Sanjivani University | PNR: 2126UMLM1263
"""

students = []


def clean(value):
    """Convert a value to text and remove outside spaces."""
    if isinstance(value, tuple):
        value = value[0] if value else ""
    return str(value or "").strip()


def search_student(roll):
    """Find a student by roll number."""
    roll = clean(roll).upper()
    for student in students:
        if student["roll_number"] == (roll,):
            return student
    return None


def average(student):
    """Return average marks, or zero when there are no marks."""
    return sum(student["marks"]) / len(student["marks"]) if student and student["marks"] else 0.0


def add_student(roll, reg, name, dept, subjects, marks, attendance, dob, email, address, clubs):
    """Validate and add a student."""
    roll, reg, name, dept = clean(roll).upper(), clean(reg).upper(), clean(name).title(), clean(dept).upper()
    if not roll or not reg or not name or not dept:
        print("Roll number, registration number, name and department are required.")
        return False
    if search_student(roll):
        print("Student already exists.")
        return False
    if any(m < 0 or m > 100 for m in marks + attendance):
        print("Marks and attendance values must be between 0 and 100.")
        return False

    students.append({
        "roll_number": (roll,), "registration_number": (reg,),
        "name": name, "department": dept,
        "subjects": list(subjects), "marks": list(marks),
        "attendance": list(attendance), "dob": tuple(clean(dob).split("-")),
        "contact": {"email": clean(email).lower(), "address": clean(address)},
        "clubs": set(clubs)
    })
    print("Student added successfully.")
    return True


def update_student(roll, field, value):
    """Update an existing student's field."""
    s = search_student(roll)
    if not s:
        print("Student not found.")
        return False
    field = clean(field).lower()
    if field == "roll_number":
        new = clean(value).upper()
        if not new or any(x is not s and x["roll_number"] == (new,) for x in students):
            print("Invalid or duplicate roll number.")
            return False
        s[field] = (new,)
    elif field == "registration_number":
        s[field] = (clean(value).upper(),)
    elif field == "name":
        s[field] = clean(value).title()
    elif field == "department":
        s[field] = clean(value).upper()
    elif field in ("subjects", "marks", "attendance"):
        values = list(value)
        if field in ("marks", "attendance") and any(v < 0 or v > 100 for v in values):
            print("Values must be between 0 and 100.")
            return False
        s[field] = values
    elif field == "clubs":
        s[field] = set(value)
    elif field == "dob":
        s[field] = tuple(clean(value).split("-"))
    elif field in ("email", "address"):
        s["contact"][field] = clean(value).lower() if field == "email" else clean(value)
    else:
        print("Invalid field.")
        return False
    print("Student record updated.")
    return True


def delete_student(roll):
    s = search_student(roll)
    if not s:
        print("Student not found.")
        return False
    students.remove(s)
    print("Student deleted.")
    return True


def display_records(records=None):
    records = students if records is None else records
    if not records:
        print("No student records available.")
        return
    for s in records:
        print("-" * 55)
        print("Roll:", s["roll_number"][0], "| Registration:", s["registration_number"][0])
        print("Name:", s["name"], "| Department:", s["department"])
        print("Subjects:", ", ".join(s["subjects"]), "| Marks:", s["marks"])
        print("Average:", f"{average(s):.2f}", "| Attendance:", s["attendance"])
        print("DOB:", "-".join(s["dob"]))
        print("Email:", s["contact"]["email"], "| Address:", s["contact"]["address"])
        print("Clubs:", ", ".join(sorted(s["clubs"])))


def report():
    if not students:
        print("No records available.")
        return
    departments = {s["department"] for s in students}
    subjects = {x for s in students for x in s["subjects"]}
    clubs = {x for s in students for x in s["clubs"]}
    top = max(students, key=average)
    print("Total students:", len(students))
    print("Departments:", ", ".join(sorted(departments)))
    print("Subjects:", ", ".join(sorted(subjects)))
    print("Clubs:", ", ".join(sorted(clubs)))
    print("Highest scorer:", top["name"], f"({average(top):.2f})")
    for dept in sorted(departments):
        print(dept + ":", sum(1 for s in students if s["department"] == dept))


def read_list(prompt, convert=str):
    return [convert(x.strip()) for x in input(prompt).split(",") if x.strip()]


def seed_demo_data():
    add_student("S001", "REG001", "Aarav Kumar", "CSE", ["Python", "Maths", "Physics"],
                [86, 91, 84], [92, 95, 90], "2006-04-19", "aarav@example.com",
                "Guntur, Andhra Pradesh", ["Coding Club", "AI Club"])
    add_student("S002", "REG002", "Meera Sharma", "AIML", ["Python", "Maths", "AI"],
                [94, 89, 96], [97, 91, 95], "2006-08-12", "meera@example.com",
                "Vijayawada, Andhra Pradesh", ["AI Club"])


def main():
    seed_demo_data()
    while True:
        print("\nSTUDENT RECORD AND ACADEMIC MANAGEMENT SYSTEM")
        print("1 Add | 2 Search | 3 Update | 4 Delete | 5 Display")
        print("6 Average | 7 Report | 8 Highest scorer | 9 By department | 10 Count | 0 Exit")
        choice = input("Choice: ").strip()
        try:
            if choice == "1":
                roll, reg = input("Roll: "), input("Registration number: ")
                name, dept = input("Name: "), input("Department: ")
                subjects = read_list("Subjects (comma-separated): ")
                marks = read_list("Marks (comma-separated): ", float)
                attendance = read_list("Attendance (comma-separated): ", float)
                dob, email, address = input("DOB YYYY-MM-DD: "), input("Email: "), input("Address: ")
                clubs = read_list("Clubs (comma-separated): ")
                add_student(roll, reg, name, dept, subjects, marks, attendance, dob, email, address, clubs)
            elif choice == "2":
                s = search_student(input("Roll number: "))
                display_records([s]) if s else print("Student not found.")
            elif choice == "3":
                roll = input("Current roll number: ")
                field = input("Field (roll_number, registration_number, name, department, subjects, marks, attendance, clubs, dob, email, address): ")
                if field in ("subjects", "clubs"):
                    value = read_list("New values, comma-separated: ")
                elif field in ("marks", "attendance"):
                    value = read_list("New numbers, comma-separated: ", float)
                else:
                    value = input("New value: ")
                update_student(roll, field, value)
            elif choice == "4":
                delete_student(input("Roll number: "))
            elif choice == "5":
                display_records()
            elif choice == "6":
                s = search_student(input("Roll number: "))
                print(f"Average: {average(s):.2f}" if s else "Student not found.")
            elif choice == "7":
                report()
            elif choice == "8":
                if students:
                    top = max(students, key=average)
                    print("Highest scorer:", top["name"], f"({average(top):.2f})")
                else:
                    print("No student records available.")
            elif choice == "9":
                dept = clean(input("Department: ")).upper()
                display_records([s for s in students if s["department"] == dept])
            elif choice == "10":
                print("Total students:", len(students))
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid number. Please enter numeric values correctly.")


if __name__ == "__main__":
    main()
