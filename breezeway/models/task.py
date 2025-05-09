from dataclasses import dataclass
from datetime import datetime, timedelta, time, date
from decimal import Decimal
from enum import Enum

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

    @staticmethod
    def preprocess_data(json_data: dict):
        json_data['expires_at'] = datetime.fromisoformat(json_data['expires_at']) if json_data['expires_at'] else None


@dataclass
class Cost(BaseBreezewayModel):
    id: int
    cost: Decimal
    created_at: datetime
    description: str
    type_cost: TypeCost
    updated_at: datetime | None

    @staticmethod
    def preprocess_data(json_data: dict) -> None:
        json_data['cost'] = Decimal(json_data['cost']) if json_data['cost'] else None
        json_data['created_at'] = datetime.fromisoformat(json_data['created_at']) if json_data['created_at'] else None
        json_data['type_cost'] = TypeCost(json_data['type_cost']['code']) if json_data['type_cost'] else None
        json_data['updated_at'] = datetime.fromisoformat(json_data['updated_at']) if json_data['updated_at'] else None


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

    @staticmethod
    def preprocess_data(json_data: dict) -> None:
        json_data['markup_pricing_type'] = MarkupType(json_data['markup_pricing_type']) if json_data['markup_pricing_type'] else None
        json_data['total_price'] = Decimal(json_data['total_price']) if json_data['total_price'] else None
        json_data['unit_cost'] = Decimal(json_data['unit_cost']) if json_data['unit_cost'] else None


@dataclass
class TaskTag(BaseBreezewayModel):
    
    id: int
    name: str
    company_id: int | None


@dataclass
class Task(BaseBreezewayModel):
    id: int
    name: str  # Title
    assignments: list[Assignment]
    bill_to: Payor | None
    costs: list[Cost]
    created_at: datetime
    created_by: None | str | dict  # TODO: Unknown type. Need to test.
    description: str | None
    finished_at: datetime | None
    finished_by: dict  # TODO use a model from people?
    home_id: int
    paused: bool
    photos: list[dict]  # TODO Unknown what this list looks like.
    rate_paid: str
    rate_type: RateType
    reference_property_id: str | None
    report_url: str
    requested_by: Requester | None
    scheduled_date: date | None
    scheduled_time: time | None
    started_at: str | None
    subdepartments: list[Subdepartment]
    supplies: list[TaskSupply]
    tags: list[str]
    task_tags: list[TaskTag]
    template_id: int | None
    total_time: timedelta | None
    type_department: Department
    type_priority: Priority
    type_task_status: TaskStatus
    updated_at: datetime

    @staticmethod
    def preprocess_data(json_data: dict):
        json_data['assignments'] = [Assignment.from_json(assignment) for assignment in json_data['assignments']]
        json_data['bill_to'] = Payor(json_data['bill_to']) if json_data['bill_to'] else None
        json_data['costs'] = [Cost.from_json(cost) for cost in json_data['costs']]
        json_data['created_at'] = datetime.fromisoformat(json_data['created_at']) if json_data['created_at'] else None
        json_data['finished_at'] = datetime.fromisoformat(json_data['finished_at']) if json_data['finished_at'] else None
        json_data['rate_type'] = RateType(json_data['rate_type']) if json_data['rate_type'] else None
        json_data['requested_by'] = Requester(json_data['requested_by']) if json_data['requested_by'] else None
        json_data['scheduled_date'] = date.fromisoformat(json_data['scheduled_date']) if json_data['scheduled_date'] else None
        json_data['scheduled_time'] = time.fromisoformat(json_data['scheduled_time']) if json_data['scheduled_time'] else None
        json_data['subdepartments'] = [Subdepartment.from_json(subdepartment) for subdepartment in json_data['subdepartments']]
        json_data['supplies'] = [TaskSupply.from_json(supply) for supply in json_data['supplies']]
        json_data['task_tags'] = [TaskTag.from_json(tag) for tag in json_data['task_tags']]
        if json_data['total_time']:
            total_time = datetime.fromisoformat(json_data['total_time'])
            json_data['total_time'] = timedelta(hours=total_time.hour, minutes=total_time.minute, seconds=total_time.second)
        json_data['type_department'] = Department(json_data['type_department']) if json_data['type_department'] else None
        json_data['priority'] = Priority(json_data['priority']) if json_data['priority'] else None
        json_data['type_task_status'] = TaskStatus(json_data['type_task_status']) if json_data['type_task_status'] else None
        json_data['updated_at'] = datetime.fromisoformat(json_data['updated_at']) if json_data['updated_at'] else None


@dataclass
class Comment(BaseBreezewayModel):
    id: int
    comment: str
    created_at: datetime

    @staticmethod
    def preprocess_data(json_data: dict) -> None:
        json_data['created_at'] = datetime.fromisoformat(json_data['created_at']) if json_data['created_at'] else None


@dataclass
class TaskRequirement(BaseBreezewayModel):
    action: list[str]
    home_element_name: str  # TODO: Testing
    note: str | None  # TODO: Testing
    photo_required: bool
    photos: list
    response: str  # TODO: testing
    section_name: str
    type_requirement: str  # TODO: Enum for Checklist, text, rating etc.
