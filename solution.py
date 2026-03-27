"""
mini-grades v2 - advanced implementation

CHANGELOGS:
- Implemented loops and lists for dynamic data management.
- Added persistent grade storage using a 3-column delimited format (ID | Name | Grades).
- Enabled real-time average calculation with support for multiple grades per student.
- Refactored student listing to include automated performance reporting.
- Improved error handling for edge cases such as empty databases or missing grades.

add-student, add-grade, delete-student, delete-grade, calculate-average, list-students functions are working.
generate-report and change-grade functions will be implemented soon.
"""

import sys
import os

# --- FUNCTION DEFINITIONS ---

def initialize():
    """Creates the .minigrades directory and data file for the system to operate."""
    if os.path.exists(".minigrades"):
        return "Already initialized"
    os.mkdir(".minigrades")
    f = open(".minigrades/data.txt", "w")
    f.close()
    return "Initialized empty system in .minigrades/"

# -----------------------------------------------------------

def add_student(id, name):
    """Enables adding a new student to the system."""
    if not id.isdigit():
        return "Invalid input: Please enter a numeric value."
    
    if not os.path.exists(".minigrades/data.txt"):
        return "Not initialized. Run: python solution.py init"
    
    f_check = open(".minigrades/data.txt", "r")
    content = f_check.read()
    f_check.close()
    
    # Searching for ID with a delimiter ( |) to avoid partial matches (e.g., finding 1 inside 101).
    if id + " |" in content:
        return f"Error: Student with ID {id} already exists."
    
    f = open(".minigrades/data.txt", "a")
    # Saving data in a delimited format (ID | Name).
    f.write(id + " | " + name + "\n")
    f.close()

    return "Student added successfully."

# -----------------------------------------------------------

