"""
Tests for the task service
"""
import pytest
import os
from datetime import datetime, timedelta
from internal.app import create_app
from internal.db.database import db
from internal.models.task import Task, TaskStatus, TaskPriority
from internal.handlers.task_service import TaskService

@pytest.fixture
def app():
    """
    Flask app fixture for tests
    """
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """
    Test client fixture
    """
    return app.test_client()

def test_create_task(app):
    """Test creating a task"""
    with app.app_context():
        # Prepare task data
        tomorrow = datetime.utcnow() + timedelta(days=1)
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "priority": TaskPriority.HIGH.value,
            "due_date": tomorrow
        }
        
        # Create task
        task = TaskService.create_task(task_data)
        
        # Assertions
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "This is a test task"
        assert task.priority == TaskPriority.HIGH.value
        assert task.status == TaskStatus.PENDING.value
        assert task.due_date is not None

def test_get_task_by_id(app):
    """Test getting a task by ID"""
    with app.app_context():
        # Create a task first
        task = Task(title="Test Task")
        db.session.add(task)
        db.session.commit()
        
        # Get the task
        retrieved_task = TaskService.get_task_by_id(task.id)
        
        # Assertions
        assert retrieved_task is not None
        assert retrieved_task.id == task.id
        assert retrieved_task.title == "Test Task"

def test_list_tasks(app):
    """Test listing tasks with pagination and filters"""
    with app.app_context():
        # Create some tasks
        tasks = [
            Task(
                title=f"Task {i}", 
                status=TaskStatus.PENDING.value if i % 3 == 0 else 
                      TaskStatus.IN_PROGRESS.value if i % 3 == 1 else 
                      TaskStatus.COMPLETED.value,
                priority=TaskPriority.LOW.value if i % 3 == 0 else 
                        TaskPriority.MEDIUM.value if i % 3 == 1 else 
                        TaskPriority.HIGH.value
            ) for i in range(25)
        ]
        db.session.add_all(tasks)
        db.session.commit()
        
        # List all tasks (default pagination)
        all_tasks, total_pages, total_items = TaskService.list_tasks()
        assert len(all_tasks) == 20  # Default per_page is 20
        assert total_items == 25
        assert total_pages == 2
        
        # List tasks with custom pagination
        page_2_tasks, _, _ = TaskService.list_tasks(page=2, per_page=10)
        assert len(page_2_tasks) == 5  # 5 items on page 2
        
        # List tasks with status filter
        pending_tasks, _, _ = TaskService.list_tasks(status=TaskStatus.PENDING.value)
        assert all(task.status == TaskStatus.PENDING.value for task in pending_tasks)
        
        # List tasks with priority filter
        high_priority_tasks, _, _ = TaskService.list_tasks(priority=TaskPriority.HIGH.value)
        assert all(task.priority == TaskPriority.HIGH.value for task in high_priority_tasks)

def test_update_task(app):
    """Test updating a task"""
    with app.app_context():
        # Create a task first
        task = Task(title="Original Title", description="Original Description")
        db.session.add(task)
        db.session.commit()
        
        # Update the task
        updated_task = TaskService.update_task(task.id, {
            "title": "Updated Title",
            "description": "Updated Description"
        })
        
        # Assertions
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        
        # Verify the update persisted
        db.session.expire_all()
        persisted_task = Task.query.get(task.id)
        assert persisted_task.title == "Updated Title"

def test_update_task_status(app):
    """Test updating a task status"""
    with app.app_context():
        # Create a task first
        task = Task(title="Test Task", status=TaskStatus.PENDING.value)
        db.session.add(task)
        db.session.commit()
        
        # Update the task status
        updated_task = TaskService.update_task_status(task.id, TaskStatus.COMPLETED.value)
        
        # Assertions
        assert updated_task.status == TaskStatus.COMPLETED.value
        
        # Verify the update persisted
        db.session.expire_all()
        persisted_task = Task.query.get(task.id)
        assert persisted_task.status == TaskStatus.COMPLETED.value

def test_delete_task(app):
    """Test deleting a task"""
    with app.app_context():
        # Create a task first
        task = Task(title="Test Task")
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        
        # Delete the task
        success = TaskService.delete_task(task_id)
        
        # Assertions
        assert success is True
        
        # Verify the task was deleted
        deleted_task = Task.query.get(task_id)
        assert deleted_task is None
