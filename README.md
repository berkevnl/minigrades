# Mini-Grades (v1)

`mini-grades` is a robust Command-Line Interface (CLI) tool designed for managing student records and academic performance. This project goes beyond basic functionality, emphasizing **Defensive Programming**, **Unit Testing**, and **Persistent Data Structuring** using low-level file I/O operations.

---

## 🚀 Key Features (v1)
* **CLI Architecture:** Operates through parametric commands (`init`, `add`, `list`, etc.) for a streamlined user experience.
* **Data Persistence:** Records are stored locally within a structured `.minigrades/` directory to ensure data integrity across sessions.
* **Advanced Error Handling:** Comprehensive validation for non-numeric inputs, duplicate IDs, and uninitialized system states.
* **TDD (Test-Driven Development):** Fully verified with a custom suite of 15 `pytest` scenarios (**100% Pass Rate**).
* **Professional Reporting:** Generates human-readable, formatted tables in `report.txt`.

---

## 🛠️ Technical Foundation
Developed with intentional constraints to master the core building blocks of software engineering without relying on high-level data structures (loops/lists) in this version:
* **Language:** Python 3.13.2
* **File Management:** Direct stream manipulation using `os` and `sys` modules.
* **Pattern Matching:** Implemented a custom separator pattern (`ID | Name`) to ensure unique ID identification and prevent data collision.
* **Validation:** Automated functional verification via `pytest`.

---

## 📂 Getting Started

```bash
# 1. Initialize the system
python solution.py init

# 2. Add a student
python solution.py add 101 Berke

# 3. List all students
python solution.py list

# 4. Run automated tests
pytest test.py
```
---
Author: berkevnl

Version: v1.0