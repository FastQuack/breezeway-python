from .breezeway_client import BreezewayClient, AsyncBreezewayClient
from .models.company import Department
from .models.unit import Unit, UnitGroup, UnitNotes
from .models.user import UserRole, UserStatus

__all__ = [
    # Clients
    'BreezewayClient', 'AsyncBreezewayClient',

    # Company
    'Department',

    # People
    'UserStatus',

    # Property
    'Unit', 'UnitGroup', 'UnitNotes'
]

# Package metadata
__author__ = 'Anthony DeGarimore'
__email__ = 'Anthony@DeGarimore.com'
__licence__ = 'MIT'
