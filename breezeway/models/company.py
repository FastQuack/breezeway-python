from enum import StrEnum

from pydantic import Field

from breezeway.models.base import BaseBreezewayModel


class Department(StrEnum):
    HOUSEKEEPING = 'housekeeping'
    INSPECTION = 'inspection'
    MAINTENANCE = 'maintenance'
    SAFETY = 'safety'
    MANAGEMENT = 'management'
    OFFICE = 'office'
    FINANCE = 'finance'
    ACCOUNTING = 'accounting'
    PROPERTY_SERVICES = 'property_services'
    GUEST_SERVICES = 'guest_services'
    OWNER_SERVICES = 'owner_services'
    VENDORS = 'vendors'
    CONCIERGE = 'concierge'
    EXPERIENCES = 'experiences'
    RESERVATIONS = 'reservations'
    LOST_AND_FOUND = 'lost_and_found'

    @property
    def name(self) -> str:
        return {
            Department.HOUSEKEEPING: "Cleaning",
            Department.INSPECTION: "Inspection",
            Department.MAINTENANCE: "Maintenance",
            Department.SAFETY: "Safety",
            Department.MANAGEMENT: "Management",
            Department.OFFICE: "Office",
            Department.FINANCE: "Finance",
            Department.ACCOUNTING: "Accounting",
            Department.PROPERTY_SERVICES: "Property Services",
            Department.GUEST_SERVICES: "Guest Services",
            Department.OWNER_SERVICES: "Owner Services",
            Department.VENDORS: "Vendors",
            Department.CONCIERGE: "Concierge",
            Department.EXPERIENCES: "Experiences",
            Department.RESERVATIONS: "Reservations",
            Department.LOST_AND_FOUND: "Lost and Found",
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
