from datetime import date
from typing import TypedDict, Literal, Unpack

from httpx import Request

from .resource import BaseResource

class ReservationListDict(TypedDict, total=False):
    unit_id: int
    checkin_date_lt: date
    checkin_date_le: date
    checkin_date_gt: date
    checkin_date_ge: date
    checkout_date_lt: date
    checkout_date_le: date
    checkout_date_gt: date
    checkout_date_ge: date
    created_at_lt: date
    created_at_le: date
    created_at_gt: date
    created_at_ge: date
    property_id: int
    updated_at_lt: date
    updated_at_le: date
    updated_at_gt: date
    updated_at_ge: date
    limit: int
    page: int
    sort_by: str
    sort_order: Literal['desc', 'asc']
    company_id: int  # required if using cross-company access

class ReservationResource(BaseResource):
    def list_reservations(self, **kwargs: Unpack[ReservationListDict]) -> Request:
        """Get a paginated list of reservations."""
        endpoint = 'public/reservation/v1/reservation'
        if 'unit_id' in kwargs:
             kwargs['property_id'] = kwargs.pop('unit_id')
        return self._build_request('GET', endpoint, params=kwargs)