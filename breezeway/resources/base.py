from abc import ABC
from dataclasses import dataclass
from datetime import date
from typing import Literal, Mapping, Any, NamedTuple, TypedDict, BinaryIO, Never

import httpx


RequestFileContent = bytes | str | BinaryIO
RequestFileValue = (
    RequestFileContent
    | tuple[str, RequestFileContent]
    | tuple[str, RequestFileContent, str]
    | tuple[str, RequestFileContent, str, Mapping[str, str]]
)
RequestFiles = Mapping[str, RequestFileValue]


class BaseResource(ABC):

    def __init__(self, base_url: str):
        self._base_url = base_url

    def _build_request(
            self,
            method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
            endpoint: str,
            *,
            params: Mapping[str, Any] | None = None,
            payload: Mapping[str, Any] | list[int] | None = None,
            files: RequestFiles | None = None
    ) -> httpx.Request:

        return httpx.Request(
            method=method,
            url=f'{self._base_url}{endpoint}',
            params=params,
            json=payload,
            files=files
        )

@dataclass
class DateRange:
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