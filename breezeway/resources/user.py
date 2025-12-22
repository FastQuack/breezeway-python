from typing import Any, Generator, TypedDict

from httpx import Request

from .base import BaseResource
from ..models.user import UserStatus


class UserResource(BaseResource):
    def list_users(self, status: UserStatus = UserStatus.ACTIVE) -> Generator[Request, Any, None]:
        """List users with the specified status"""
        endpoint = '/public/inventory/v1/people'
        yield self._build_request('GET', endpoint, params={'status': status})