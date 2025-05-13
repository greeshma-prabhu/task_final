"""
Tests for the API endpoints
"""
import pytest
import json
from datetime import datetime, timedelta
from internal.app import create_app
from internal.db.database import db
from internal.models.task import Task, TaskStatus, TaskPriority

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

def test_create_task_endpoint(app, client):
    """Test creating a task via API"""
    # Prepare task data
    tomorrow = datetime.utcnow() + timedelta(days=1)
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": TaskPriority.HIGH.value,
        "due_date": tomorrow.isoformat()
    }
    
    # Make API request
    response = client.post(
        '/api/tasks',
        data=json.dumps(task_data),
        content_type='application/json'
    )
    
    # Assertions
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert response_data["title"] == "Test Task"
    assert response_data["description"] == "This is a test task"
    assert response_data["priority"] == TaskPriority.HIGH.value
    assert response_data["status"] == TaskStatus.PENDING.value
    
    # Verify in database
    with app.app_context():
        task = Task.query.get(response_data["id"])
        assert task is not None
        assert task.title == "Test Task"

def test_get_task_endpoint(app, client):
    """Test getting a task by ID via API"""
    # Create a task first
    with app.app_context():
        task = Task(title="Get Task Test")
        db.session.add(task)
        db.session.commit()
        task_id = task.id
    
    # Make API request
    response = client.get(f'/api/tasks/{task_id}')
    
    # Assertions
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["id"] == task_id
    assert response_data["title"] == "Get Task Test"

def test_get_task_not_found(client):
    """Test getting a non-existent task"""
    # Make API request with invalid ID
    response = client.get('/api/tasks/9999')
    
    # Assertions
    assert response.status_code == 404

def test_list_tasks_endpoint(app, client):
    """Test listing tasks via API"""
    # Create some tasks
    with app.app_context():
        tasks = [
            Task(
                title=f"API Task {i}", 
                status=TaskStatus.PENDING.value if i % 3 == 0 else 
                      TaskStatus.IN_PROGRESS.value if i % 3 == 1 else 
                      TaskStatus.COMPLETED.value
            ) for i in range(10)
        ]
        db.session.add_all(tasks)
        db.session.commit()
    
    # Make API request
    response = client.get('/api/tasks')
    
    # Assertions
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert "tasks" in response_data
    assert "pagination" in response_data
    assert len(response_data["tasks"]) == 10
    
    # Test with pagination
    response = client.get('/api/tasks?page=1&per_page=5')
    response_data = json.loads(response.data)
    assert len(response_data["tasks"]) == 5
    
    # Test with filters
    response = client.get(f'/api/tasks?status={TaskStatus.PENDING.value}')
    response_data = json.loads(response.data)
    assert all(task["status"] == TaskStatus.PENDING.value for task in response_data["tasks"])

def test_update_task_endpoint(app, client):
    """Test updating a task via API"""
    # Create a task first
    with app.app_context():
        task = Task(title="Original Title", description="Original Description")
        db.session.add(task)
        db.session.commit()
        task_id = task.id
    
    # Prepare update data
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description"
    }
    
    # Make API request
    response = client.put(
        f'/api/tasks/{task_id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Assertions
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["title"] == "Updated Title"
    assert response_data["description"] == "Updated Description"
    
    # Verify in database
    with app.app_context():
        updated_task = Task.query.get(task_id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"

def test_update_task_status_endpoint(app, client):
    """Test updating a task status via API"""
    # Create a task first
    with app.app_context():
        task = Task(title="Status Test", status=TaskStatus.PENDING.value)
        db.session.add(task)
        db.session.commit()
        task_id = task.id
    
    # Prepare status update data
    status_data = {
        "status": TaskStatus.COMPLETED.value
    }
    
    # Make API request
    response = client.patch(
        f'/api/tasks/{task_id}/status',
        data=json.dumps(status_data),
        content_type='application/json'
    )
    
    # Assertions
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["status"] == TaskStatus.COMPLETED.value
    
    # Verify in database
    with app.app_context():
        updated_task = Task.query.get(task_id)
        assert updated_task.status == TaskStatus.COMPLETED.value

def test_delete_task_endpoint(app, client):
    """Test deleting a task via API"""
    # Create a task first
    with app.app_context():
        task = Task(title="Delete Test")
        db.session.add(task)
        db.session.commit()
        task_id = task.id
    
    # Make API request
    response = client.delete(f'/api/tasks/{task_id}')
    
    # Assertions
    assert response.status_code == 200
    
    # Verify in database
    with app.app_context():
        deleted_task = Task.query.get(task_id)
        assert deleted_task is None

def test_validation_errors(client):
    """Test validation errors in API endpoints"""
    # Test missing required field
    response = client.post(
        '/api/tasks',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400
    
    # Test invalid priority
    response = client.post(
        '/api/tasks',
        data=json.dumps({
            "title": "Test Task",
            "priority": "invalid"
        }),
        content_type='application/json'
    )
    assert response.status_code == 400
    
    # Test past due date
    yesterday = datetime.utcnow() - timedelta(days=1)
    response = client.post(
        '/api/tasks',
        data=json.dumps({
            "title": "Test Task",
            "due_date": yesterday.isoformat()
        }),
        content_type='application/json'
    )
    assert response.status_code == 400
