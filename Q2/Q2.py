import sqlite3

class MarksManagementSystem:
    def __init__(self, db_name='marks_management.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
       
        # Initialize the database tables if they don't exist
        self.initialize_database()
       
    def initialize_database(self):
        """Initialize the database and tables if they don't exist."""
        # Create the students table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_no INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            math INTEGER DEFAULT 0,
            science INTEGER DEFAULT 0,
            english INTEGER DEFAULT 0,
            total INTEGER DEFAULT 0
        )
        ''')
       
        # Insert some initial dummy student data if the table is empty
        self.cursor.execute("SELECT COUNT(*) FROM students")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.executemany('''
            INSERT INTO students (roll_no, name) VALUES (?, ?)
            ''', [
                (1, 'Alice'),
                (2, 'Bob'),
                (3, 'Charlie')
            ])
            self.connection.commit()

    def update_marks(self, subject, roll_no, marks):
        """Update marks for a subject."""
        if subject not in ['math', 'science', 'english']:
            print("Invalid subject!")
            return
       
        query = f"UPDATE students SET {subject} = ? WHERE roll_no = ?"
        self.cursor.execute(query, (marks, roll_no))
       
        # Recalculate total marks
        self.cursor.execute('''
        UPDATE students
        SET total = math + science + english
        WHERE roll_no = ?
        ''', (roll_no,))
       
        self.connection.commit()

    def view_results(self):
        """View sorted results based on total marks."""
        self.cursor.execute('''
        SELECT roll_no, name, math, science, english, total
        FROM students
        ORDER BY total DESC
        ''')

        rows = self.cursor.fetchall()
        print("Roll No | Name    | Math | Science | English | Total")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]:7} | {row[1]:7} | {row[2]:4} | {row[3]:7} | {row[4]:7} | {row[5]:5}")
   
    def teacher_update(self):
        """Allow teachers to update marks."""
        print("\n--- Teacher Menu ---")
        subject = input("Enter subject (math/science/english): ").lower()
        roll_no = int(input("Enter student roll number: "))
        marks = int(input(f"Enter marks for {subject}: "))
       
        self.update_marks(subject, roll_no, marks)
        print(f"Marks for {subject} updated successfully.")

    def student_view(self):
        """Allow students to view their marks."""
        roll_no = int(input("Enter your roll number: "))
        self.cursor.execute('''
        SELECT name, math, science, english, total
        FROM students WHERE roll_no = ?
        ''', (roll_no,))
       
        row = self.cursor.fetchone()
        if row:
            print(f"\nStudent: {row[0]}")
            print(f"Math: {row[1]}")
            print(f"Science: {row[2]}")
            print(f"English: {row[3]}")
            print(f"Total: {row[4]}")
        else:
            print("Student not found!")

    def close_connection(self):
        """Close the connection to the database."""
        self.connection.close()


if __name__ == "__main__":
    system = MarksManagementSystem()

    # Teacher interaction
    while True:
        print("\n--- Teacher Menu ---")
        print("1. Update marks for a subject")
        print("2. View sorted student results")
        print("3. Exit")
        option = input("Select an option: ")
       
        if option == "1":
            system.teacher_update()
        elif option == "2":
            system.view_results()
        elif option == "3":
            break
        else:
            print("Invalid option. Try again.")
   
    # Student interaction
    while True:
        print("\n--- Student Menu ---")
        print("1. View my marks")
        print("2. Exit")
        option = input("Select an option: ")
       
        if option == "1":
            system.student_view()
        elif option == "2":
            break
        else:
            print("Invalid option. Try again.")

    # Close the database connection
    system.close_connection()
