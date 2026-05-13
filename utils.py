import os
from datetime import datetime
from colorama import Fore, Style, init

init()

# --- Constants ---
LESSONS_AND_GRADES = {}
BASE_DIR = ".minigrades"
DATA_FILE = os.path.join(BASE_DIR, "data.txt")
LOG_FILE = os.path.join(BASE_DIR, "log.txt")
REPORT_FILE = os.path.join(BASE_DIR, "report.md")

# --- Utility Functions ---

def check_path():
    """Checks if the .minigrades directory exists."""
    if not os.path.exists(BASE_DIR):
        return error_message("Not initialized. Run: python main.py init")
    return ""

# -----------------------------------------------------------

def success_message(msg):
    """Returns a green-colored success message."""
    return Fore.GREEN + msg + Style.RESET_ALL

def error_message(msg):
    """Returns a red-colored error message."""
    return Fore.RED + msg + Style.RESET_ALL

def question_message(msg):
    """Returns a magenta-colored question message."""
    return Fore.MAGENTA + msg + Style.RESET_ALL

def info_message(msg):
    """Returns a cyan-colored info message."""
    return Fore.CYAN + msg + Style.RESET_ALL

def help_message(msg):
    """Returns a yellow-colored help message."""
    return Fore.YELLOW + msg + Style.RESET_ALL

# -----------------------------------------------------------

def activity_log(activity, state):
    """Saves an activity entry to the log file."""
    current_datetime = datetime.now()
    with open(LOG_FILE, "a") as f:
        f.write(f"{state}: [{current_datetime.strftime('%Y-%m-%d %H:%M:%S')}] {activity}\n")

def log_and_return(message, status):
    """Logs the activity and returns an appropriately colored message."""
    activity_log(message, status)
    formatters = {"SUCCESS": success_message, "ERROR": error_message, "INFO": info_message}
    return formatters[status](message)

# -----------------------------------------------------------

