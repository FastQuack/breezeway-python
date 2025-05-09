from dataclasses import dataclass

from breezeway.models.base import BaseBreezewayModel


@dataclass
class UnitGroup(BaseBreezewayModel):
    id: int
    name: str
    parent_group_id: int


@dataclass
class UnitNotes(BaseBreezewayModel):
    access: str | None
    general: str | None
    wifi: str | None
    about: str | None
    direction: str | None
    trash_info: str | None

    @staticmethod
    def preprocess_data(json_data: dict) -> None:
        json_data.update({key: json_data.get(key, None) for key in ('access', 'general', 'wifi', 'about', 'direction', 'trash_info')})

@dataclass
class Unit(BaseBreezewayModel):
    id: int
    name: str
    address1: str
    address2: str | None
    building: str | None
    city: str
    company_id: int
    country: str
    display: str
    groups: list[UnitGroup]
    latitude: float | None
    longitude: float | None
    notes: UnitNotes
    photos: list[str]
    reference_company_id: str
    reference_external_property_id: str
    reference_property_id: str
    state: str
    status: str
    zipcode: str
    access_code: str | None = None

    @staticmethod
    def preprocess_data(json_data: dict) -> None:
        json_data['groups'] = [UnitGroup.from_json(group) for group in json_data['groups']]
        json_data['notes'] = UnitNotes.from_json(json_data['notes'])