def add_grade(id, grade):
    """Enables adding a grade to a specific student."""
    if not id.isdigit():
        return "Invalid input: Please enter a numeric value."
    
    if not os.path.exists(".minigrades/data.txt"):
        return "Not initialized. Run: python solution.py init"
    
    if not grade.isdigit():
        return "Invalid input: Please enter a numeric value."
        
    if int(grade) < 0 or int(grade) > 100:
        return "Invalid grade: Grades must be between 0 and 100."

    updated_lines = []
    found = False

    with open(".minigrades/data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue

            parts = line.split(" | ")

            if parts[0] == id:
                found = True
                if len(parts) == 2:
                    line = f"{line} | {grade}"
                else:
                    line = f"{line},{grade}"
            
            updated_lines.append(line)
    
    if not found:
        return f"Error: No student found with ID {id}."
    
    with open(".minigrades/data.txt", "w") as f:
        for updated_line in updated_lines:
            f.write(updated_line + "\n")
    
    return f"Grades added successfully for student {id}."

# -----------------------------------------------------------

def delete_grade(id, grade):
    """Enables adding a grade to a specific student."""
    if not id.isdigit():
        return "Invalid input: Please enter a numeric value."
    
    if not grade.isdigit():
        return "Invalid input: Please enter a numeric value."
    
    if int(grade) < 0 or int(grade) > 100:
        return "Invalid grade: Grades must be between 0 and 100."
    
    if not os.path.exists(".minigrades/data.txt"):
        return "Not initialized. Run: python solution.py init"
    
    updated_lines = []
    student_found = False
    grade_found = False
    target_grade = int(grade)
    
    with open(".minigrades/data.txt", "r") as f:
        for line in f:
            line = line.strip()

            parts = line.split(" | ")
            if parts[0] == id:
                student_found = True
                if len(parts) > 2:
                    grades = parts[2]
                    grade_list = parts[2].split(",")
                    numbers = [int(g) for g in grade_list]
                    if target_grade in numbers:
                        grade_found = True
                        numbers.remove(target_grade)

                        new_grades_str = ",".join([str(n) for n in numbers])

                        if new_grades_str:
                            line = f"{parts[0]} | {parts[1]} | {new_grades_str}"
                        else:
                            line = f"{parts[0]} | {parts[1]}"

            updated_lines.append(line)
    
    if not student_found:
        return f"Error: No student found with ID {id}."
    
    if not grade_found:
        return f"Error: Grade {target_grade} not found for this student."
    
    with open(".minigrades/data.txt", "w") as f:
        for updated_line in updated_lines:
            f.write(updated_line + "\n")
    
    return f"Grade {target_grade} successfully removed!"

# -----------------------------------------------------------

def delete_student(id):
    """Enables deleting a student from the system."""
    if not os.path.exists(".minigrades/data.txt"):
        return "Not initialized. Run: python solution.py init"
    
    if not id.isdigit():
        return "Invalid input: Please enter a numeric value."

    updated_lines = []
    found = False
    
    with open(".minigrades/data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue

            parts = line.split(" | ")
            if parts[0] == id:
                found = True
                line = ""
            else:
                updated_lines.append(line)
    
    if not found:
        return f"Error: No student found with ID {id}."
    
    with open(".minigrades/data.txt", "w") as f:
        for updated_line in updated_lines:
            f.write(updated_line + "\n")
    
    return "Student and all grades deleted successfully."

# -----------------------------------------------------------

def list_students():
    """Lists all students currently in the system."""
    if not os.path.exists(".minigrades/data.txt"):
        return "Error: No students found in the system. Operation aborted."

    with open(".minigrades/data.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

        if not lines:
            return "Error: No students found in the system. Operation aborted."

        print("=== LIST OF STUDENTS ===\n")
        i = 1
        for line in lines:
            line = line.strip()

            parts = line.split(" | ")

            id_val = parts[0]
            name_val = parts[1]
            if len(parts) > 2:
                grades_val = parts[2]
            else:
                grades_val = "None"

            print(
                f"Student {i}\n",
                "---------------\n",
                f"ID: {id_val}\n",
                f"Name: {name_val}\n",
                f"Grades: {grades_val}\n",
                f"{calculate_average(id_val)}\n"
                "---------------\n",
            )
            i+=1

    return ""

# -----------------------------------------------------------

def calculate_average(id):
    """Calculates the average of a student (v0 Simulation)."""
    if not os.path.exists(".minigrades/data.txt"):
        return "Not initialized. Run: python solution.py init"
    
    found = False
    
    with open(".minigrades/data.txt", "r") as f:
        for line in f:
            line = line.strip()
            
            parts = line.split(" | ")
            if parts[0] == id:
                found = True
                if len(parts) > 2:
                    grades = parts[2]
                    grade_list = grades.split(",")
                    numbers = [int(g) for g in grade_list]
                    average = sum(numbers)/len(grade_list)
                    return f"Average for student {id} is {average:.2f}."
                else:
                    return f"Error: Could not calculate average for student {id}."
    
    if not found:
        return f"Error: No student found with ID {id}."
    
# -----------------------------------------------------------

def generate_report():
    """Generates a report file from the system data."""
    if not os.path.exists(".minigrades/data.txt"):
        return "Error: No data available to generate a report."
    
    f = open(".minigrades/data.txt", "r")
    current_data = f.read()
    f.close()

    if current_data == "":
        return "Error: No data available to generate a report."
    
    r = open(".minigrades/report.txt", "w")
    r.write("ID | NAME | GRADES\n-----------\n")
    r.write(current_data)
    r.close()

    return "Report saved to .minigrades/report.txt"

# --- MAIN PROGRAM ---

if len(sys.argv) < 2:
    print("Usage: python solution.py <command> [args]")

elif sys.argv[1] == "init":
    print(initialize())

elif sys.argv[1] == "add":
    if len(sys.argv) < 4:
        print("Usage: python solution.py add <id> <name>")
    else:
        print(add_student(sys.argv[2], sys.argv[3]))

elif sys.argv[1] == "add-grade":
    if len(sys.argv) < 4:
        print("Usage: python solution.py add-grade <id> <grades>")
    else:
        print(add_grade(sys.argv[2], sys.argv[3]))

elif sys.argv[1] == "delete":
    if len(sys.argv) < 3:
        print("Usage: python solution.py delete <id>")
    else:
        print(delete_student(sys.argv[2]))

elif sys.argv[1] == "list":
    print(list_students())

elif sys.argv[1] == "del-grade":
    if len(sys.argv) < 4:
        print("Usage: python solution.py del-grade <id> <grade>")
    else:
        print(delete_grade(sys.argv[2], sys.argv[3]))

elif sys.argv[1] == "report":
    print(generate_report())

elif sys.argv[1] == "calc-avg":
    if len(sys.argv) < 3:
        print("Usage: python solution.py calc-avg <id>")
    else:
        print(calculate_average(sys.argv[2]))

else:
    print("Unknown command: " + sys.argv[1] + ". Please select from the menu.")
