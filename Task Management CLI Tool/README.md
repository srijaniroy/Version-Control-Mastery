# Task Manager

A simple task management system built using Python and SQLite for storing tasks and their histories. This application allows users to add, edit, complete, view, and remove tasks. It also provides features to track task history and view pending/completed tasks separately.

## Features

- **Add Tasks**: Add new tasks with a description.
- **Edit Tasks**: Edit the description of existing tasks.
- **Remove Tasks**: Remove tasks from the system.
- **Complete Tasks**: Mark tasks as completed.
- **View Tasks**: View all tasks (pending and completed).
- **Pending Tasks**: View tasks that are pending.
- **Completed Tasks**: View tasks that are completed.
- **Task History**: View the history of actions performed on tasks.
- **Task Persistence**: Tasks are stored in an SQLite database, ensuring persistence across sessions.

## Installation

### Prerequisites

- Python 3.x
- SQLite (usually bundled with Python)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/srijaniroy/Version-Control-Mastery.git
   cd cd '.\Task Management CLI Tool\'
   ```

2. Install the required dependencies:
   This project only relies on built-in libraries (`sqlite3`, `time`), you can install any additional dependencies if needed.

3. Run the application:
   ```bash
   python task_manager.py
   ```

   This will start the task manager in the command line interface.

## Database Structure

The application uses SQLite with the following tables:

- **tasks**: Stores all tasks, including their description, status (pending/completed), and timestamps.
- **pending_tasks**: Stores the tasks that are currently pending.
- **completed_tasks**: Stores the tasks that are marked as completed.
- **task_history**: Stores a history of all actions performed on tasks (add, edit, complete, etc.).

## Assigned to

[Srijani Roy](https://github.com/srijaniroy)

