"""
Task service for handling business logic
"""
from internal.db.database import db
from internal.models.task import Task
from sqlalchemy import desc

class TaskService:
    """Service for task management operations"""
    
    @staticmethod
    def create_task(task_data):
        """
        Create a new task
        
        Args:
            task_data (dict): Task data
            
        Returns:
            Task: Created task
        """
        task = Task(**task_data)
        db.session.add(task)
        db.session.commit()
        return task
    
    @staticmethod
    def get_task_by_id(task_id):
        """
        Get task by ID
        
        Args:
            task_id (int): Task ID
            
        Returns:
            Task: Task if found, None otherwise
        """
        return Task.query.get(task_id)
    
    @staticmethod
    def list_tasks(page=1, per_page=20, status=None, priority=None):
        """
        List tasks with pagination and filters
        
        Args:
            page (int): Page number
            per_page (int): Items per page
            status (str, optional): Filter by status
            priority (str, optional): Filter by priority
            
        Returns:
            tuple: (tasks, total_pages, total_items)
        """
        query = Task.query
        
        # Apply filters if provided
        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        # Order by created date, newest first
        query = query.order_by(desc(Task.created_at))
        
        # Apply pagination
        pagination = query.paginate(page=page, per_page=per_page)
        
        return pagination.items, pagination.pages, pagination.total
    
    @staticmethod
    def update_task(task_id, task_data):
        """
        Update an existing task
        
        Args:
            task_id (int): Task ID
            task_data (dict): Updated task data
            
        Returns:
            Task: Updated task or None if not found
        """
        task = Task.query.get(task_id)
        
        if not task:
            return None
            
        for key, value in task_data.items():
            setattr(task, key, value)
            
        db.session.commit()
        return task
    
    @staticmethod
    def update_task_status(task_id, status):
        """
        Update task status
        
        Args:
            task_id (int): Task ID
            status (str): New status
            
        Returns:
            Task: Updated task or None if not found
        """
        task = Task.query.get(task_id)
        
        if not task:
            return None
            
        task.status = status
        db.session.commit()
        return task
    
    @staticmethod
    def delete_task(task_id):
        """
        Delete a task
        
        Args:
            task_id (int): Task ID
            
        Returns:
            bool: True if task was deleted, False otherwise
        """
        task = Task.query.get(task_id)
        
        if not task:
            return False
            
        db.session.delete(task)
        db.session.commit()
        return True
