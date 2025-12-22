from abc import ABC, abstractmethod
from datetime import date
from os import getenv
from typing import Literal, overload, Unpack

import httpx

from .errors import *
from .models.auth import JWTAuth
from .models.company import Company, Subdepartment, Template
from .models.reservation import PaginatedReservations
from .models.unit import PaginatedUnits, Unit, UnitTag, UnitPhoto
from .models.user import User, UserStatus, InvitedUser
from .resources.company import CompanyResource
from .resources.unit import UnitCreateDict, UnitResource
from .resources.user import UserResource


class BaseBreezewayClient(ABC):
    HEADERS = {'accept': 'application/json'}

    def __init__(self, client_id: str, client_secret: str, base_url: str = 'https://api.breezeway.io', company_id: int | None = None):
        self.base_url = base_url.rstrip('/')
        client_id = client_id or getenv('BREEZEWAY_CLIENT_ID')
        client_secret = client_secret or getenv('BREEZEWAY_CLIENT_SECRET')
        if not client_id or not client_secret:
            raise AuthenticationError('client_id and client_secret are required as parameters or environment variables'
                             'BREEZEWAY_CLIENT_ID and BREEZEWAY_CLIENT_SECRET')
        self._company_id: int | None = int(company_id) if company_id else company_id
        self.auth: JWTAuth = JWTAuth(self.base_url, client_id, client_secret)
        self._company_resource = CompanyResource(base_url)
        self._unit_resource = UnitResource(base_url)
        self._user_resource = UserResource(base_url)

    @abstractmethod
    def _handle_request(self, request: httpx.Request) -> dict:
        pass

    @staticmethod
    def _handle_response(resp: httpx.Response) -> None:
        if 'error' not in resp.json():
            return None
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

    # def _get_user_data(self, status: UserStatus | None = None) -> dict:
    #     endpoint = '/public/inventory/v1/people'
    #     query_params = {'status': status.value if status else None}
    #     return self._request('GET', endpoint, query_params=query_params)

    @property
    def authenticated(self) -> bool:
        return self.auth.authenticated

    def paginated_reservations(
            self,* ,
            property_id: int | None = None,
            company_id: int | None = None,
            checkin_date_lt: date | None = None,
            checkin_date_le: date | None = None,
            checkin_date_gt: date | None = None,
            checkin_date_ge: date | None = None,
            checkout_date_lt: date | None = None,
            checkout_date_le: date | None = None,
            checkout_date_gt: date | None = None,
            checkout_date_ge: date | None = None,
            created_at_lt: date | None = None,
            created_at_le: date | None = None,
            created_at_gt: date | None = None,
            created_at_ge: date | None = None,
            updated_at_lt: date | None = None,
            updated_at_le: date | None = None,
            updated_at_gt: date | None = None,
            updated_at_ge: date | None = None,
            limit: int | None = None,
            page: int | None = None,
            sort_by: str | None = None,
            sort_order: Literal['desc', 'asc'] | None = None) -> PaginatedReservations:
        """Get a paginated list of reservations."""
        endpoint = 'public/reservation/v1/reservation'
        query_params = {
            'property_id': property_id,
            'company_id': company_id,
            'checkin_date_lt': checkin_date_lt,
            'checkin_date_le': checkin_date_le,
            'checkin_date_gt': checkin_date_gt,
            'checkin_date_ge': checkin_date_ge,
            'checkout_date_lt': checkout_date_lt,
            'checkout_date_le': checkout_date_le,
            'checkout_date_gt': checkout_date_gt,
            'checkout_date_ge': checkout_date_ge,
            'created_at_lt': created_at_lt,
            'created_at_le': created_at_le,
            'created_at_gt': created_at_gt,
            'created_at_ge': created_at_ge,
            'updated_at_lt': updated_at_lt,
            'updated_at_le': updated_at_le,
            'updated_at_gt': updated_at_gt,
            'updated_at_ge': updated_at_ge,
            'limit': limit,
            'page': page,
            'sort_by': sort_by,
            'sort_order': sort_order
        }
        paginated_reservations = PaginatedReservations.model_validate(self._request('GET', endpoint, query_params=query_params))
        for reservation in paginated_reservations.results:
            reservation.attach_client(self)
        return paginated_reservations

    def paginated_units(self, company_id: int | None = None, limit: int | None = None, page: int | None = None, sort_by: str | None = None, sort_order: Literal['desc', 'asc'] | None = None) -> PaginatedUnits:
        """
        Get a paginated list of units.
        Company ID is required for clients with multi-company access.
        """
        endpoint = 'public/inventory/v1/property'
        query_params = {
            'company_id': company_id,
            'limit': limit,
            'page': page,
            'sort_by': sort_by,
            'sort_order': sort_order
        }
        paginated_units = PaginatedUnits.model_validate(self._request('GET', endpoint, query_params=query_params))
        for unit in paginated_units.results:
            unit.attach_client(self)
        return paginated_units

    def reservations(
            self,* ,
            property_id: int | None = None,
            company_id: int | None = None,
            checkin_date_lt: date | None = None,
            checkin_date_le: date | None = None,
            checkin_date_gt: date | None = None,
            checkin_date_ge: date | None = None,
            checkout_date_lt: date | None = None,
            checkout_date_le: date | None = None,
            checkout_date_gt: date | None = None,
            checkout_date_ge: date | None = None,
            created_at_lt: date | None = None,
            created_at_le: date | None = None,
            created_at_gt: date | None = None,
            created_at_ge: date | None = None,
            updated_at_lt: date | None = None,
            updated_at_le: date | None = None,
            updated_at_gt: date | None = None,
            updated_at_ge: date | None = None,
            limit: int | None = None,
            sort_by: str | None = None,
            sort_order: Literal['desc', 'asc'] | None = None):
        """Get a list of reservations."""
        endpoint = 'public/reservation/v1/reservation'
        query_params = {
            'property_id': property_id,
            'company_id': company_id,
            'checkin_date_lt': checkin_date_lt,
            'checkin_date_le': checkin_date_le,
            'checkin_date_gt': checkin_date_gt,
            'checkin_date_ge': checkin_date_ge,
            'checkout_date_lt': checkout_date_lt,
            'checkout_date_le': checkout_date_le,
            'checkout_date_gt': checkout_date_gt,
            'checkout_date_ge': checkout_date_ge,
            'created_at_lt': created_at_lt,
            'created_at_le': created_at_le,
            'created_at_gt': created_at_gt,
            'created_at_ge': created_at_ge,
            'updated_at_lt': updated_at_lt,
            'updated_at_le': updated_at_le,
            'updated_at_gt': updated_at_gt,
            'updated_at_ge': updated_at_ge,
            'limit': limit,
            'sort_by': sort_by,
            'sort_order': sort_order
        }
        paginated_reservations = self.paginated_reservations(**query_params)
        reservations = paginated_reservations.results
        for page in range(2, paginated_reservations.total_pages + 1):
            reservations += self.paginated_reservations(**query_params, page=page).results
        return [reservation.attach_client(self) for reservation in reservations]


    def set_default_photo_for_unit(self, unit: Unit, photo: UnitPhoto) -> Unit:
        """Set a default photo for a unit."""
        endpoint = f'public/inventory/v1/property/{unit.id}/default_photo'
        payload = {'photo_id': photo.id}
        return Unit.model_validate(self._request('PATCH', endpoint, payload=payload))

    def subdepartments(self, company_id: int | None = None, reference_company_id: str | None = None) -> list[Subdepartment]:
        """
        Get a list of all subdepartments associated with the company.
        Company ID is required for clients with multi-company access.
        """
        endpoint = 'public/inventory/v1/companies/subdepartments'
        query_params = {
            'company_id': company_id,
            'reference_company_id': reference_company_id
        }
        return [Subdepartment.model_validate(subdepartment) for subdepartment in self._request('GET', endpoint, query_params=query_params)]

    def templates(self, company_id: int | None = None) -> list[Template]:
        """
        Get a list of all templates associated with the company.
        Company ID is required for clients with multi-company access.
        """
        endpoint = 'public/inventory/v1/companies/templates'
        query_params = {'company_id': company_id}
        return [Template.model_validate(template) for template in self._request('GET', endpoint, query_params=query_params)]

    def unit(self, unit_id: int) -> Unit:
        """Get a unit by its ID."""
        endpoint = f'public/inventory/v1/property/{unit_id}'
        return Unit.model_validate(self._request('GET', endpoint)).attach_client(self)

    def units(self, company_id: int | None = None, sort_by: str | None = None, sort_order: Literal['desc', 'asc'] | None = None) -> list[Unit]:
        """
        Get a list of all units associated with the company.
        Company ID is required for clients with multi-company access.
        """
        paginated_units = self.paginated_units(company_id=company_id, sort_by=sort_by, sort_order=sort_order)
        units = paginated_units.results
        for page in range(2, paginated_units.total_pages + 1):
            units += self.paginated_units(company_id=company_id, page=page, sort_by=sort_by, sort_order=sort_order).results
        return [unit.attach_client(self) for unit in units]

    def unit_tags(self, company_id: int | None = None) -> list[UnitTag]:
        """
        List property tags configured for a Breezeway company; creation of company tags must be performed within the app.
        company_id is required for clients with multi-company access.
        """
        endpoint = f'public/inventory/v1/property/tags'
        query_params = {'company_id': company_id}
        return [UnitTag.model_validate(tag) for tag in self._request('GET', endpoint, query_params=query_params)]

    def user(self, user_id: int) -> User:
        """Get a user by their ID."""
        endpoint = f'public/inventory/v1/people/{user_id}'
        return User.model_validate(self._request('GET', endpoint)).attach_client(self)


