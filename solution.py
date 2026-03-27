"""
mini-grades v0 - basitleştirilmiş implementasyon
Öğrenci: Efe Berke Ağlık (251478034)

Kapsam: Sadece fonksiyon yapısı ve temel mantık.
Sınırlamalar: Döngü ve liste henüz kullanılmadı, veriler kalıcı olarak saklanmıyor.
"""

import sys
import os

# --- FONKSİYON TANIMLARI ---

def initialize():
    """Sistemin çalışması için .minigrades dizini ve veri dosyasını oluşturur."""
    if os.path.exists(".minigrades"):
        return "Already initialized"
    os.mkdir(".minigrades")
    f = open(".minigrades/data.txt", "w")
    f.close()
    return "Initialized empty system in .minigrades/"

def add_student(id, name):
    """Sisteme öğrenci eklemeyi sağlar."""
    if not id.isdigit():
        return "Invalid input: Please enter a numeric value."
    
    if not os.path.exists(".minigrades/data.txt"):
        return "Not initialized. Run: python solution.py init"
    
    f_check = open(".minigrades/data.txt", "r")
    content = f_check.read()
    f_check.close()
    
    # ID'yi ayıraçla ( |) aratıyoruz ki 101 içindeki 1'i yanlışlıkla bulmasın.
    if id + " |" in content:
        return f"Error: Student with ID {id} already exists."
    
    f = open(".minigrades/data.txt", "a")
    # Veriyi boşluklu formatta (ID | Name) kaydediyoruz.
    f.write(id + " | " + name + "\n")
    f.close()

    return "Student added successfully."

def add_grade(id, grade):
    """Öğrenciye not eklemeyi sağlar."""
    if not id.isdigit():
        return "Invalid input: Please enter a numeric value."
    
    if not os.path.exists(".minigrades/data.txt"):
        return "Not initialized. Run: python solution.py init"

    # data.txt verilerini content değişkenine çekiyoruz
    f_check = open(".minigrades/data.txt", "r")
    content = f_check.read()
    f_check.close()

    # content içerisinde aradığımız öğrenci var mı onu kontrol ediyoruz
    if not id + " |" in content:
        return f"Error: No student found with ID {id}."
    
    if not grade.isdigit():
        return "Invalid input: Please enter a numeric value."
        
    if int(grade) < 0 or int(grade) > 100:
        return "Invalid grade: Grades must be between 0 and 100."
    else:
        return f"Grades added successfully for student {id}."

def delete_student(id):
    """Sistemden öğrenci silmeyi sağlar."""
    if not os.path.exists(".minigrades/data.txt"):
        return "Not initialized. Run: python solution.py init"
    
    if not id.isdigit():
        return "Invalid input: Please enter a numeric value."

    f_check = open(".minigrades/data.txt", "r")
    content = f_check.read()
    f_check.close()

    # content içerisinde aradığımız öğrenci var mı onu kontrol ediyoruz
    if not id + " |" in content:
        return f"Error: No student found with ID {id}."
    
    return "Student and all grades deleted successfully."

def list_students():
    """Sistemdeki öğrencileri listeler."""
    if not os.path.exists(".minigrades/data.txt"):
        return "Error: No students found in the system. Operation aborted."
    
    f = open(".minigrades/data.txt", "r")
    content = f.read()
    f.close()

    # contentin boş olup olmadığını kontrol ediyoruz (eğer boşsa veri yoktur)
    if content == "":
        return "Error: No students found in the system. Operation aborted."
    
    return content

def calculate_average(id):
    """Öğrencinin ortalamasını hesaplar (v0 Simülasyonu)."""
    if not os.path.exists(".minigrades/data.txt"):
        return "Not initialized. Run: python solution.py init"
    
    f_check = open(".minigrades/data.txt", "r")
    content = f_check.read()
    f_check.close()

    # content içerisinde aradığımız öğrenci var mı onu kontrol ediyoruz
    if not id + " |" in content:
        return f"Error: No student found with ID {id}."
    
    return "Average calculation will be implemented in future weeks."

def generate_report():
    """Sistemdeki verilerden rapor oluşturur."""
    if not os.path.exists(".minigrades/data.txt"):
        return "Error: No data available to generate a report."
    
    f = open(".minigrades/data.txt", "r")
    current_data = f.read()
    f.close()

    if current_data == "":
        return "Error: No data available to generate a report."
    
    r = open(".minigrades/report.txt", "w")
    r.write("ID | NAME\n-----------\n")
    r.write(current_data)
    r.close()

    return "Report saved to .minigrades/report.txt"

# --- ANA PROGRAM ---

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

elif sys.argv[1] == "report":
    print(generate_report())

elif sys.argv[1] == "average":
    if len(sys.argv) < 3:
        print("Usage: python solution.py average <id>")
    else:
        print(calculate_average(sys.argv[2]))

else:
    print("Unknown command: " + sys.argv[1] + ". Please select from the menu.")