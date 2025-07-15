Here is the Python code for the todo list item models:

from pydantic import BaseModel
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TodoItem(BaseModel):
    id: int
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM