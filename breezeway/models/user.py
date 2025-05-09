from dataclasses import dataclass
from enum import Enum

from .base import BaseBreezewayModel
from .company import Department
from .unit import UnitGroup

class UserRole(Enum):
    ADMIN = 'administrator'
    OFFICE = 'office'
    REPRESENTATIVE = 'representative'
    SERVICE_PARTNER = 'service_partner'
    SUPERVISOR = 'supervisor'

    @property
    def name(self) -> str:
        return {
            UserRole.ADMIN: "Administrator",
            UserRole.OFFICE: "Office",
            UserRole.REPRESENTATIVE: "Representative",
            UserRole.SERVICE_PARTNER: "Service Partner",
            UserRole.SUPERVISOR: "Supervisor",
        }[self]

class UserStatus(Enum):
    ACTIVE = 'active'
    INVITED = 'invited'
    INACTIVE = 'inactive'

    @property
    def name(self) -> str:
        return {
            UserStatus.ACTIVE: "Active",
            UserStatus.INVITED: "Invited",
            UserStatus.INACTIVE: "Inactive",
        }[self]


@dataclass
class User(BaseBreezewayModel):
    id: int
    first_name: str
    last_name: str
    accept_decline_tasks: bool
    active: bool
    emails: list[str]
    employee_code: str
    groups: list[UnitGroup]
    shifts: dict
    type_departments: list[Department]
    type_role: UserRole

    @staticmethod
    def preprocess_data(json_data: dict) -> None:
        json_data['type_departments'] = [Department(department) for department in json_data['type_departments']]
        json_data['groups'] = [UnitGroup.from_json(group) for group in json_data['groups']]
        json_data['type_role'] = UserRole(json_data['type_role'])