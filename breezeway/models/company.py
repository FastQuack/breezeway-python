from enum import StrEnum

from pydantic import Field

from breezeway.models.base import BaseBreezewayModel


class Department(StrEnum):
    HOUSEKEEPING = 'housekeeping'
    INSPECTION = 'inspection'
    MAINTENANCE = 'maintenance'
    ACCOUNTING = 'accounting'
    CONCIERGE = 'concierge'
    EXPERIENCES = 'experiences'
    FINANCE = 'finance'
    GUEST_SERVICES = 'guest_services'
    LINENS = 'linens'
    LOST_AND_FOUND = 'lost_and_found'
    MANAGEMENT = 'management'
    OFFICE = 'office'
    OWNER_SERVICES = 'owner_services'
    PROPERTY_SERVICES = 'property_services'
    RESERVATIONS = 'reservations'
    SAFETY = 'safety'
    VENDORS = 'vendors'

    @property
    def name(self) -> str:
        return {
            Department.HOUSEKEEPING: '"Cleaning',
            Department.INSPECTION: 'Inspection',
            Department.MAINTENANCE: 'Maintenance',
            Department.ACCOUNTING: 'Accounting',
            Department.CONCIERGE: 'Concierge',
            Department.EXPERIENCES: 'Experiences',
            Department.FINANCE: 'Finance',
            Department.GUEST_SERVICES: 'Guest Services',
            Department.LINENS: 'Linens',
            Department.LOST_AND_FOUND: 'Lost and Found',
            Department.MANAGEMENT: 'Management',
            Department.OFFICE: 'Office',
            Department.OWNER_SERVICES: 'Owner Services',
            Department.PROPERTY_SERVICES: 'Property Services',
            Department.RESERVATIONS: 'Reservations',
            Department.SAFETY: 'Safety',
            Department.VENDORS: 'Vendors',
        }[self]


class Company(BaseBreezewayModel):
    id: int
    name: str
    reference_company_id: str | None = None


class Subdepartment(BaseBreezewayModel):
    id: int
    name: str


class Template(BaseBreezewayModel):
    id: int
    name: str = Field(validation_alias='template_name', serialization_alias='template_name')
    department: Department = Field(validation_alias='department_code', serialization_alias='department_code')
