from typing import TypedDict, Unpack

from httpx import Request

from .base import BaseResource, ListDict
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
    def create_unit(self, **kwargs: Unpack[UnitCreateDict]) -> Request:
        """
        Create a new property.
        Company ID is required for clients with multi-company access.
        """
        endpoint = '/public/inventory/v1/property'
        payload = kwargs
        return self._build_request('POST', endpoint, payload=payload)

    def list_units(self, **kwargs: Unpack[ListDict]) -> Request:
        """
        Get a paginated list of units.
        Company ID is required for clients with multi-company access.
        """
        endpoint = 'public/inventory/v1/property'
        params = kwargs
        return self._build_request('GET', endpoint, params=params)

    def list_unit_tags(self, company_id):
        """
        List unit tags configured for a Breezeway company
        Creation of company tags must be performed within the app.
        Company ID is required for clients with multi-company access.
        """
        endpoint = f'public/inventory/v1/property/tags'
        params = {'company_id': company_id}
        return self._build_request('GET', endpoint, params=params)

    def retrieve_unit(self, unit_id: int) -> Request:
        """
        Retrieve a unit by its Breezeway ID.
        """
        endpoint = f'public/inventory/v1/property/{unit_id}'
        return self._build_request('GET', endpoint)

    def update_default_photo(self, *, unit_id: int, photo_id: int) -> Request:
        endpoint = f'public/inventory/v1/property/{unit_id}/default_photo'
        payload = {'photo_id': photo_id}
        return self._build_request('PATCH', endpoint, payload=payload)