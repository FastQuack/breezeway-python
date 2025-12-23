from datetime import date
from typing import Any, Literal, Mapping, TypedDict, Never, NamedTuple
import httpx


class BaseResource:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def _build_request(
            self,
            method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
            endpoint: str,
            params: Mapping[str, Any] | None = None,
            payload: Mapping[str, Any] | None = None
    ) -> httpx.Request:

        return httpx.Request(
            method=method,
            url=f'{self.base_url}{endpoint}',
            params=params,
            json=payload
        )


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