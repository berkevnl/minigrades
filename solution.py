"""
mini-grades v3 - advanced implementation

CHANGELOGS:
- student_info function added to provide detailed information about a specific student.
- change_grade function implemented to allow modification of existing grades for a student.
- check_path function enhanced to validate the existence of necessary directories and files before operations.
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
    
    if not name.isalpha():
        return "Invalid input: Please enter a valid name consisting of letters only."
    
    path_check()
    
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
    if not id.isdigit() or not grade.isdigit():
        return "Invalid input: Please enter a numeric value."
    
    if int(grade) < 0 or int(grade) > 100:
        return "Invalid grade: Grades must be between 0 and 100."
    
    path_check()

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
    if not id.isdigit() or not grade.isdigit():
        return "Invalid input: Please enter a numeric value."
    
    if int(grade) < 0 or int(grade) > 100:
        return "Invalid grade: Grades must be between 0 and 100."
    
    path_check()
    
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
    path_check()
    
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
    path_check()

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
    """Calculates the average of a student."""
    if not id.isdigit():
        return "Invalid input: Please enter a numeric value."
    
    path_check()
    
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

def change_grade(id, old_grade, new_grade):
    """Enables changing an existing grade for a student to a new value."""
    try:
        val_id = int(id)
        val_old = int(old_grade)
        val_new = int(new_grade)
    except ValueError:
        return "Invalid input: Please enter a numeric value."
    
    if val_old < 0 or val_old > 100 or val_new < 0 or val_new > 100:
        return "Invalid grade: Grades must be between 0 and 100."
    
    path_check()
    
    updated_lines = []
    student_found = False
    grade_found = False

    with open(".minigrades/data.txt", "r") as f:
        for line in f:
            line = line.strip()

            parts = line.split(" | ")

            if parts[0] == id:
                student_found = True
                if len(parts) > 2:
                    grades = parts[2]
                    grade_list = grades.split(",")
                    numbers = [int(g) for g in grade_list]
                    if int(old_grade) in numbers:
                        grade_found = True
                        grade_index = numbers.index(int(old_grade))
                        numbers.remove(int(old_grade))
                        numbers.insert(grade_index, int(new_grade))
                        new_grades_str = ",".join([str(n) for n in numbers])
                        if new_grades_str:
                            line = f"{parts[0]} | {parts[1]} | {new_grades_str}"
                        else:
                            line = f"{parts[0]} | {parts[1]}"
                        
            updated_lines.append(line)
        
        if not student_found:
            return f"Error: No student found with ID {id}."
        
        if not grade_found:
            return f"Error: Grade {old_grade} not found for this student."
        
        with open (".minigrades/data.txt", "w") as f:
            for updated_line in updated_lines:
                f.write(updated_line + "\n")
        
        return f"Grade {old_grade} changed to {new_grade} for student {id} successfully!"
                    

# -----------------------------------------------------------

def student_info(id):
    """Provides detailed information about a specific student."""
    if not id.isdigit():
        return "Invalid input: Please enter a numeric value."
    path_check()

    found = False

    with open(".minigrades/data.txt", "r") as f:
        for line in f:
            line = line.strip()

            parts = line.split(" | ")
            
            if len(parts) > 2:
                grades_val = parts[2]
            else:
                grades_val = "None"

            if parts[0] == id:
                found = True
                info = (
                    "=====================================\n"
                    f"Information for student with ID {parts[0]}:\n"
                    "=====================================\n"
                    f"Name: {parts[1]}\n"
                    f"Grades: {grades_val}\n"
                    f"Average: {calculate_average(id)}\n"
                    "====================================="
                )
                return info
        
        if not found:
            return f"Error: No student found with ID {id}."
        
        return ""

# -----------------------------------------------------------

def path_check():
    """Checks if the .minigrades directory and data.txt file exist."""
    if not os.path.exists(".minigrades"):
        return "Not initialized. Run: python solution.py init"
    return ""

# -----------------------------------------------------------

def generate_report():
    """
    Reads student records from data.txt and generates a formatted, 
    user-friendly table in report.txt.
    
    Follows PEP-8 standards and ensures DRY principles by handling 
    file operations safely.
    """
    base_dir = ".minigrades"
    data_file = os.path.join(base_dir, "data.txt")
    report_file = os.path.join(base_dir, "report.txt")

    # Check if data file exists and has content (DRY: Centralized validation)
    if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
        print("Error: No data available to generate a report.")
        return ""

    try:
        with open(data_file, "r", encoding="utf-8") as f:
            records = f.readlines()

        with open(report_file, "w", encoding="utf-8") as rf:
            # Table Header Construction
            header = f"{'ID':<10} | {'NAME':<15} | {'GRADES':<20} | {'AVERAGE':<10}"
            rf.write("=== MINI-GRADES STUDENT REPORT ===\n")
            rf.write("\n")
            rf.write(header + "\n")
            rf.write("-" * len(header) + "\n")

            for record in records:
                if "|" not in record:
                    continue
                
                # Parsing logic with list comprehension for clean data
                parts = [p.strip() for p in record.split("|")]
                
                # Unpack with defaults to prevent IndexErrors (DRY & Safe)
                s_id = parts[0]
                s_name = parts[1]
                s_grades = parts[2] if len(parts) > 2 else "None"
                s_avg = calculate_average(s_id)

                # Standardized row formatting
                row = f"{s_id:<10} | {s_name:<15} | {s_grades:<20} | {s_avg:<10}"
                rf.write(row + "\n")

        print(f"Report saved to {report_file}")

    except IOError as e:
        print(f"Error: Could not process report files. {e}")
    return ""

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

elif sys.argv[1] == "delete-student":
    if len(sys.argv) < 3:
        print("Usage: python solution.py delete-student <id>")
    else:
        print(delete_student(sys.argv[2]))

elif sys.argv[1] == "list":
    print(list_students())

elif sys.argv[1] == "delete-grade":
    if len(sys.argv) < 4:
        print("Usage: python solution.py delete-grade <id> <grade>")
    else:
        print(delete_grade(sys.argv[2], sys.argv[3]))

elif sys.argv[1] == "report":
    print(generate_report())

elif sys.argv[1] == "calc-avg":
    if len(sys.argv) < 3:
        print("Usage: python solution.py calc-avg <id>")
    else:
        print(calculate_average(sys.argv[2]))

elif sys.argv[1] == "change-grade":
    if len(sys.argv) < 4:
        print("Usage: python solution.py change-grade <id> <grade> <new_grade>")
    else:
        print(change_grade(sys.argv[2], sys.argv[3], sys.argv[4]))

elif sys.argv[1] == "student-info":
    if len(sys.argv) < 3:
        print("Usage: python solution.py student-info <id>")
    else:
        print(student_info(sys.argv[2]))

else:
    print("Unknown command: " + sys.argv[1] + ". Please select from the menu.")
