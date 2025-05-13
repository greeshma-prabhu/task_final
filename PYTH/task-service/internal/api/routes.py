"""
API routes for task management
"""
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError

from internal.handlers.task_service import TaskService
from internal.models.schemas import TaskCreateSchema, TaskUpdateSchema, TaskStatusUpdateSchema

# Initialize blueprints
tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

def register_routes(app):
    """
    Register API routes with the Flask application
    
    Args:
        app: Flask application instance
    """
    app.register_blueprint(tasks_bp)

# Schema instances
task_create_schema = TaskCreateSchema()
task_update_schema = TaskUpdateSchema()
task_status_schema = TaskStatusUpdateSchema()

@tasks_bp.route('', methods=['POST'])
def create_task():
    """
    Create a new task
    """
    try:
        # Validate input data
        data = request.get_json()
        validated_data = task_create_schema.load(data)
        
        # Create task
        task = TaskService.create_task(validated_data)
        
        return jsonify(task.to_dict()), 201
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Error creating task: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Get task by ID
    """
    try:
        task = TaskService.get_task_by_id(task_id)
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
            
        return jsonify(task.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Error retrieving task: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@tasks_bp.route('', methods=['GET'])
def list_tasks():
    """
    List tasks with pagination and filters
    """
    try:
        # Parse query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        # Validate page and per_page
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
            
        # Get tasks
        tasks, total_pages, total_items = TaskService.list_tasks(
            page=page,
            per_page=per_page,
            status=status,
            priority=priority
        )
        
        # Format response
        response = {
            "tasks": [task.to_dict() for task in tasks],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
                "total_items": total_items
            }
        }
        
        return jsonify(response), 200
    except Exception as e:
        current_app.logger.error(f"Error listing tasks: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update an existing task
    """
    try:
        # Validate input data
        data = request.get_json()
        validated_data = task_update_schema.load(data)
        
        # Update task
        task = TaskService.update_task(task_id, validated_data)
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
            
        return jsonify(task.to_dict()), 200
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Error updating task: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@tasks_bp.route('/<int:task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    """
    Update task status
    """
    try:
        # Validate input data
        data = request.get_json()
        validated_data = task_status_schema.load(data)
        
        # Update task status
        task = TaskService.update_task_status(task_id, validated_data['status'])
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
            
        return jsonify(task.to_dict()), 200
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Error updating task status: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task
    """
    try:
        success = TaskService.delete_task(task_id)
        
        if not success:
            return jsonify({"error": "Task not found"}), 404
            
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting task: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
