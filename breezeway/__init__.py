from .breezeway_client import BreezewayClient, AsyncBreezewayClient
from .models.company import Department
from models.reservation import Reservation, ReservationType
from .models.task import Task, TaskStatus
from .models.unit import Unit, UnitNotes
from .models.user import User, UserRole

__all__ = [
    # Clients
    'BreezewayClient', 'AsyncBreezewayClient',

    # Company
    'Department',

    # People
    'User',
    'UserRole',

    # Reservation
    'Reservation',
    'ReservationType',

    # Property
    'Unit',
    'UnitNotes',

    # Task
    'Task',
    'TaskStatus'
]

# Package metadata
__author__ = 'Anthony DeGarimore'
__email__ = 'Anthony@DeGarimore.com'
__licence__ = 'MIT'