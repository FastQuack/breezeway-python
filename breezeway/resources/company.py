from typing import Any, Generator

from httpx import Request

from .base import BaseResource


class CompanyResource(BaseResource):
    def get_companies(self) -> Generator[Request, Any, None]:
        """Get all companies associated with the client."""
        endpoint = '/public/inventory/v1/companies'
        yield self._build_request('GET', endpoint)