from abc import ABC, abstractmethod
from os import getenv
from typing import Literal

import httpx

from .errors import *
from .models.auth import JWTAuth
from .models.company import Company, Subdepartment, Template
from .models.unit import Unit
from .models.user import User, UserStatus


class BaseBreezewayClient(ABC):
    HEADERS = {'accept': 'application/json'}

    def __init__(self, client_id: str, client_secret: str, base_url: str, company_id: int | None = None):
        base_url = base_url or 'https://api.breezeway.io'
        client_id = client_id or getenv('BREEZEWAY_CLIENT_ID')
        client_secret = client_secret or getenv('BREEZEWAY_CLIENT_SECRET')
        if not client_id or not client_secret:
            raise AuthenticationError('client_id and client_secret are required either as parameters or environment variables'
                             'BREEZEWAY_CLIENT_ID and BREEZEWAY_CLIENT_SECRET')
        self.base_url: str = base_url.rstrip('/')
        self._company_id: int | None = int(company_id) if company_id else company_id
        self.auth: JWTAuth = JWTAuth(self.base_url, client_id, client_secret)

    @abstractmethod
    def _request(self, method: str, endpoint: str, query_params: dict = None, payload: dict = None) -> dict:
        pass

    @staticmethod
    def _filter_query_params(query_params: dict | None) -> dict:
        if query_params is None:
            return {}
        return {key: value for key, value in query_params.items() if value is not None}

    @staticmethod
    def _handle_response(resp: httpx.Response) -> None:
        if 'error' not in resp.json():
            return None
        if resp.json()['error'] == 'inactive client':
            raise AuthenticationError('Inactive client. Check your credentials.')
        if resp.status_code == 403:
            raise UnauthorizedError(resp.json()['description'])
        if resp.status_code == 429:
            raise RateLimitExceeded(resp.json())

        if resp.json() and 'description' in resp.json():
            raise APIClientError(f"API error: {resp.json()['description']}")
        raise APIClientError()

    @property
    def authenticated(self) -> bool:
        return self.auth.authenticated

    @property
    def company_id(self) -> int:
        if self._company_id:
            return self._company_id
        companies = self.companies()
        if not companies:
            raise NoCompaniesError()
        elif len(companies) > 1:
            raise MultipleCompaniesError()
        self._company_id = companies[0].id
        return self._company_id

    @company_id.setter
    def company_id(self, value: int):
        self._company_id = value

    def companies(self) -> list[Company]:
        endpoint = '/public/inventory/v1/companies'
        return [Company.from_json(company) for company in self._request('GET', endpoint)]

    def invite(self, user: User = None, user_id: int = None) -> None:
        if not (user or user_id):
            raise ValueError('Either user or user_id must be provided')
        if user and user_id:
            raise ValueError('Either user or user_id must be provided, not both')
        if user is not None:
            user_id = user.id
        endpoint = f'public/inventory/v1/people/{user_id}/invite'
        self._request('POST', endpoint)

    def subdepartments(self, company_id: int | None = None, reference_company_id: str | None = None) -> list[Subdepartment]:
        endpoint = 'public/inventory/v1/companies/subdepartments'
        query_params = {
            'company_id': company_id,
            'reference_company_id': reference_company_id
        }
        return [Subdepartment.from_json(subdepartment) for subdepartment in self._request('GET', endpoint, query_params=query_params)]

    def templates(self, company_id: int | None = None) -> list[Template]:
        endpoint = 'public/inventory/v1/companies/templates'
        query_params = {'company_id': company_id}
        return [Template.from_json(template) for template in self._request('GET', endpoint, query_params=query_params)]

    def units(self, company_id: int | None = None, limit: int | None = None, page: int | None = None, sort_by: str | None = None, sort_order: Literal['desc', 'asc'] | None = None) -> list[Unit]:
        endpoint = 'public/inventory/v1/property'
        query_params = {
            'company_id': company_id,
            'limit': limit,
            'page': page,
            'sort_by': sort_by,
            'sort_order': sort_order
        }
        return [Unit.from_json(unit) for unit in self._request('GET', endpoint, query_params=query_params)['results']]

    def user(self, user_id: int) -> User:
        endpoint = f'public/inventory/v1/people/{user_id}'
        return User.from_json(self._request('GET', endpoint))

    def users(self, status: UserStatus | None = None) -> list[User]:
        endpoint = 'public/inventory/v1/people'
        query_params = {'status': status.value} if status else None
        return [User.from_json(user) for user in self._request('GET', endpoint, query_params=query_params)]


class BreezewayClient(BaseBreezewayClient):
    def __init__(self, client_id=None, client_secret=None, base_url=None, company_id: int | None = None):
        super().__init__(client_id, client_secret, base_url, company_id)
        self.client = httpx.Client(auth=self.auth, base_url=self.base_url, headers=self.HEADERS)

    def _request(self, method: str, endpoint: str, query_params: dict | None = None, payload: dict = None) -> dict:
        resp = self.client.request(method, endpoint, json=payload, params=self._filter_query_params(query_params))
        resp.read()
        self._handle_response(resp)
        return resp.json()


class AsyncBreezewayClient(BaseBreezewayClient):
    def __init__(self, client_id=None, client_secret=None, base_url=None, company_id: int | None = None):
        super().__init__(client_id, client_secret, base_url, company_id)
        self.client = httpx.AsyncClient(auth=self.auth, base_url=self.base_url, headers=self.HEADERS)

    async def _request(self, method: str, endpoint: str, query_params: dict | None = None, payload: dict = None) -> dict:
        resp = await self.client.request(method, endpoint, json=payload, params=self._filter_query_params(query_params))
        await resp.aread()
        self._handle_response(resp)
        return resp.json()
