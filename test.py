"""
SPECS test scenarios
Project: mini-grades (v4)
"""

import subprocess
import os
import shutil
import pytest

# --- Constants ---
ID = "101"
ID_2 = "102"
NAME = "Berke"
NAME_2 = "Efe"
GRADE = "85"
LESSON = "Math"
LESSON_2 = "Science"
NONEXISTENT_ID = "999"

# --- Helper Functions ---
def run_cmd(args):
    """Executes the command in the terminal. Runs 'init' first to ensure the system is always ready."""
    subprocess.run(["python", "main.py", "init"], capture_output=True, text=True)
    result = subprocess.run(
        ["python", "main.py"] + args,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def add_student(id=ID, name=NAME):
    """Shortcut to add a student."""
    return run_cmd(["add-student", id, name])

def add_grade(id=ID, lesson=LESSON, grade=GRADE):
    """Shortcut to add a grade to a student under a lesson."""
    return run_cmd(["add-grade", id, lesson, grade])

def setup_student_with_grade(id=ID, name=NAME, lesson=LESSON, grade=GRADE):
    """Creates a student and assigns them a grade under a lesson."""
    add_student(id, name)
    add_grade(id, lesson, grade)

def setup_function():
    """Resets the .minigrades directory before each test."""
    if os.path.exists(".minigrades"):
        shutil.rmtree(".minigrades")

# --- add student tests ---
def test_add_student_success():
    """Tests the successful addition of a new student with a unique ID."""
    response = add_student()
    assert response == f"Student {ID} added successfully."

def test_add_student_duplicate():
    """Tests the 'Duplicate ID' error when attempting to add a student with an existing ID."""
    add_student()
    response = add_student(name="Efe")
    assert response == f"Adding student failed: student with ID {ID} already exists."

def test_add_student_non_numeric_id():
    """Tests the numeric value error when a non-numeric string is entered as an ID."""
    response = add_student(id="abc")
    assert response == "Adding student failed: ID must be a numeric value."

def test_add_student_non_alpha_name():
    """Tests the name validation error when a non-alphabetic name is entered."""
    response = add_student(name="Berke123")
    assert response == "Adding student failed: name must contain only letters."

# --- add grade tests ---
def test_add_grade_success():
    """Tests the successful addition of a grade under a lesson to an existing student."""
    add_student()
    response = add_grade(lesson=LESSON, grade="80")
    assert response == f"Lesson {LESSON} and grade 80 added for student {ID}."

def test_add_grade_new_lesson():
    """Tests adding a grade to a different (new) lesson for the same student."""
    setup_student_with_grade()
    response = add_grade(id=ID, lesson=LESSON_2, grade="90")
    assert response == f"Lesson {LESSON_2} and grade 90 added for student {ID}."

def test_add_grade_existing_lesson():
    """Tests adding a second grade to the same lesson for a student."""
    setup_student_with_grade()
    response = add_grade(id=ID, lesson=LESSON, grade="90")
    assert response == f"Lesson {LESSON} and grade 90 added for student {ID}."

def test_add_grade_non_numeric_grade():
    """Tests that the added grade must consist of numbers."""
    add_student()
    response = add_grade(grade="abc", lesson=LESSON)
    assert response == "Adding grade failed: ID and grade must be numeric values."

def test_add_grade_non_alpha_lesson():
    """Tests that the lesson name must contain only letters."""
    add_student()
    response = add_grade(lesson="Math123", grade="80")
    assert response == "Adding grade failed: lesson must contain only letters."

def test_add_grade_student_not_found():
    """Tests the error when trying to add a grade to a student ID that does not exist."""
    response = add_grade(id=NONEXISTENT_ID, lesson=LESSON, grade="80")
    assert response == f"Adding grade failed: no student found with ID {NONEXISTENT_ID}."

def test_add_grade_out_of_range():
    """Tests that the added grade must be between 0 and 100."""
    add_student()
    response = add_grade(lesson=LESSON, grade="101")
    assert response == "Adding grade failed: grade must be between 0 and 100."

# --- delete student tests ---
def test_delete_student_success():
    """Tests the deletion of an existing student via their ID."""
    add_student()
    response = run_cmd(["delete-student", ID])
    assert response == f"Student {ID} and all grades deleted successfully."

def test_delete_student_not_found():
    """Tests the error message when attempting to delete a non-existent ID."""
    response = run_cmd(["delete-student", NONEXISTENT_ID])
    assert response == f"Deleting student failed: no student found with ID {NONEXISTENT_ID}."

# --- delete grade tests ---
def test_delete_grade_success():
    """Tests the deletion of an existing grade from a lesson for a student."""
    setup_student_with_grade()
    response = run_cmd(["delete-grade", ID, LESSON, GRADE])
    assert response == f"Grade {GRADE} in lesson {LESSON} removed for student {ID}."

def test_delete_grade_non_numeric_id():
    """Tests that the ID must consist of numbers."""
    setup_student_with_grade()
    response = run_cmd(["delete-grade", "abc", LESSON, GRADE])
    assert response == "Deleting grade failed: ID and grade must be numeric values."

def test_delete_grade_non_numeric_grade():
    """Tests that the grade must consist of numbers."""
    setup_student_with_grade()
    response = run_cmd(["delete-grade", ID, LESSON, "abc"])
    assert response == "Deleting grade failed: ID and grade must be numeric values."

def test_delete_grade_non_alpha_lesson():
    """Tests that the lesson name must contain only letters."""
    setup_student_with_grade()
    response = run_cmd(["delete-grade", ID, "Math123", GRADE])
    assert response == "Deleting grade failed: lesson must contain only letters."

def test_delete_grade_out_of_range():
    """Tests that the grade must be between 0 and 100."""
    setup_student_with_grade()
    response = run_cmd(["delete-grade", ID, LESSON, "101"])
    assert response == "Deleting grade failed: grade must be between 0 and 100."

def test_delete_grade_student_not_found():
    """Tests the error when trying to delete a grade from a student ID that does not exist."""
    response = run_cmd(["delete-grade", NONEXISTENT_ID, LESSON, GRADE])
    assert response == f"Deleting grade failed: no student found with ID {NONEXISTENT_ID}."

def test_delete_grade_not_found():
    """Tests the error when trying to delete a grade that does not exist in the lesson."""
    setup_student_with_grade()
    response = run_cmd(["delete-grade", ID, LESSON, "90"])
    assert response == f"Deleting grade failed: grade 90 in {LESSON} not found for student {ID}."

# --- list students tests ---
def test_list_students_success():
    """Tests the listing of all registered students."""
    add_student()
    add_student(ID_2, NAME_2)
    response = run_cmd(["list"])
    assert "=== LIST OF STUDENTS ===" in response
    assert f"Student ID: {ID}" in response
    assert f"Name: {NAME}" in response
    assert f"Student ID: {ID_2}" in response
    assert f"Name: {NAME_2}" in response

def test_list_students_with_grades_success():
    """Tests the listing of students with lesson-based grades and averages."""
    setup_student_with_grade()
    add_student(ID_2, "Eren")
    add_grade(ID_2, LESSON, "90")
    response = run_cmd(["list"])
    assert "=== LIST OF STUDENTS ===" in response
    assert f"Student ID: {ID}" in response
    assert f"Name: {NAME}" in response
    assert f"Lesson 1: {LESSON}" in response
    assert f"Student ID: {ID_2}" in response
    assert f"Name: Eren" in response

def test_list_students_empty():
    """Tests the error when listing is requested while no students are registered."""
    response = run_cmd(["list"])
    assert response == "Listing students failed: no student records found."

# --- generate report tests ---
def test_generate_report_success():
    """Tests the successful generation of a report from system data."""
    setup_student_with_grade()
    response = run_cmd(["report"])
    assert response == "Report saved to .minigrades/report.md"
    assert os.path.exists(".minigrades/report.md")
    with open(".minigrades/report.md", "r", encoding="utf-8") as f:
        content = f.read()
    assert "MINI-GRADES STUDENT REPORT" in content
    assert "LESSON" in content
    assert LESSON in content

def test_generate_report_empty():
    """Tests the error when report generation is requested with no registered students."""
    response = run_cmd(["report"])
    assert response == "Report generation failed: no student data available."

# --- change grade tests ---
def test_change_grade_success():
    """Tests the successful change of an existing grade for a student."""
    setup_student_with_grade()
    response = run_cmd(["change-grade", ID, LESSON, GRADE, "90"])
    assert response == f"Grade {GRADE} changed to 90 for student {ID}."

def test_change_grade_non_numeric_id():
    """Tests the error when a non-numeric ID is provided for grade change."""
    setup_student_with_grade()
    response = run_cmd(["change-grade", "abc", LESSON, GRADE, "90"])
    assert response == "Changing grade failed: ID and grade must be numeric values."

def test_change_grade_non_numeric_old_grade():
    """Tests the error when a non-numeric old grade is provided for grade change."""
    setup_student_with_grade()
    response = run_cmd(["change-grade", ID, LESSON, "abc", "90"])
    assert response == "Changing grade failed: ID and grade must be numeric values."

def test_change_grade_non_numeric_new_grade():
    """Tests the error when a non-numeric new grade is provided for grade change."""
    setup_student_with_grade()
    response = run_cmd(["change-grade", ID, LESSON, GRADE, "abc"])
    assert response == "Changing grade failed: ID and grade must be numeric values."

def test_change_grade_non_alpha_lesson():
    """Tests the error when a non-alphabetic lesson name is provided."""
    setup_student_with_grade()
    response = run_cmd(["change-grade", ID, "Math123", GRADE, "90"])
    assert response == "Changing grade failed: lesson must contain only letters."

def test_change_old_grade_out_of_range():
    """Tests the error when an old grade is provided outside the valid range."""
    setup_student_with_grade()
    response = run_cmd(["change-grade", ID, LESSON, "150", "90"])
    assert response == "Changing grade failed: grade must be between 0 and 100."

def test_change_new_grade_out_of_range():
    """Tests the error when a new grade is provided outside the valid range."""
    setup_student_with_grade()
    response = run_cmd(["change-grade", ID, LESSON, GRADE, "-10"])
    assert response == "Changing grade failed: grade must be between 0 and 100."

def test_change_grade_student_not_found():
    """Tests the error when trying to change a grade for a student ID that does not exist."""
    response = run_cmd(["change-grade", NONEXISTENT_ID, LESSON, GRADE, "90"])
    assert response == f"Changing grade failed: no student found with ID {NONEXISTENT_ID}."

def test_change_grade_old_grade_not_found():
    """Tests the error when trying to change a grade that does not exist for the student."""
    setup_student_with_grade()
    response = run_cmd(["change-grade", ID, LESSON, "90", "95"])
    assert response == f"Changing grade failed: grade 90 not found for student {ID}."

# --- student info tests ---
def test_student_info_success():
    """Tests the successful retrieval of a student's information via their ID."""
    setup_student_with_grade()
    response = run_cmd(["student-info", ID])
    assert f"Info for student with ID {ID}:" in response
    assert f"Name: {NAME}" in response
    assert f"Lesson: {LESSON}" in response
    assert f"Student info retrieval for ID {ID} completed." in response

def test_student_info_no_grades():
    """Tests the retrieval of a student's information when they have no grades registered."""
    add_student()
    response = run_cmd(["student-info", ID])
    assert f"Info for student with ID {ID}:" in response
    assert f"Name: {NAME}" in response
    assert f"Student info retrieval for ID {ID} completed." in response

def test_student_info_not_found():
    """Tests the error when trying to retrieve information for a student ID that does not exist."""
    response = run_cmd(["student-info", NONEXISTENT_ID])
    assert response == f"Student info retrieval failed: no student found with ID {NONEXISTENT_ID}."

def test_student_info_non_numeric_id():
    """Tests the error when a non-numeric ID is provided for student information retrieval."""
    response = run_cmd(["student-info", "abc"])
    assert response == "Student info retrieval failed: ID must be a numeric value."

# --- check path test ---
def test_check_path():
    """Tests the error message when the system is not initialized and a command is entered."""
    if os.path.exists(".minigrades"):
        shutil.rmtree(".minigrades")

    result = subprocess.run(
        ["python", "main.py", "list"],
        capture_output=True,
        text=True
    )
    assert "Not initialized. Run: python main.py init" in result.stdout.strip()

# --- unknown command test ---
def test_unknown_command():
    """Tests the error provided when an unknown command is entered."""
    response = run_cmd(["hello"])
    assert "Unknown command: hello. Please check 'help' command for more information." in response

# --- clear data tests ---
def test_clear_data_success():
    """Tests the successful clearing of all data from the system."""
    setup_student_with_grade()
    response = run_cmd(["clear-data"])
    assert response == "All the data is going to be deleted. Are you sure? (Y/N):"

def test_clear_data_no_data():
    """Tests the error when trying to clear data while no data is present."""
    response = run_cmd(["clear-data"])
    assert response == "Clearing records failed: no student records found."

def test_clear_data_cancelled():
    add_student()
    response = run_cmd(["clear-data"])
    if response == "Clearing data operation cancelled.":
        print("Test passed!")
    else:
        print("Test failed!")
    run_cmd(["clear-data"])

def test_clear_data_invalid_value():
    add_student()
    response = run_cmd(["clear-data"])
    if response == "Invalid value. Please enter Y/N.":
        print("Test passed!")
    else:
        print("Test failed!")
    run_cmd(["clear-data"])

# --- activity log tests ---
def test_activity_log_success():
    """Tests the successful logging of an activity."""
    run_cmd(["init"])
    response = add_student()
    assert response == f"Student {ID} added successfully."
    assert os.path.exists(".minigrades/log.txt")
    with open(".minigrades/log.txt", "r") as f:
        assert "SUCCESS:" in f.read()

def test_activity_log_error():
    """Tests the successful logging of a failed activity."""
    run_cmd(["init"])
    response = add_student(id="abc")
    assert response == "Adding student failed: ID must be a numeric value."
    assert os.path.exists(".minigrades/log.txt")
    with open(".minigrades/log.txt", "r") as f:
        assert "ERROR:" in f.read()

# --- help tests ---
def test_help_no_command():
    """Tests the help command when no command is provided."""
    response = run_cmd(["help"])
    assert "========================================" in response
    assert "Welcome to minigrades. This is a CLI-based student management tool." in response
    assert "Usage: python main.py <command> [args]" in response
    assert "Commands:" in response
    for cmd in ["init", "add-student", "add-grade", "delete-student", "list",
                "delete-grade", "report", "change-grade", "student-info", "clear-data", "help"]:
        assert cmd in response
    assert "Please run 'python main.py help <command>' to get detailed information." in response

def test_help_with_command():
    """Tests the help command when a command is provided."""
    response = run_cmd(["help", "add-grade"])
    assert "=== ADD GRADE ===" in response
    assert "Adds a grade under a specific lesson for a student." in response
    assert "python main.py add-grade <id> <lesson> <grade>" in response

def test_help_nonexistent_command():
    """Tests the help command when an unknown command is provided."""
    response = run_cmd(["help", "hello"])
    assert "Unknown command: hello. Please check 'help' command for more information." in response
