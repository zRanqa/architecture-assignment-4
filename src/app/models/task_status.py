from enum import Enum

class TaskStatus(Enum):
    COMPLETED = "completed"
    IN_PROGRESS = "in progress"
    TO_BE_STARTED = "to be started"
    UNASSIGNED = "unassigned"