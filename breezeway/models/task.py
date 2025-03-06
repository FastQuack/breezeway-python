from dataclasses import dataclass
from datetime import datetime, timedelta, time, date
from decimal import Decimal
from enum import Enum
from typing import List

from .base import BaseBreezewayModel
from .company import Department, Subdepartment


class Payor(Enum):
    DAMAGE = 'damage'
    GUEST = 'guest'
    INTERNAL = 'internal'
    OWNER = 'owner'
    INSURANCE = 'insurance'
    REVIEW = 'review'

    @property
    def name(self) -> str:
        return {
            Payor.DAMAGE: "Damage",
            Payor.GUEST: "Guest",
            Payor.INTERNAL: "No Charge/Internal",
            Payor.OWNER: "Owner",
            Payor.INSURANCE: "Insurance",
            Payor.REVIEW: "Review",

        }[self]


class TypeCost(Enum):  # TODO: Test that values are correct. Looks like they are actually integer values
    LABOR = 'labor'
    INSPECTION = 'inspection'
    MATERIAL = 'material'
    EXPENSE = 'expense'
    TAX = 'tax'
    SKILLED_LABOR = 'skilled_labor'
    NON_SKILLED_LABOR = 'non_skilled_labor'
    MILAGE = 'mileage'
    MARK_UP = 'mark_up'

    @property
    def name(self) -> str:
        return {
            TypeCost.LABOR: "Labor",
            TypeCost.MATERIAL: "Materials",
            TypeCost.EXPENSE: "Expense",
            TypeCost.TAX: "Tax",
            TypeCost.SKILLED_LABOR: "Skilled Labor",
            TypeCost.NON_SKILLED_LABOR: "Non-Skilled Labor",
            TypeCost.MILAGE: "Mileage",
            TypeCost.MARK_UP: "Markup"
        }[self]


class RateType(Enum):  # TODO Test this Enum
    HOUR = 'hour'
    PIECE = 'piece'

    @property
    def name(self) -> str:
        return {
            RateType.HOUR: "hourly",
            RateType.PIECE: "piece"
        }[self]


class Requester(Enum):
    OWNER = 'owner'
    GUEST = 'guest'
    GUEST_SURVEY = 'guest_survey'
    INSPECTOR = 'inspector'
    HOUSEKEEPER = 'housekeeper'
    MAINTENANCE_TECH = 'maintenance_tech'
    PROPERTY_SERVICES = 'property_services'
    PROPERTY_MANAGER = 'property_manager'
    DISPATCHER = 'dispatcher'

    @property
    def name(self) -> str:
        return {
            Requester.OWNER: "Owner",
            Requester.GUEST: "Guest",
            Requester.GUEST_SURVEY: "Guest Survey",
            Requester.INSPECTOR: "Inspector",
            Requester.HOUSEKEEPER: "Housekeeper",
            Requester.MAINTENANCE_TECH: "Maintenance Tech",
            Requester.PROPERTY_SERVICES: "Property Services",
            Requester.PROPERTY_MANAGER: "Property Manager",
            Requester.DISPATCHER: "Dispatcher"
        }[self]


class MarkupType(Enum):
    FLAT_RATE = 'flat_rate'
    PERCENT = 'percent'


class Priority(Enum):
    URGENT = 'urgent'
    HIGH = 'high'
    NORMAL = 'normal'
    LOW = 'low'
    WATCH = 'watch'


class TaskStatus(Enum):
    DRAFTED = 'drafted'
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
    CLOSED = 'closed'
    APPROVED = 'approved'
    DELETED = 'deleted'

    @property
    def name(self) -> str:
        return {
            TaskStatus.DRAFTED: "Drafted",
            TaskStatus.CREATED: "Created",
            TaskStatus.IN_PROGRESS: "In Progress",
            TaskStatus.FINISHED: "Finished",
            TaskStatus.CLOSED: "Closed",
            TaskStatus.APPROVED: "Approved",
            TaskStatus.DELETED: "Deleted"
        }[self]


@dataclass
class Assignment(BaseBreezewayModel):
    id: int
    name: str
    assignee_id: int
    employee_code: str | int | None  # Unsure what datatype this is
    expires_at: datetime | None  # I'm assuming this is iso format. I don't think I'm able to test.
    type_task_user_status: str

    @classmethod
    def preprocess_data(cls, data: dict):
        data['expires_at'] = datetime.fromisoformat(data['expires_at']) if data['expires_at'] else None