def read_students():
    """Reads all non-empty student lines from data.txt."""
    with open(DATA_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def write_students(lines):
    """Writes student lines back to data.txt."""
    with open(DATA_FILE, "w") as f:
        for line in lines:
            f.write(line + "\n")

def parse_student(line):
    """Parses a data line into (id, name, grades_string or None)."""
    parts = line.split(" | ")
    return parts[0], parts[1], parts[2] if len(parts) > 2 else None

def parse_grades(grades_str):
    """Converts a comma-separated grades string into a list of integers."""
    return [int(g) for g in grades_str.split(",")]

def format_grades(numbers):
    """Converts a list of grade integers back to a comma-separated string."""
    return ",".join(str(n) for n in numbers)

def build_student_line(s_id, s_name, grades_str=None):
    """Builds a data line from student components."""
    if grades_str:
        return f"{s_id} | {s_name} | {grades_str}"
    return f"{s_id} | {s_name}"

# --- Core Functions ---

def initialize():
    """Creates the .minigrades directory and data file for the system to operate."""
    if os.path.exists(BASE_DIR):
        return log_and_return("Already initialized. No changes made.", "INFO")
    os.mkdir(BASE_DIR)
    open(DATA_FILE, "w").close()
    return log_and_return("Initialized empty system in .minigrades/", "SUCCESS")

# -----------------------------------------------------------

def add_student(id, name):
    """Enables adding a new student to the system."""
    if not id.isdigit():
        return log_and_return("Adding student failed: ID must be a numeric value.", "ERROR")

    if not name.isalpha():
        return log_and_return("Adding student failed: name must contain only letters.", "ERROR")

    # Searching for ID with a delimiter ( |) to avoid partial matches (e.g., finding 1 inside 101).
    with open(DATA_FILE, "r") as f:
        if id + " |" in f.read():
            return log_and_return(f"Adding student failed: student with ID {id} already exists.", "ERROR")

    with open(DATA_FILE, "a") as f:
        f.write(build_student_line(id, name) + "\n")

    return log_and_return(f"Student {id} added successfully.", "SUCCESS")

# -----------------------------------------------------------

def add_grade(id, lesson, grade):
    """Adds a grade under a specific lesson for a student.

    Data format per student line:
        id | name | Lesson1: g1,g2 | Lesson2: g3
    - New lesson  → added with pipe (|)
    - Existing lesson → grade appended with comma (,)
    """
    if not id.isdigit() or not grade.isdigit():
        return log_and_return("Adding grade failed: ID and grade must be numeric values.", "ERROR")

    if not lesson.isalpha():
        return log_and_return("Adding grade failed: lesson must contain only letters.", "ERROR")

    if int(grade) < 0 or int(grade) > 100:
        return log_and_return("Adding grade failed: grade must be between 0 and 100.", "ERROR")

    updated_lines = []
    student_found = False

    for line in read_students():
        s_id = line.split(" | ")[0]
        if s_id == id:
            student_found = True
            parts = line.split(" | ")

            # Scan existing lessons
            lesson_found = False
            for i in range(2, len(parts)):
                if parts[i].startswith(f"{lesson}:"):
                    # Lesson already exists → append grade with comma
                    parts[i] = f"{parts[i]},{grade}"
                    lesson_found = True
                    break

            if not lesson_found:
                # New lesson → append with pipe
                parts.append(f"{lesson}: {grade}")

            line = " | ".join(parts)
        updated_lines.append(line)

    if not student_found:
        return log_and_return(f"Adding grade failed: no student found with ID {id}.", "ERROR")

    write_students(updated_lines)
    return log_and_return(f"Lesson {lesson} and grade {grade} added for student {id}.", "SUCCESS")

# -----------------------------------------------------------

def delete_grade(id, lesson, grade):
    """Deletes a specific grade from a lesson for a student.

    Parses the student line, finds the lesson segment, removes
    the grade. If the lesson has no grades left, removes the segment.
    """
    if not id.isdigit() or not grade.isdigit():
        return log_and_return("Deleting grade failed: ID and grade must be numeric values.", "ERROR")

    if not lesson.isalpha():
        return log_and_return("Deleting grade failed: lesson must contain only letters.", "ERROR")

    if int(grade) < 0 or int(grade) > 100:
        return log_and_return("Deleting grade failed: grade must be between 0 and 100.", "ERROR")

    updated_lines = []
    student_found = False
    grade_found = False
    target_grade = grade  # will be compared as a string

    for line in read_students():
        s_id = line.split(" | ")[0]
        if s_id == id:
            student_found = True
            parts = line.split(" | ")

            for i in range(2, len(parts)):
                if parts[i].startswith(f"{lesson}:"):
                    # "Math: 50,75" → ["50", "75"]
                    grades_str = parts[i].split(": ", 1)[1]
                    grades_list = grades_str.split(",")

                    if target_grade in grades_list:
                        grade_found = True
                        grades_list.remove(target_grade)

                        if grades_list:
                            # Lesson still has grades → update
                            parts[i] = f"{lesson}: {','.join(grades_list)}"
                        else:
                            # No grades left in lesson → remove segment
                            parts.pop(i)
                    break

            line = " | ".join(parts)
        updated_lines.append(line)

    if not student_found:
        return log_and_return(f"Deleting grade failed: no student found with ID {id}.", "ERROR")

    if not grade_found:
        return log_and_return(f"Deleting grade failed: grade {target_grade} in {lesson} not found for student {id}.", "ERROR")

    write_students(updated_lines)
    return log_and_return(f"Grade {target_grade} in lesson {lesson} removed for student {id}.", "SUCCESS")

# -----------------------------------------------------------

def delete_student(id):
    """Enables deleting a student from the system."""
    if not id.isdigit():
        return log_and_return("Deleting student failed: ID must be a numeric value.", "ERROR")

    updated_lines = []
    found = False

    for line in read_students():
        s_id, _, _ = parse_student(line)
        if s_id == id:
            found = True
        else:
            updated_lines.append(line)

    if not found:
        return log_and_return(f"Deleting student failed: no student found with ID {id}.", "ERROR")

    write_students(updated_lines)
    return log_and_return(f"Student {id} and all grades deleted successfully.", "SUCCESS")

# -----------------------------------------------------------

def list_students():
    """Lists all students currently in the system."""
    students = read_students()

    if not students:
        return log_and_return("Listing students failed: no student records found.", "ERROR")

    print(info_message("\n=== LIST OF STUDENTS ===\n"))
    print(info_message("===================="))
    for line in read_students():
        parts = line.split(" | ")
        s_id = parts[0]
        s_name = parts[1]
        print(question_message(f"Student ID: {parts[0]}"))
        print(question_message(f"Name: {s_name}"))
        for i in range(2, len(parts)):
            lesson = parts[i].split(":")[0]
            grades = parts[i].split(":")[1]
            print(help_message((f"Lesson {i-1}: {lesson} - Grades:{grades} - Average: {calculate_average(lesson, s_id)}")))
        print(info_message("===================="))

    return ""

# -----------------------------------------------------------

def calculate_average(lesson, id):
    """Calculates the average for a specific lesson of a student."""
    for line in read_students():
        s_id = line.split(" | ")[0]
        if s_id == id:
            parts = line.split(" | ")
            for i in range(2, len(parts)):
                if parts[i].startswith(f"{lesson}:"):
                    grades_str = parts[i].split(":", 1)[1]
                    grades_list = grades_str.split(",")
                    numbers = [int(grade) for grade in grades_list]
                    average = sum(numbers) / len(numbers)
                    return average
                    
    return log_and_return(f"Calculating average failed: no student found with ID {id}.", "ERROR")

# -----------------------------------------------------------

def change_grade(id, lesson, old_grade, new_grade):
    """Enables changing an existing grade for a student to a new value."""

    if not lesson.isalpha():
        return log_and_return("Changing grade failed: lesson must contain only letters.", "ERROR")

    try:
        val_id = int(id)
        val_old = int(old_grade)
        val_new = int(new_grade)
    except ValueError:
        return log_and_return("Changing grade failed: ID and grade must be numeric values.", "ERROR")

    if val_old < 0 or val_old > 100 or val_new < 0 or val_new > 100:
        return log_and_return("Changing grade failed: grade must be between 0 and 100.", "ERROR")

    updated_lines = []
    student_found = False
    grade_found = False

    for line in read_students():
        s_id = line.split(" | ")[0]
        if s_id == id:
            student_found = True
            parts = line.split(" | ")

            for i in range(2, len(parts)):
                if parts[i].startswith(f"{lesson}:"):
                    grades_str = parts[i].split(": ", 1)[1]
                    grades_list = grades_str.split(",")

                    if old_grade in grades_list:
                        grade_found = True
                        idx = grades_list.index(old_grade)
                        grades_list.remove(old_grade)
                        grades_list.insert(idx, new_grade)
                        parts[i] = f"{lesson}: {','.join(grades_list)}"
                    break

            line = " | ".join(parts)
        updated_lines.append(line)

    if not student_found:
        return log_and_return(f"Changing grade failed: no student found with ID {id}.", "ERROR")

    if not grade_found:
        return log_and_return(f"Changing grade failed: grade {old_grade} not found for student {id}.", "ERROR")

    write_students(updated_lines)
    return log_and_return(f"Grade {old_grade} changed to {new_grade} for student {id}.", "SUCCESS")

# -----------------------------------------------------------

def student_info(id):
    """Provides detailed information about a specific student."""
    if not id.isdigit():
        return log_and_return("Student info retrieval failed: ID must be a numeric value.", "ERROR")

    for line in read_students():
        s_id = line.split(" | ")[0]
        if s_id == id:
            parts = line.split(" | ")
            s_name = parts[1]

            print(info_message("============================="))
            print(info_message(f"Info for student with ID {id}:"))
            print(info_message("============================="))
            print(help_message(f"Name: {s_name}"))
            for i in range(2, len(parts)):
                lesson = parts[i].split(":")[0]
                grades = parts[i].split(":")[1]
                avg = calculate_average(lesson, id)
                avg_display = f"{avg:.2f}"
                print(help_message(f"Lesson: {lesson} - Grades:{grades} - Average: {avg_display}"))
            print(info_message("=============================\n"))

            return log_and_return(f"Student info retrieval for ID {id} completed.", "SUCCESS")

    return log_and_return(f"Student info retrieval failed: no student found with ID {id}.", "ERROR")

# -----------------------------------------------------------

def generate_report():
    """Reads student records and generates a formatted markdown report."""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return log_and_return("Report generation failed: no student data available.", "ERROR")

    try:
        students = read_students()

        with open(REPORT_FILE, "w", encoding="utf-8") as rf:
            rf.write("# MINI-GRADES STUDENT REPORT\n\n")
            rf.write("| ID         | NAME            | LESSON     | GRADES   | AVERAGE    |\n")
            rf.write("|------------|-----------------|------------|----------|------------|\n")

            for line in students:
                if "|" not in line:
                    continue
                parts = line.split(" | ")
                s_id = parts[0]
                s_name = parts[1]

                for idx, i in enumerate(range(2, len(parts))):
                    lesson = parts[i].split(":")[0].strip()
                    grades = parts[i].split(":", 1)[1].strip()
                    avg = calculate_average(lesson, s_id)
                    avg_display = f"{avg:.2f}" if avg is not None else "None"

                    if idx == 0:
                        # First lesson row → show ID and Name
                        rf.write(f"| {s_id:<10} | {s_name:<15} | {lesson:<10} | {grades:<8} | {avg_display:<10} |\n")
                    else:
                        # Subsequent lessons → ID and Name left blank
                        rf.write(f"| {'':10} | {'':15} | {lesson:<10} | {grades:<8} | {avg_display:<10} |\n")

                # Separator between students
                rf.write(f"|{'---':->12}|{'---':->17}|{'---':->12}|{'---':->10}|{'---':->12}|\n")

        return log_and_return("Report saved to .minigrades/report.md", "SUCCESS")

    except IOError as e:
        return log_and_return(f"Report generation failed: could not process report files. {e}", "ERROR")

# -----------------------------------------------------------

def clear_data():
    """Deletes all the students from data."""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return log_and_return("Clearing records failed: no student records found.", "ERROR")

    verification = input(question_message("All the data is going to be deleted. Are you sure? (Y/N): "))
    if verification.lower() in ["y", "yes"]:
        open(DATA_FILE, "w").close()
        return log_and_return("All the students deleted successfully.", "SUCCESS")
    elif verification.lower() in ["n", "no"]:
        return log_and_return("Clearing data operation cancelled.", "INFO")
    else:
        return log_and_return("Clearing data failed: invalid value.", "ERROR")

# -----------------------------------------------------------

def clear_log():
    """Deletes all the content from log.txt."""
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        return error_message("Clearing log failed: no log records found.")

    open(LOG_FILE, "w").close()
    return log_and_return("Log cleared successfully.", "SUCCESS")

# -----------------------------------------------------------

def help(command=None):
    """Provides a help message with usage instructions for the CLI."""
    if command is None:
        return help_message(
            "========================================\n"
            "Welcome to minigrades. This is a CLI-based student management tool.\n"
            "Usage: python main.py <command> [args]\n\n"
            "Commands:\n"
            "  init                Initializes the system\n"
            "  add-student         Adds a new student\n"
            "  add-grade           Adds a grade under a lesson for a student\n"
            "  delete-student      Deletes the student\n"
            "  list                Lists all students\n"
            "  delete-grade        Deletes a specific grade from a lesson\n"
            "  report              Generates a formatted report\n"
            "  change-grade        Changes an existing grade in a lesson\n"
            "  student-info        Displays detailed information of a student\n"
            "  clear-data          Deletes all student records\n"
            "  clear-log           Clears the activity log\n"
            "  help                Displays this message\n"
            "========================================\n"
            "Please run 'python main.py help <command>' to get detailed information.\n"
        )

    commands = {
        "init": ("INIT", "Initializes the system by creating a .minigrades directory and a data.txt file.", "python main.py init"),
        "add-student": ("ADD STUDENT", "Adds a new student to the system.", "python main.py add-student <id> <name>"),
        "add-grade": ("ADD GRADE", "Adds a grade under a specific lesson for a student.", "python main.py add-grade <id> <lesson> <grade>"),
        "delete-student": ("DELETE STUDENT", "Deletes the student.", "python main.py delete-student <id>"),
        "list": ("LIST", "Lists all students.", "python main.py list"),
        "delete-grade": ("DELETE GRADE", "Deletes a specific grade from a lesson for a student.", "python main.py delete-grade <id> <lesson> <grade>"),
        "report": ("REPORT", "Generates a formatted report.", "python main.py report"),
        "change-grade": ("CHANGE GRADE", "Changes an existing grade in a lesson for a student.", "python main.py change-grade <id> <lesson> <old_grade> <new_grade>"),
        "student-info": ("STUDENT INFO", "Displays detailed information of a student.", "python main.py student-info <id>"),
        "clear-data": ("CLEAR DATA", "Deletes all student records.", "python main.py clear-data"),
        "clear-log": ("CLEAR LOG", "Clears the activity log.", "python main.py clear-log"),
        "help": ("HELP", "Displays this message.", "python main.py help"),
    }

    if command in commands:
        title, desc, usage = commands[command]
        return help_message(f"=== {title} ===\n{desc}\nUsage: {usage}\n")

    return error_message(f"Unknown command: {command}. Please check 'help' command for more information.")