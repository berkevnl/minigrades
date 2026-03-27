# Mini-Grades (v2)

`mini-grades` is a robust Command-Line Interface (CLI) tool designed for managing student records and academic performance. After a successful v1 release focusing on core architecture, **v2** introduces dynamic data processing and iterative logic.

---

## 🚀 Key Features (v2)
* **Dynamic Data Handling:** Transitioned from manual string indexing to iterative processing using **loops**.
* **Functional CRUD Operations:** v2 now supports **actual deletion** by rewriting file streams without the targeted ID.
* **Persistent Grade Management:** Grades are now processed and appended to student records persistently.
* **Mathematical Processing:** Implemented logic to parse string-based grades into numerical values for real-time calculation.
* **Enhanced CLI Output:** Optimized formatting for student listings and reporting.

---

## 📜 CHANGELOG

### [v1.0] -> [v2.0]
- **From Simulation to Reality:** Replaced placeholder messages in `delete` and `calc-avg` with functional algorithms.
- **Iteration Implementation:** Integrated **for/while loops** to process `data.txt` line-by-line.
- **Data Structure Shift:** Adopted **Python Lists** to temporarily hold and filter records during file updates.
- **Improved Pattern Matching:** Refined ID detection to ensure 100% accuracy during deletion and grade appending.

---

## 🛠️ Technical Foundation
While v1 was built with intentional constraints, **v2** leverages high-level logic to manage data more efficiently:
* **Language:** Python 3.13.2
* **Logic:** Iterative processing (Loops) and dynamic storage (Lists).
* **File Management:** Advanced stream manipulation using the `with open()` pattern for safer I/O operations.
* **Validation:** Updated `pytest` suite to cover iterative edge cases.

---

## 📂 Getting Started

```bash
# 1. Initialize the system
python solution.py init

# 2. Add a student
python solution.py add 101 Berke

# 3. Add grades
python solution.py add-grade 101 85

# 4. Calculate average
python solution.py calc-avg 101

# 5. List all students
python solution.py list

# 5. Run automated tests
pytest test.py
