from typing import Any, Generator, TypedDict, Unpack

from httpx import Request

from .base import BaseResource
from ..models.unit import UnitStatus, UnitNotes

class UnitCreateDict(TypedDict):
    name: str
    internal_code: str
    address1: str | None
    address2: str | None
    city: str | None
    state: str | None
    zipcode: str | None
    country: str | None
    latitude: float | None
    longitude: float | None
    photos: list[str] | None
    status: UnitStatus | None
    building: str | None
    notes: UnitNotes | None
    bedrooms: int | None
    bathrooms: int | None
    access_code: str | None
    guest_access_code: str | None
    wifi_name: str | None
    wifi_password: str | None
    company_id: int | None  # required if using cross-company access


class UnitResource(BaseResource):
    def create_unit(self, **kwargs: Unpack[UnitCreateDict]) -> Generator[Request, Any, None]:
        """Create a new property"""
        payload = locals()
        endpoint = '/public/inventory/v1/property'
        yield self._build_request('POST', endpoint, payload=payload)