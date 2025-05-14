
# 📡 Task API - `curl` Examples

Base URL: `https://task-api-bm4j.onrender.com/api/tasks`

---

## ✅ Create a Task  
Creates a new task with title, description, due date, and priority.

```bash
curl -X POST https://task-api-bm4j.onrender.com/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete Project",
    "description": "Finish the task management API",
    "due_date": "2025-05-20T00:00:00",
    "priority": "high"
  }'
```

---

## 📄 Get a Task by ID  
Fetches a specific task using its ID.

```bash
curl https://task-api-bm4j.onrender.com/api/tasks/2
```

---

## 📋 List All Tasks with Filters  
Retrieves a paginated list of tasks, optionally filtered by status and priority.

```bash
curl "https://task-api-bm4j.onrender.com/api/tasks?page=1&per_page=20&status=pending&priority=high"
```

---

## ✏️ Update a Task  
Updates a task's fields like title, description, or priority.

```bash
curl -X PUT https://task-api-bm4j.onrender.com/api/tasks/2 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "description": "Updated description",
    "priority": "medium"
  }'
```

---

## 🔄 Update Task Status  
Updates only the status of a task (`pending`, `in_progress`, `completed`, etc.).

```bash
curl -X PATCH https://task-api-bm4j.onrender.com/api/tasks/2/status \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

---

## ❌ Delete a Task  
Deletes a task by its ID.

```bash
curl -X DELETE https://task-api-bm4j.onrender.com/api/tasks/2
```

---
