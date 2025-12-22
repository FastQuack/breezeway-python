from typing import Any, Literal
import httpx


class BaseResource:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def _build_request(
            self,
            method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
            endpoint: str,
            params: dict[str, Any] | None = None,
            payload: Any | None = None
    ) -> httpx.Request:

        # Filter out None values from params to keep URLs clean
        clean_params = {k: v for k, v in (params or {}).items() if k is not 'self' and v is not None}

        return httpx.Request(
            method=method,
            url=f'{self.base_url}{endpoint}',
            params=clean_params,
            json=payload
        )