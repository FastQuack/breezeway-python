from __future__ import annotations

from abc import ABC, abstractmethod
from os import getenv
from typing import Unpack, NoReturn, Any, TYPE_CHECKING

from httpx import AsyncClient, Client, Request, Response

from .auth import JWTAuth
from .clients.company import CompanyClient, AsyncCompanyClient
from .clients.reservation import ReservationClient, AsyncReservationClient
from .clients.task import TaskClient
from .clients.unit import UnitClient, AsyncUnitClient
from .entities.entity import Entity, AsyncEntity
from .errors import *
from .resources.reservation import ReservationResource
from .resources.resource import Resource

if TYPE_CHECKING:
    from .models.base import Paginated
    from .models.reservation import Reservation
    from .models.task import Task
    from .models.user import User, UserStatus
    from .resources.reservation import ReservationListDict
    from .resources.task import TaskListDict


class BaseBreezewayClient(ABC):
    HEADERS = {'accept': 'application/json'}

    def __init__(self, client_id: str, client_secret: str, base_url: str, company_id: int | None = None):
        self.base_url = base_url.rstrip('/')
        client_id = client_id or getenv('BREEZEWAY_CLIENT_ID')
        client_secret = client_secret or getenv('BREEZEWAY_CLIENT_SECRET')
        if not client_id or not client_secret:
            raise AuthenticationError('client_id and client_secret are required as parameters or environment variables'
                             'BREEZEWAY_CLIENT_ID and BREEZEWAY_CLIENT_SECRET')
        self.company_id: int | None = int(company_id) if company_id else company_id
        self.auth: JWTAuth = JWTAuth(base_url, client_id, client_secret)
        self.resource = Resource(base_url)

    @abstractmethod
    def process_request(self, request: Request) -> Any:
        pass

    @staticmethod
    def _handle_response_error(resp: Response) -> NoReturn:
            if resp.json()['error'] == 'inactive client':
                raise AuthenticationError('Inactive client. Check your credentials.')
            if resp.status_code == 403:
                raise UnauthorizedError(resp.json()['description'])
            if resp.status_code == 404:
                raise NotFoundError('Resource not found. Are you using the correct endpoint?')
            if resp.status_code == 429:
                raise RateLimitExceeded(resp.json())
            if resp.json() and 'description' in resp.json():
                raise APIClientError(f"API error: {resp.json()['description']}")
            raise APIClientError()

    def _process_response(self, resp: Response) -> Any:
        data = resp.json()
        if isinstance(data, dict) and 'error' in data:
            self._handle_response_error(resp)
        return data

    @property
    def authenticated(self) -> bool:
        return self.auth.authenticated


class BreezewayClient(BaseBreezewayClient):
    def __init__(
            self,
            client_id: str = None,
            client_secret: str = None,
            base_url: str = 'https://api.breezeway.io',
            company_id: int | None = None
    ):
        super().__init__(client_id, client_secret, base_url, company_id)
        self.client = Client(auth=self.auth, base_url=base_url, headers=self.HEADERS)

    def process_request(self, request: Request) -> Any:
        response = self.client.send(request)
        return self._process_response(response)


class AsyncBreezewayClient(BaseBreezewayClient):
    def __init__(
            self,
            client_id: str = None,
            client_secret: str = None,
            base_url: str = 'https://api.breezeway.io',
            company_id: int | None = None
    ):
        super().__init__(client_id, client_secret, base_url, company_id)
        self.client = AsyncClient(auth=self.auth, base_url=base_url, headers=self.HEADERS)

    async def process_request(self, request: Request) -> Any:
        response = await self.client.send(request)
        return self._process_response(response)


class Breezeway:
    def __init__(
            self,
            client_id: str = None,
            client_secret: str = None,
            base_url: str = 'https://api.breezeway.io',
            company_id: int | None = None
    ):
        self._client = BreezewayClient(client_id, client_secret, base_url, company_id)
        Entity.configure(self)
        self.company = CompanyClient(self._client)
        self.reservation = ReservationClient(self._client)
        self.task = TaskClient(self._client)
        self.unit = UnitClient(self._client)


    def reservations(self, **kwargs: Unpack[ReservationListDict]) -> Paginated[Reservation]:
        """
        Get a paginated list of reservations.
        Company ID is required for clients with multi-company access.
        """
        request = ReservationResource.list_reservations(**kwargs)
        data = self._client.process_request(request)
        return Paginated[Reservation].model_validate(data)

    def tasks(self, **kwargs: Unpack[TaskListDict]) -> Paginated[Task]:
        """
        Get a paginated list of tasks.
        Company ID is required for clients with multi-company access.
        """
        request = self._client.resource.task.list_tasks(**kwargs)
        data = self._client.process_request(request)
        return Paginated[Task].model_validate(data)

    def users(self, status: UserStatus | None) -> list[User]:
        """
        Get a list of users associated with the client.
        """
        request = self._client.resource.user.list_users(status=status)
        data = self._client.process_request(request)
        return [User.model_validate(user) for user in data]

    def user(self, user_id: int) -> User:
        """
        Retrieve a user by their ID.
        """
        request = self._client.resource.user.retrieve_user(user_id=user_id)
        data = self._client.process_request(request)
        return User.model_validate(data)


class AsyncBreezeway:
    def __init__(
            self,
            client_id: str = None,
            client_secret: str = None,
            base_url: str = 'https://api.breezeway.io',
            company_id: int | None = None
    ):
        self._client = AsyncBreezewayClient(client_id, client_secret, base_url, company_id)
        AsyncEntity.configure(self)
        self.company = AsyncCompanyClient(self._client)
        self.reservation = AsyncReservationClient(self._client)
        self.unit = AsyncUnitClient(self._client)

    async def reservations(self, **kwargs: Unpack[ReservationListDict]) -> Paginated[Reservation]:
        """
        Get a paginated list of reservations.
        Company ID is required for clients with multi-company access.
        """
        request = ReservationResource.list_reservations(**kwargs)
        data = await self._client.process_request(request)
        return Paginated[Reservation].model_validate(data)

    async def tasks(self, **kwargs: Unpack[TaskListDict]) -> Paginated[Task]:
        """
        Get a paginated list of tasks.
        Company ID is required for clients with multi-company access.
        """
        request = self._client.resource.task.list_tasks(**kwargs)
        data = await self._client.process_request(request)
        return Paginated[Task].model_validate(data)

    async def users(self, status: UserStatus | None) -> list[User]:
        """
        Get a list of users associated with the client.
        """
        request = self._client.resource.company.list_users(status=status)
        data = await self._client.process_request(request)
        return [User.model_validate(user) for user in data]

    async def user(self, user_id: int) -> User:
        """
        Retrieve a user by their ID.
        """
        request = self._client.resource.user.retrieve_user(user_id=user_id)
        data = await self._client.process_request(request)
        return User.model_validate(data)