@dataclass
class Cost(BaseBreezewayModel):
    id: int
    cost: Decimal
    created_at: datetime
    description: str
    type_cost: TypeCost
    updated_at: datetime | None

    @classmethod
    def preprocess_data(cls, data: dict) -> None:
        data['cost'] = Decimal(data['cost']) if data['cost'] else None
        data['created_at'] = datetime.fromisoformat(data['created_at']) if data['created_at'] else None
        data['type_cost'] = TypeCost(data['type_cost']['code']) if data['type_cost'] else None
        data['updated_at'] = datetime.fromisoformat(data['updated_at']) if data['updated_at'] else None


@dataclass
class TaskSupply(BaseBreezewayModel):
    id: int
    name: str
    billable: bool
    description: str
    markup_pricing_type: MarkupType
    markup_rate: int
    quantity: int
    size: str
    supply_id: int
    total_price: Decimal
    unit_cost: Decimal

    @classmethod
    def preprocess_data(cls, data: dict) -> None:
        data['markup_pricing_type'] = MarkupType(data['markup_pricing_type']) if data['markup_pricing_type'] else None
        data['total_price'] = Decimal(data['total_price']) if data['total_price'] else None
        data['unit_cost'] = Decimal(data['unit_cost']) if data['unit_cost'] else None


@dataclass
class TaskTag(BaseBreezewayModel):
    id: int
    name: str
    company_id: int | None


@dataclass
class Task(BaseBreezewayModel):
    id: int
    name: str  # Title
    assignments: List[Assignment]
    bill_to: Payor | None
    costs: List[Cost]
    created_at: datetime
    created_by: None | str | dict  # TODO: Unknown type. Need to test.
    description: str | None
    finished_at: datetime | None
    finished_by: dict  # TODO use a model from people?
    home_id: int
    paused: bool
    photos: List[dict]  # TODO Unknown what this list looks like.
    rate_paid: str
    rate_type: RateType
    reference_property_id: str | None
    report_url: str
    requested_by: Requester | None
    scheduled_date: date | None
    scheduled_time: time | None
    started_at: str | None
    subdepartments: List[Subdepartment]
    supplies: List[TaskSupply]
    tags: List[str]
    task_tags: List[TaskTag]
    template_id: int | None
    total_time: timedelta | None
    type_department: Department
    type_priority: Priority
    type_task_status: TaskStatus
    updated_at: datetime

    @classmethod
    def preprocess_data(cls, data: dict):
        data['assignments'] = [Assignment.from_json(assignment) for assignment in data['assignments']]
        data['bill_to'] = Payor(data['bill_to']) if data['bill_to'] else None
        data['costs'] = [Cost.from_json(cost) for cost in data['costs']]
        data['created_at'] = datetime.fromisoformat(data['created_at']) if data['created_at'] else None
        data['finished_at'] = datetime.fromisoformat(data['finished_at']) if data['finished_at'] else None
        data['rate_type'] = RateType(data['rate_type']) if data['rate_type'] else None
        data['requested_by'] = Requester(data['requested_by']) if data['requested_by'] else None
        data['scheduled_date'] = date.fromisoformat(data['scheduled_date']) if data['scheduled_date'] else None
        data['scheduled_time'] = time.fromisoformat(data['scheduled_time']) if data['scheduled_time'] else None
        data['subdepartments'] = [Subdepartment.from_json(subdepartment) for subdepartment in data['subdepartments']]
        data['supplies'] = [TaskSupply.from_json(supply) for supply in data['supplies']]
        data['task_tags'] = [TaskTag.from_json(tag) for tag in data['task_tags']]
        if data['total_time']:
            total_time = datetime.fromisoformat(data['total_time'])
            data['total_time'] = timedelta(hours=total_time.hour, minutes=total_time.minute, seconds=total_time.second)
        data['type_department'] = Department(data['type_department']) if data['type_department'] else None
        data['priority'] = Priority(data['priority']) if data['priority'] else None
        data['type_task_status'] = TaskStatus(data['type_task_status']) if data['type_task_status'] else None
        data['updated_at'] = datetime.fromisoformat(data['updated_at']) if data['updated_at'] else None


@dataclass
class Comment(BaseBreezewayModel):
    id: int
    comment: str
    created_at: datetime

    @classmethod
    def preprocess_data(cls, data: dict) -> None:
        data['created_at'] = datetime.fromisoformat(data['created_at']) if data['created_at'] else None


@dataclass
class TaskRequirement(BaseBreezewayModel):
    action: List[str]
    home_element_name: str  # TODO: Testing
    note: str | None  # TODO: Testing
    photo_required: bool
    photos: list
    response: str  # TODO: testing
    section_name: str
    type_requirement: str  # TODO: Enum for Checklist, text, rating etc.
