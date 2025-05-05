from abc import ABC, abstractmethod
from os import getenv
from typing import List, Optional

import httpx

from .models.auth import JWTAuth
from .models.company import Company, Subdepartment, Template
from .models.user import User, Status


class BaseBreezewayClient(ABC):
    HEADERS = {'accept': 'application/json'}

    def __init__(self, client_id: str, client_secret: str, base_url: str, company_id: Optional[int] = None):
        base_url = base_url or 'https://api.breezeway.io'
        client_id = client_id or getenv('BREEZEWAY_CLIENT_ID')
        client_secret = client_secret or getenv('BREEZEWAY_CLIENT_SECRET')
        if not client_id or not client_secret:
            raise ValueError('client_id and client_secret are required either as parameters or environment variables '
                             'BREEZEWAY_CLIENT_ID and BREEZEWAY_CLIENT_SECRET')
        self.base_url: str = base_url.rstrip('/')
        self._company_id: Optional[int] = int(company_id) if company_id else company_id
        self.auth: httpx.Auth = JWTAuth(self.base_url, client_id, client_secret)

    @abstractmethod
    def _request(self, method: str, endpoint: str, query_params: dict = None, payload: dict = None) -> dict:
        pass

    @property
    def company_id(self) -> int:
        if self._company_id:
            return self._company_id
        companies = self.companies()
        if not companies:
            raise RuntimeError('No companies found')
        elif len(companies) > 1:
            raise RuntimeError('Multiple companies found. '
                               'You must specify a company id when initializing the client')
        self._company_id = companies[0].id
        return self._company_id

    @company_id.setter
    def company_id(self, value: int):
        self._company_id = value

    def companies(self) -> List[Company]:
        endpoint = '/public/inventory/v1/companies'
        return [Company.from_json(company) for company in self._request('GET', endpoint)]

    def invite(self, user_id: int) -> None:
        endpoint = f'public/inventory/v1/people/{user_id}/invite'
        self._request('POST', endpoint)

    def subdepartments(self) -> List[Subdepartment]:
        endpoint = 'public/inventory/v1/companies/subdepartments'
        payload = {'company_id': self.company_id}
        return [Subdepartment.from_json(subdepartment) for subdepartment in self._request('GET', endpoint, payload=payload)]

    def templates(self) -> List[Template]:
        endpoint = 'public/inventory/v1/companies/templates'
        payload = {'company_id': self.company_id}
        return [Template.from_json(template) for template in self._request('GET', endpoint, payload=payload)]

    def user(self, user_id: int) -> User:
        endpoint = f'public/inventory/v1/people/{user_id}'
        return User.from_json(self._request('GET', endpoint))

    def users(self, status: Optional[Status] = None) -> List[User]:
        endpoint = 'public/inventory/v1/people'
        query_params = {'status': status.value} if status else None
        return [User.from_json(user) for user in self._request('GET', endpoint, query_params=query_params)]


class BreezewayClient(BaseBreezewayClient):
    def __init__(self, client_id=None, client_secret=None, base_url=None, company_id: Optional[int] = None):
        super().__init__(client_id, client_secret, base_url, company_id)
        self.client = httpx.Client(auth=self.auth, base_url=self.base_url, headers=self.HEADERS)

    def _request(self, method: str, endpoint: str, query_params: dict = None, payload: dict = None) -> dict:
        if query_params:
            endpoint += '?' + '&'.join(f'{key}={value}' for key, value in query_params.items())
        resp = self.client.request(method, endpoint, json=payload)
        resp.read()
        return resp.json()


class AsyncBreezewayClient(BaseBreezewayClient):
    def __init__(self, client_id=None, client_secret=None, base_url=None, company_id: Optional[int] = None):
        super().__init__(client_id, client_secret, base_url, company_id)
        self.client = httpx.AsyncClient(auth=self.auth, base_url=self.base_url, headers=self.HEADERS)

    async def _request(self, method: str, endpoint: str, query_params: dict = None, payload: dict = None) -> dict:
        if query_params:
            endpoint += '?' + '&'.join(f'{key}={value}' for key, value in query_params.items())
        resp = await self.client.request(method, endpoint, json=payload)
        await resp.aread()
        return resp.json()
