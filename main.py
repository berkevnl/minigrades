import sys
from utils import *

# --- Command Table ---
# Format: "command": (min_args, handler_function, "usage string")
COMMANDS = {
    "add-student":    (4, lambda a: add_student(a[2], a[3]),             "python main.py add-student <id> <name>"),
    "add-grade":      (5, lambda a: add_grade(a[2], a[3], a[4]),               "python main.py add-grade <id> <lesson> <grade>"),
    "delete-student": (3, lambda a: delete_student(a[2]),                "python main.py delete-student <id>"),
    "delete-grade":   (5, lambda a: delete_grade(a[2], a[3], a[4]),            "python main.py delete-grade <id> <lesson> <grade>"),
    "change-grade":   (6, lambda a: change_grade(a[2], a[3], a[4], a[5]),     "python main.py change-grade <id> <lesson> <old_grade> <new_grade>"),
    "list":           (2, lambda a: list_students(),                     "python main.py list"),
    "report":         (2, lambda a: generate_report(),                   "python main.py report"),
    "student-info":   (3, lambda a: student_info(a[2]),                  "python main.py student-info <id>"),
    "clear-data":     (2, lambda a: clear_data(),                        "python main.py clear-data"),
    "clear-log":      (2, lambda a: clear_log(),                         "python main.py clear-log"),
}

# --- MAIN PROGRAM ---

if len(sys.argv) < 2:
    print(error_message("Usage: python main.py <command> [args]"))

elif sys.argv[1] == "init":
    print(initialize())

elif sys.argv[1] == "help":
    if len(sys.argv) < 3:
        print(help())
    else:
        print(help(sys.argv[2]))

elif sys.argv[1] in COMMANDS:
    if check_path():
        print(check_path())
    else:
        min_args, handler, usage = COMMANDS[sys.argv[1]]
        if len(sys.argv) < min_args:
            print(error_message(f"Usage: {usage}"))
        else:
            print(handler(sys.argv))

else:
    print(error_message(f"Unknown command: {sys.argv[1]}. Please check 'help' command for more information."))
