# Task Management Backend Service

A backend service to manage tasks, built with Python and PostgreSQL. The service supports creating, retrieving, updating, and listing tasks.

---

## :star: Features

- **Create Task**: Create new tasks with title, description, due date, and priority.
- **Get Task by ID**: Retrieve a task by its unique ID.
- **List Tasks**: List tasks with pagination, and filter them by status or priority.
- **Update Task Status**: Change the status of a task (e.g., Pending, In Progress, Completed).

---

## :wrench: Tech Stack

- **Backend**: Python (Flask)
- **Database**: PostgreSQL
- **Testing**: pytest

---
## :memo: Setup Instructions

### 1. Clone the Repository

> **Step 1**: Clone the repository to your local machine.


git clone https://github.com/greeshma-prabhu/task_final.git
cd task_final

> 2. Install Dependencies
**Step 2**: Install the required Python packages.



pip install -r requirements.txt

### 3. Set Up Database

> **Step 3**: Set up your PostgreSQL database (locally or on a cloud service). Configure the connection using environment variables:


export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=task_db
export DB_USER=your_db_user
export DB_PASSWORD=your_db_password

### 4. Run the Application

> **Step 4**: Start the Flask application.


python app.py

### 5. Running Tests

> **Step 5**: Run the unit tests using `pytest`.


pytest

## :computer: API Endpoints

| Method | Endpoint                      | Description                     |
|--------|-------------------------------|---------------------------------|
| POST   | `/api/tasks`                 | Create a new task               |
| GET    | `/api/tasks/{id}`            | Retrieve a task by ID           |
| GET    | `/api/tasks`                 | List all tasks (with filters)   |
| PUT    | `/api/tasks/{id}/status`     | Update the status of a task     |

## :pencil2: Example cURL Requests

### ▶️ Create a Task

curl -X POST http://localhost:5000/api/tasks \
-H "Content-Type: application/json" \
-d '{"title":"New Task","description":"This is a sample task","due_date":"2025-05-20","priority":"High"}'

>🔍 Get Task by ID
bash
Copy
Edit
curl http://localhost:5000/api/tasks/1
