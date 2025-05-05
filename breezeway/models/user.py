from dataclasses import dataclass
from enum import Enum

from breezeway.models.base import BaseBreezewayModel
from breezeway.models.company import Department
from breezeway.models.unit import Group


class Status(Enum):
    ACTIVE = 'active'
    INVITED = 'invited'
    INACTIVE = 'inactive'


@dataclass
class User(BaseBreezewayModel):
    id: int
    first_name: str
    last_name: str
    accept_decline_tasks: bool
    active: bool
    emails: list[str]
    employee_code: str
    groups: list[Group]
    shifts: dict
    type_departments: list[Department]
    type_role: str


    def convert_data_types(self):
        if not all(isinstance(department, Department) for department in self.type_departments):
            self.type_departments = [Department(department) for department in self.type_departments]
        if not all(isinstance(group, Group) for group in self.groups):
            self.groups = [Group(**group) for group in self.groups]