"""
Schemas for request validation and serialization
"""
from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime
from internal.models.task import TaskStatus, TaskPriority

class TaskCreateSchema(Schema):
    """Schema for task creation validation"""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(required=False, allow_none=True)
    due_date = fields.DateTime(required=False, allow_none=True)
    priority = fields.Str(
        required=False,
        validate=validate.OneOf([p.value for p in TaskPriority]),
        default=TaskPriority.MEDIUM.value
    )
    
    @validates('due_date')
    def validate_due_date(self, value):
        """Validate due date is in the future"""
        if value and value < datetime.utcnow():
            raise ValidationError("Due date cannot be in the past")

class TaskUpdateSchema(Schema):
    """Schema for task update validation"""
    title = fields.Str(required=False, validate=validate.Length(min=1, max=255))
    description = fields.Str(required=False, allow_none=True)
    due_date = fields.DateTime(required=False, allow_none=True)
    priority = fields.Str(
        required=False,
        validate=validate.OneOf([p.value for p in TaskPriority])
    )
    status = fields.Str(
        required=False,
        validate=validate.OneOf([s.value for s in TaskStatus])
    )
    
    @validates('due_date')
    def validate_due_date(self, value):
        """Validate due date is in the future"""
        if value and value < datetime.utcnow():
            raise ValidationError("Due date cannot be in the past")

class TaskStatusUpdateSchema(Schema):
    """Schema for task status update validation"""
    status = fields.Str(
        required=True,
        validate=validate.OneOf([s.value for s in TaskStatus])
    )
