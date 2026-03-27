"""
mini-grades SPECS için test senaryoları
Öğrenci: Efe Berke Ağlık (251478034)
Proje: mini-grades
"""

import subprocess
import os
import shutil
import pytest

# --- Yardımcı Fonksiyonlar ---
def run_cmd(args):
    """Komutu terminalde çalıştırır. Önce init yapar ki sistem hep hazır olsun."""
    # Her testin başında sistemi otomatik hazırla
    subprocess.run(["python", "solution.py", "init"], capture_output=True, text=True)
    
    result = subprocess.run(
        ["python", "solution.py"] + args,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def setup_function():
    """Her testten önce .minigrades klasörünü sıfırlar."""
    if os.path.exists(".minigrades"):
        shutil.rmtree(".minigrades")

# --- add testleri ---
def test_add_student_success():
    """Yeni bir öğrencinin benzersiz ID ile sisteme başarıyla eklenmesini test eder."""
    response = run_cmd(["add", "101", "Berke"])
    assert response == "Student added successfully."

def test_add_student_duplicate():
    """Zaten var olan bir ID ile öğrenci eklemeye çalışıldığında 'Duplicate ID' hatasını test eder."""
    run_cmd(["add", "101", "Berke"])
    response = run_cmd(["add", "101", "Efe"])
    assert response == "Error: Student with ID 101 already exists."

def test_add_student_non_numeric_id():
    """ID kısmına sayı yerine harf girildiğinde sistemin verdiği numerik değer hatasını test eder."""
    response = run_cmd(["add", "abc", "Berke"])
    assert response == "Invalid input: Please enter a numeric value."

# --- add-grade testleri ---
def test_add_grade_success():
    """Var olan bir öğrenciye geçerli notların başarıyla eklenmesini test eder."""
    run_cmd(["add", "101", "Berke"])
    response = run_cmd(["add-grade", "101", "80"])
    assert response == "Grades added successfully for student 101."

def test_add_grade_non_numeric_grade():
    """Eklenecek notun sayılardan oluşmasını test eder."""
    run_cmd(["add", "101", "Berke"])
    response = run_cmd(["add-grade", "101", "abc"])
    assert response == "Invalid input: Please enter a numeric value."

def test_add_grade_student_not_found():
    """Not eklenecek öğrenci ID'nin sistemde olmadığını test eder."""
    response = run_cmd(["add-grade", "999", "80"])
    assert response == "Error: No student found with ID 999."

# --- delete testleri ---
def test_delete_student_success():
    """Var olan bir öğrencinin ID üzerinden sistemden silinmesini test eder."""
    run_cmd(["add", "101", "Berke"])
    response = run_cmd(["delete", "101"])
    assert response == "Student and all grades deleted successfully."

def test_delete_student_not_found():
    """Sistemde olmayan bir ID silinmeye çalışıldığında hata mesajını test eder."""
    response = run_cmd(["delete", "999"])
    assert response == "Error: No student found with ID 999."

# --- calculate testleri ---
def test_calculate_average_success():
    """Kayıtlı bir öğrencinin ortalamasının (simülasyon mesajını) test eder."""
    run_cmd(["add", "101", "Berke"])
    response = run_cmd(["average", "101"])
    assert response == "Average calculation will be implemented in future weeks."

def test_calculate_average_student_not_found():
    """Sistemde kayıtlı olmayan bir öğrenci sorgulandığında verilecek hatayı test eder."""
    response = run_cmd(["average", "999"])
    assert response == "Error: No student found with ID 999."

# --- list testleri ---
def test_list_students_success():
    """Sistemde kayıtlı tüm öğrencilerin yeni formata (ID | Name) göre listelenmesini test eder."""
    run_cmd(["add", "101", "Berke"])
    run_cmd(["add", "102", "Efe"])
    response = run_cmd(["list"])
    assert "101 | Berke" in response
    assert "102 | Efe" in response

def test_list_students_empty():
    """Sistemde hiç öğrenci kayıtlı değilken listeleme yapıldığında verilecek hatayı test eder."""
    response = run_cmd(["list"])
    assert response == "Error: No students found in the system. Operation aborted."

# --- report testleri ---
def test_generate_report_success():
    """Sistemdeki verilerin başarıyla raporlanmasını test eder."""
    run_cmd(["add", "101", "Berke"])
    run_cmd(["add", "102", "Efe"])
    response = run_cmd(["report"])
    assert response == "Report saved to .minigrades/report.txt"
    assert os.path.exists(".minigrades/report.txt")

def test_generate_report_empty():
    """Sistemde hiç öğrenci kayıtlı değilken raporlama yapıldığında verilecek hatayı test eder."""
    response = run_cmd(["report"])
    assert response == "Error: No data available to generate a report."

# --- unknown-command testi ---
def test_unknown_command():
    """Bilinmeyen bir komut girildiğinde verilen hatayı test eder."""
    response = run_cmd(["hello"])
    assert "Unknown command: hello. Please select from the menu." in response