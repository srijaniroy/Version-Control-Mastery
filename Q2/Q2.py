import sqlite3

def initialize_database():
    conn = sqlite3.connect('marks.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_number INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            student_id INTEGER,
            subject_id INTEGER,
            marks INTEGER,
            PRIMARY KEY (student_id, subject_id),
            FOREIGN KEY (student_id) REFERENCES students (roll_number),
            FOREIGN KEY (subject_id) REFERENCES subjects (id)
        )
    """)
    
    conn.commit()
    conn.close()

def add_student():
    conn = sqlite3.connect('marks.db')
    cursor = conn.cursor()
    
    roll_number = input("Enter Roll Number: ")
    name = input("Enter Student Name: ")
    
    cursor.execute("INSERT INTO students (roll_number, name) VALUES (?, ?)", (roll_number, name))
    conn.commit()
    
    print(f"Student {name} added successfully!")
    conn.close()

def add_subject():
    conn = sqlite3.connect('marks.db')
    cursor = conn.cursor()
    
    subject_name = input("Enter Subject Name: ")
    cursor.execute("INSERT INTO subjects (name) VALUES (?)", (subject_name,))
    conn.commit()
    
    print(f"Subject {subject_name} added successfully!")
    conn.close()

def add_or_update_marks():
    conn = sqlite3.connect('marks.db')
    cursor = conn.cursor()
    
    roll = input("Enter Student Roll Number: ")
    subject_input = input("Enter Subject Name or ID: ")
    
    # Check if the input is numeric or a subject name
    if subject_input.isnumeric():
        cursor.execute("SELECT id FROM subjects WHERE id = ?", (subject_input,))
    else:
        cursor.execute("SELECT id FROM subjects WHERE name = ?", (subject_input,))
    
    subject_row = cursor.fetchone()
    if not subject_row:
        print("Subject not found!")
        return
    subject_id = subject_row[0]
    
    marks = input("Enter Marks: ")
    cursor.execute("""
        INSERT INTO marks (student_id, subject_id, marks)
        VALUES (?, ?, ?)
        ON CONFLICT(student_id, subject_id) DO UPDATE SET marks = excluded.marks
    """, (roll, subject_id, marks))
    conn.commit()
    print("Marks added/updated successfully!")
    
    conn.close()

def display_marks():
    conn = sqlite3.connect('marks.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.roll_number, s.name, sub.name as subject, m.marks
        FROM students s
        JOIN marks m ON s.roll_number = m.student_id
        JOIN subjects sub ON m.subject_id = sub.id
        ORDER BY s.roll_number
    """)
    rows = cursor.fetchall()
    
    student_data = {}
    for row in rows:
        roll_number, name, subject, marks = row
        if roll_number not in student_data:
            student_data[roll_number] = {'name': name, 'subjects': [], 'total_marks': 0}
        student_data[roll_number]['subjects'].append((subject, marks))
        student_data[roll_number]['total_marks'] += marks
    
    print("\nStudent Marks Sorted by Total Marks:")
    sorted_students = sorted(student_data.items(), key=lambda x: x[1]['total_marks'], reverse=True)
    
    for roll_number, data in sorted_students:
        print(f"\nRoll No: {roll_number} | Name: {data['name']}")
        for subject, marks in data['subjects']:
            print(f"  {subject}: {marks}")
        print(f"Total Marks: {data['total_marks']}")
    
    conn.close()

def main():
    initialize_database()
    while True:
        print("\nMarks Management System:")
        print("1. Add Student")
        print("2. Add Subject")
        print("3. Add or Update Marks")
        print("4. Display Marks")
        print("5. Exit")
        
        choice = input("Enter choice: ")
        if choice == '1':
            add_student()
        elif choice == '2':
            add_subject()
        elif choice == '3':
            add_or_update_marks()
        elif choice == '4':
            display_marks()
        elif choice == '5':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