class BreezewayClient(BaseBreezewayClient):
    def __init__(self, client_id=None, client_secret=None, base_url=None, company_id: int | None = None):
        super().__init__(client_id, client_secret, base_url, company_id)
        self.client = httpx.Client(auth=self.auth, base_url=self.base_url, headers=self.HEADERS)

    def _handle_request(self, request: httpx.Request) -> dict:
        response = self.client.send(request)
        self._handle_response(response)
        return response.json()

    def companies(self) -> list[Company]:
        """Get a list of all companies associated with the client."""
        request = next(self._company_resource.get_companies())
        data = self._handle_request(request)
        return [Company.model_validate(company) for company in data]

    def create_unit(self, **kwargs: Unpack[UnitCreateDict]) -> Unit:
        """Create a new unit."""
        request = next(self._unit_resource.create_unit(**kwargs))
        data = self._handle_request(request)
        return Unit.model_validate(data).attach_client(self)

    @overload
    def users(self, status: UserStatus.INVITED) -> list[InvitedUser]: ...

    @overload
    def users(self, status: UserStatus = UserStatus.ACTIVE) -> list[User]: ...

    def users(self, status: UserStatus = UserStatus.ACTIVE) -> list[User]:
        request = next(self._user_resource.list_users(status=status))
        data = self._handle_request(request)
        return [User.model_validate(user) for user in data]


