# Task Management Service

A RESTful API service for managing tasks with CRUD operations, filtering, and pagination.

## Tech Stack

- Python 3.8+
- Flask web framework
- SQLAlchemy ORM
- SQLite/PostgreSQL/MySQL database
- Pytest for testing

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd task-service
```

### 2. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root with the following content:

```
FLASK_ENV=development
FLASK_APP=cmd.main:app
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///tasks.db
```

For PostgreSQL, use:
```
DATABASE_URL=postgresql://username:password@localhost:5432/taskdb
```

### 5. Initialize the database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the application

```bash
flask run
```

Or directly:

```bash
python -m cmd.main
```

The API will be available at http://127.0.0.1:5000/

### 7. Run tests

```bash
pytest
```

## API Endpoints

### Create a Task

**Endpoint:** `POST /api/tasks`

**Request Body:**
```json
{
  "title": "Complete Project",
  "description": "Finish the task management API",
  "due_date": "2025-05-20T00:00:00",
  "priority": "high"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete Project",
  "description": "Finish the task management API",
  "due_date": "2025-05-20T00:00:00",
  "priority": "high",
  "status": "pending",
  "created_at": "2025-05-13T10:30:00",
  "updated_at": "2025-05-13T10:30:00"
}
```

### Get Task by ID

**Endpoint:** `GET /api/tasks/{task_id}`

**Response:**
```json
{
  "id": 1,
  "title": "Complete Project",
  "description": "Finish the task management API",
  "due_date": "2025-05-20T00:00:00",
  "priority": "high",
  "status": "pending",
  "created_at": "2025-05-13T10:30:00",
  "updated_at": "2025-05-13T10:30:00"
}
```

### List Tasks

**Endpoint:** `GET /api/tasks?page=1&per_page=20&status=pending&priority=high`

**Query Parameters:**
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20, max: 100)
- `status` - Filter by status (optional)
- `priority` - Filter by priority (optional)

**Response:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete Project",
      "description": "Finish the task management API",
      "due_date": "2025-05-20T00:00:00",
      "priority": "high",
      "status": "pending",
      "created_at": "2025-05-13T10:30:00",
      "updated_at": "2025-05-13T10:30:00"
    },
    {
      "id": 2,
      "title": "Another Task",
      "description": "This is another task",
      "due_date": null,
      "priority": "medium",
      "status": "pending",
      "created_at": "2025-05-13T10:35:00",
      "updated_at": "2025-05-13T10:35:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_pages": 1,
    "total_items": 2
  }
}
```

### Update Task

**Endpoint:** `PUT /api/tasks/{task_id}`

**Request Body:**
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "priority": "medium"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Title",
  "description": "Updated description",
  "due_date": "2025-05-20T00:00:00",
  "priority": "medium",
  "status": "pending",
  "created_at": "2025-05-13T10:30:00",
  "updated_at": "2025-05-13T11:15:00"
}
```

### Update Task Status

**Endpoint:** `PATCH /api/tasks/{task_id}/status`

**Request Body:**
```json
{
  "status": "completed"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Title",
  "description": "Updated description",
  "due_date": "2025-05-20T00:00:00",
  "priority": "medium",
  "status": "completed",
  "created_at": "2025-05-13T10:30:00",
  "updated_at": "2025-05-13T11:20:00"
}
```

### Delete Task

**Endpoint:** `DELETE /api/tasks/{task_id}`

**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:
- `400 Bad Request` - Invalid input data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error responses include a message and, for validation errors, detailed information about what went wrong.



Clone the repository
Create and activate a Python virtual environment: python -m venv venv && source venv/bin/activate
Install dependencies: pip install -r requirements.txt
Initialize the database:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Start the application: flask run
The API will be accessible at http://localhost:5000/api/tasks