import sqlite3
import time

class Task:
    def __init__(self, task_id, description):
        self.id = task_id
        self.description = description
        self.is_completed = False
        self.timestamp = time.ctime()

    def display_task(self):
        status = "Completed" if self.is_completed else "Pending"
        print(f"Task ID: {self.id}\nDescription: {self.description}\nStatus: {status}\nCreated/Updated at: {self.timestamp}")

    def log_task_history(self, action):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO task_history (action, task_id, description, status, timestamp) VALUES (?, ?, ?, ?, ?)",
                       (action, self.id, self.description, "Completed" if self.is_completed else "Pending", self.timestamp))
        conn.commit()
        conn.close()

    def log_pending_task(self):
        if not self.is_completed:
            conn = sqlite3.connect('task_manager.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pending_tasks (task_id, description, timestamp) VALUES (?, ?, ?)",
                           (self.id, self.description, self.timestamp))
            conn.commit()
            conn.close()

    def log_completed_task(self):
        if self.is_completed:
            conn = sqlite3.connect('task_manager.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO completed_tasks (task_id, description, timestamp) VALUES (?, ?, ?)",
                           (self.id, self.description, self.timestamp))
            conn.commit()
            conn.close()

    @staticmethod
    def update_pending_tasks_file():
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pending_tasks")
        cursor.execute("INSERT INTO pending_tasks (task_id, description, timestamp) SELECT id, description, timestamp FROM tasks WHERE is_completed = 0")
        conn.commit()
        conn.close()

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.initialize_database()
        self.task_id_counter = 1

    def initialize_database(self):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            description TEXT,
                            is_completed INTEGER,
                            timestamp TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS pending_tasks (
                            task_id INTEGER,
                            description TEXT,
                            timestamp TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS completed_tasks (
                            task_id INTEGER,
                            description TEXT,
                            timestamp TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS task_history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            action TEXT,
                            task_id INTEGER,
                            description TEXT,
                            status TEXT,
                            timestamp TEXT)''')
        conn.commit()
        conn.close()

    def add_task(self, description):
        if not description:
            print("Error: Task description cannot be empty. Please try again.")
            return
        task = Task(self.task_id_counter, description)
        self.tasks.append(task)
        self.task_id_counter += 1
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (description, is_completed, timestamp) VALUES (?, ?, ?)",
               (task.description, task.is_completed, task.timestamp))
        task_id = cursor.lastrowid  
        task.id = task_id
        conn.commit()
        conn.close()
        task.log_task_history("Added")
        task.log_pending_task()
        print(f"Task added successfully! Task ID: {task.id}")

    def edit_task(self, task_id, new_description):
        if not new_description:
            print("Error: New description cannot be empty.")
            return    
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            conn.close()
            return
        updated_timestamp = time.ctime()
        cursor.execute("UPDATE tasks SET description = ?, timestamp = ? WHERE id = ?",
                    (new_description, updated_timestamp, task_id))
        conn.commit()
        cursor.execute("INSERT INTO task_history (action, task_id, description, status, timestamp) VALUES (?, ?, ?, ?, ?)",
                    ("Edited", task_id, new_description, "Pending" if task[2] == 0 else "Completed", updated_timestamp))
        conn.commit()
        conn.close()
        Task.update_pending_tasks_file() 
        print("Task edited successfully!")

    def complete_task(self, task_id):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            conn.close()
            return
        if task[2] == 1:  
            print(f"Error: Task {task_id} is already marked as completed.")
            conn.close()
            return
        updated_timestamp = time.ctime()
        cursor.execute("UPDATE tasks SET is_completed = ?, timestamp = ? WHERE id = ?",
                    (1, updated_timestamp, task_id))
        conn.commit()
        cursor.execute("INSERT INTO task_history (action, task_id, description, status, timestamp) VALUES (?, ?, ?, ?, ?)",
                    ("Completed", task_id, task[1], "Completed", updated_timestamp))
        cursor.execute("INSERT INTO completed_tasks (task_id, description, timestamp) VALUES (?, ?, ?)",
                    (task_id, task[1], updated_timestamp))
        cursor.execute("DELETE FROM pending_tasks WHERE task_id = ?", (task_id,))
        conn.commit()
        conn.close()
        print(f"Task {task_id} marked as completed successfully!")

    def remove_task(self, task_id):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()        
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            conn.close()
            return
        
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        cursor.execute("DELETE FROM pending_tasks WHERE task_id = ?", (task_id,))
        cursor.execute("DELETE FROM completed_tasks WHERE task_id = ?", (task_id,))
        cursor.execute("DELETE FROM task_history WHERE task_id = ?", (task_id,))
        conn.commit()
        conn.close()
        print(f"Task {task_id} removed successfully!")

    def view_tasks(self):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        conn.close()
        if not tasks:
            print("No tasks available.")
        else:
            for task in tasks:
                print(f"Task ID: {task[0]}\nDescription: {task[1]}\nStatus: {'Completed' if task[2] else 'Pending'}\nCreated/Updated at: {task[3]}")
                print("--------------------------------")

    def view_pending_tasks(self):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pending_tasks")
        tasks = cursor.fetchall()
        conn.close()
        if not tasks:
            print("No pending tasks available.")
        else:
            for task in tasks:
                print(f"Task ID: {task[0]}\nDescription: {task[1]}\nCreated/Updated at: {task[2]}")
                print("--------------------------------")

    def view_completed_tasks(self):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM completed_tasks")
        tasks = cursor.fetchall()
        conn.close()
        if not tasks:
            print("No completed tasks available.")
        else:
            for task in tasks:
                print(f"Task ID: {task[0]}\nDescription: {task[1]}\nCompleted at: {task[2]}")
                print("--------------------------------")

    def view_task_history(self):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM task_history")
        history = cursor.fetchall()
        conn.close()
        if not history:
            print("No task history available.")
        else:
            for entry in history:
                print(f"Action: {entry[1]}\nTask ID: {entry[2]}\nDescription: {entry[3]}\nStatus: {entry[4]}\nTimestamp: {entry[5]}")
                print("--------------------------------")

    def display_menu(self):
        print("Task Manager")
        print("1. Add a task")
        print("2. Edit a task")
        print("3. Complete a task")
        print("4. View all tasks")
        print("5. View pending tasks")
        print("6. View completed tasks")
        print("7. View task history")
        print("8. Remove a task")
        print("9. Exit")

    def execute_choice(self, choice):
        if choice == 1:
            description = input("Enter task description: ")
            self.add_task(description)
        elif choice == 2:
            task_id = int(input("Enter task ID to edit: "))
            new_description = input("Enter new description: ")
            self.edit_task(task_id, new_description)
        elif choice == 3:
            task_id = int(input("Enter task ID to complete: "))
            self.complete_task(task_id)
        elif choice == 4:
            self.view_tasks()
        elif choice == 5:
            self.view_pending_tasks()
        elif choice == 6:
            self.view_completed_tasks()
        elif choice == 7:
            self.view_task_history()
        elif choice == 8:
            task_id = int(input("Enter task ID to remove: "))
            self.remove_task(task_id)
        elif choice == 9:
            print("Exiting task manager...")
        else:
            print("Invalid choice! Please try again.")

def main():
    manager = TaskManager()
    choice = 0
    while choice != 9:
        manager.display_menu()
        choice = int(input("Enter your choice: "))
        manager.execute_choice(choice)

if __name__ == "__main__":
    main()