class AsyncBreezewayClient(BaseBreezewayClient):
    def __init__(self, client_id=None, client_secret=None, base_url=None, company_id: int | None = None):
        super().__init__(client_id, client_secret, base_url, company_id)
        self.client = httpx.AsyncClient(auth=self.auth, base_url=self.base_url, headers=self.HEADERS)

    async def _handle_request(self, request: httpx.Request) -> dict:
        response = await self.client.send(request)
        self._handle_response(response)
        return response.json()

    async def companies(self) -> list[Company]:
        """Get a list of all companies associated with the client."""
        request = next(self._company_resource.get_companies())
        data = await self._handle_request(request)
        return [Company.model_validate(company) for company in data]

    async def create_unit(self, **kwargs: Unpack[UnitCreateDict]) -> Unit:
        """Create a new unit."""
        request = next(self._unit_resource.create_unit(**kwargs))
        data = await self._handle_request(request)
        return Unit.model_validate(data).attach_client(self)

    @overload
    async def users(self, status: UserStatus.INVITED) -> list[InvitedUser]: ...

    @overload
    async def users(self, status: UserStatus = UserStatus.ACTIVE) -> list[User]: ...

    async def users(self, status: UserStatus = UserStatus.ACTIVE) -> list[User]:
        request = next(self._user_resource.list_users(status=status))
        data = await self._handle_request(request)
        return [User.model_validate(user) for user in data]

    # async def units(self, company_id: int | None = None, sort_by: str | None = None, sort_order: Literal['desc', 'asc'] | None = None) -> list[Unit]:
    #     paginated_units = await self.paginated_units(company_id=company_id, sort_by=sort_by, sort_order=sort_order)
    #     units = paginated_units.results
    #     tasks = [
    #         self.paginated_units(company_id=company_id, page=page, sort_by=sort_by, sort_order=sort_order)
    #         for page in range(2, paginated_units.total_pages + 1)
    #     ]
    #     for result in await asyncio.gather(*tasks):
    #         units += result.results
    #     return units
