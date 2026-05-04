from abc import ABC
from datetime import date
from typing import Any, Literal, Mapping, TypedDict, Never, NamedTuple
import httpx

from breezeway.resources.company import CompanyResource
from breezeway.resources.reservation import ReservationResource
from breezeway.resources.task import TaskResource
from breezeway.resources.unit import UnitResource
from breezeway.resources.user import UserResource


class BaseResource(ABC):

    def __init__(self, base_url: str):
        self._base_url = base_url

    def _build_request(
            self,
            method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
            endpoint: str,
            params: Mapping[str, Any] | None = None,
            payload: Mapping[str, Any] | list[int] | None = None
    ) -> httpx.Request:

        return httpx.Request(
            method=method,
            url=f'{self._base_url}{endpoint}',
            params=params,
            json=payload
        )


class Resource(BaseResource):

    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.company = CompanyResource(base_url)
        self.reservation = ReservationResource(base_url)
        self.task = TaskResource(base_url)
        self.unit = UnitResource(base_url)
        self.user = UserResource(base_url)


class DateRange(NamedTuple):
    start: date
    end: date

    def __str__(self):
        return f"{self.start.isoformat()},{self.end.isoformat()}"


class ListDict(TypedDict, total=False):
    limit: int | None  # Defaults to 100
    page: int | None  # Defaults to 1
    sort_by: str | None  # Defaults to 'created_at'
    sort_order: Literal['desc', 'asc'] | None  # Defaults to 'desc'
    company_id: int | None  # required if using cross-company access


class ListAllDict(TypedDict, total=False):
    limit: int | None  # Defaults to 100
    page: Never
    sort_by: str | None  # Defaults to 'created_at'
    sort_order: Literal['desc', 'asc'] | None  # Defaults to 'desc'
    company_id: int | None  # required if using cross-company access