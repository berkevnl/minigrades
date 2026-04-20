# Mini-Grades (v3)

`mini-grades` is a robust Command-Line Interface (CLI) tool designed for managing student records and academic performance. After a successful initial release (v2) that laid the groundwork for student management, v3 introduces significant enhancements in functionality, data handling, and user experience.

---

## 📜 CHANGELOG

### [v2.0] -> [v3.0]
- **Change Grade Functionality:** Added a `change_grade` function to accept both old and new grades, allowing for precise grade modifications.
- **Student Info Retrieval:** Introduced a `student_info` function to fetch and display comprehensive student details, including ID, name, grades, and average.
- **Check Path Validation:** Implemented a `check_path` function to ensure the necessary directory and file structure exists before performing operations.

---

## 🚀 Key Features
* **Dynamic Data Handling:** Transitioned from manual string indexing to iterative processing using **loops**.
* **Functional Deletion:** Implemented actual deletion logic that removes student records from `data.txt` based on ID.
* **Persistent Grade Management:** Enabled appending new grades to existing records and calculating averages in real-time.
* **Mathematical Processing:** Integrated average calculation using Python's built-in functions for accurate results.
* **Enhanced CLI Output:** Optimized formatting for student listings and reporting.

---

## 📋 Operations Status

| Feature | Status | Description |
| :--- | :---: | :--- |
| **Initialize System** | ✅ | Sets up `.minigrades/data.txt` storage |
| **Add Student** | ✅ | Registers a new student record |
| **Add Grade** | ✅ | Appends new numeric grades to students |
| **Delete Student** | ✅ | Removes a student entry by ID |
| **List Students** | ✅ | Displays all students with details |
| **Calculate Average** | ✅ | Computes real-time GPA based on grades |
| **Change Grade** | ✅ | Modifies an existing grade entry |
| **Delete Grade** | ✅ | Removes a specific grade from a student |
| **Student Info** | ✅ | Displays name, grades, and average |
| **Generate Report** | ✅ | Creates a formatted report of all students |
| **Check Path** | ✅ | Ensures file system integrity |

## 🛠️ Technical Foundation
While v2 focused on establishing the core architecture, v3 builds upon that foundation with enhanced logic and data handling techniques.
* **Language:** Python 3.13.x
* **Logic:** Iterative processing (Loops) and dynamic storage (Lists).
* **File Management:** Advanced stream manipulation using the `with open()` pattern for safer I/O operations.
* **Validation:** Updated `pytest` suite to cover iterative edge cases.

![Tests](https://img.shields.io/badge/Tests-36%2F36%20Passed-darkgreen)

---

## 📂 Project Structure

```text
minigrades/
├── .minigrades/        # Persistent storage directory (Generated at runtime)
│   └── data.txt        # Student records (ID | Name | Grades)
    └── report.txt      # Formatted student report
├── solution.py         # Core CLI application logic
├── test.py             # Pytest suite for iterative logic
└── README.md           # Documentation
└── SPEC.txt            # Project specifications
```

---

## ⚙️ Getting Started

```bash
# 1. Initialize the system
python solution.py init
# Output: "Initialized empty system in .minigrades/"

# 2. Add a student
python solution.py add 101 Berke
# Output: "Student Berke with ID 101 added successfully."

# 3. Add grades
python solution.py add-grade 101 85
# Output: "Grade 85 added for student 101."

# 4. Calculate average
python solution.py calc-avg 101
# Output: "Average for student 101 is 85.00."

# 5. Change a grade
python solution.py change-grade 101 85 90
# Output: "Grade 85 changed to 90 for student 101 successfully!"

# 6. Get student info
python solution.py student-info 101
# Output: "ID: 101, Name: Berke, Grades: 90, Average: 90.00."

# 7. List all students
python solution.py list

# 8. Run automated tests
pytest test.py
