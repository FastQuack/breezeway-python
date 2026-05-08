from typing import TYPE_CHECKING

import asyncio

from .tag import UnitTagClient, AsyncUnitTagClient
from breezeway.models.base import Paginated
from breezeway.models.unit import Unit, UnitPhoto

if TYPE_CHECKING:
    from typing import Unpack
    from breezeway.breezeway import BreezewayClient, AsyncBreezewayClient
    from breezeway.resources.base import ListAllDict, ListDict
    from breezeway.resources.unit import UnitDict


class UnitClient:
    def __init__(self, client: BreezewayClient):
        self._client = client
        self.tag = UnitTagClient(client)

    def list_all(self, **kwargs: Unpack[ListAllDict]) -> list[Unit]:
        """
        Get a list of all units.
        Company ID is required for clients with multi-company access.
        """
        paginated_units = self.list_page(**kwargs)
        units = paginated_units.results
        for page in range(2, paginated_units.total_pages + 1):
            units += self.list_page(page=page, **kwargs).results
        return units

    def create(self, **kwargs: Unpack[UnitDict]) -> Unit:
        """
        Create a new unit.
        Company ID is required for clients with multi-company access.
        """
        request = self._client.resource.unit.create_unit(**kwargs)
        data = self._client.process_request(request)
        return Unit.model_validate(data)

    def get(self, *, unit_id: int) -> Unit:
        """
        Retrieve a unit by its Breezeway ID.
        """
        request = self._client.resource.unit.retrieve_unit(unit_id=unit_id)
        data = self._client.process_request(request)
        return Unit.model_validate(data)

    def list_page(self, **kwargs: Unpack[ListDict]) -> Paginated[Unit]:
        """
        Get a paginated list of units.
        Company ID is required for clients with multi-company access.
        """
        request = self._client.resource.unit.list_units(**kwargs)
        data = self._client.process_request(request)
        return Paginated[Unit].model_validate(data)

    def update(self, *, unit_id: int, unit: Unpack[UnitDict]) -> None:
        request = self._client.resource.unit.update_unit(unit_id=unit_id, unit=unit)
        self._client.process_request(request)

    def update_default_photo(self, *, unit_id: int, photo_id: int) -> UnitPhoto:
        """
        Set a default photo for a unit.
        """
        request = self._client.resource.unit.update_default_photo(unit_id=unit_id, photo_id=photo_id)
        photo = self._client.process_request(request)
        return UnitPhoto.model_validate(photo)

    def update_room_count(self, *, unit_id, num_bedrooms: int, num_bathrooms: int) -> None:
        """
        Add (and only add) bedrooms and/or bathrooms to a unit
        """
        request = self._client.resource.unit.set_room_count(unit_id=unit_id, num_bedrooms=num_bedrooms, num_bathrooms=num_bathrooms)
        self._client.process_request(request)


class AsyncUnitClient:
    def __init__(self, client: AsyncBreezewayClient):
        self._client = client
        self.tag = AsyncUnitTagClient(client)

    async def list_all(self, **kwargs: Unpack[ListAllDict]) -> list[Unit]:
        """
        Get a list of all units.
        Company ID is required for clients with multi-company access.
        """
        paginated_units = await self.list_page(**kwargs)
        units = paginated_units.results
        if paginated_units.total_pages == 1:
            return units
        tasks = [self.list_page(page=page, **kwargs) for page in range(2, paginated_units.total_pages + 1)]
        remaining_pages = await asyncio.gather(*tasks)
        for page in remaining_pages:
            units += page.results
        return units

    async def create(self, **kwargs: Unpack[UnitDict]) -> Unit:
        """
        Create a new unit.
        Company ID is required for clients with multi-company access.
        """
        request = self._client.resource.unit.create_unit(**kwargs)
        data = await self._client.process_request(request)
        return Unit.model_validate(data)

    async def get(self, unit_id: int) -> Unit:
        """
        Retrieve a unit by its Breezeway ID.
        """
        request = self._client.resource.unit.retrieve_unit(unit_id=unit_id)
        data = await self._client.process_request(request)
        return Unit.model_validate(data)

    async def list_page(self, **kwargs: Unpack[ListDict]) -> Paginated[Unit]:
        """
        Get a paginated list of units.
        Company ID is required for clients with multi-company access.
        """
        request = self._client.resource.unit.list_units(**kwargs)
        data = await self._client.process_request(request)
        return Paginated[Unit].model_validate(data)

    async def update(self, unit_id: int, unit: Unpack[UnitDict]) -> None:
        request = self._client.resource.unit.update_unit(unit_id=unit_id, unit=unit)
        await self._client.process_request(request)

    async def update_default_photo(self, *, unit_id: int, photo_id: int) -> UnitPhoto:
        """
        Set a default photo for a unit.
        """
        request = self._client.resource.unit.update_default_photo(unit_id=unit_id, photo_id=photo_id)
        photo = await self._client.process_request(request)
        return UnitPhoto.model_validate(photo)

    async def update_room_count(self, *, unit_id, num_bedrooms: int, num_bathrooms: int) -> None:
        """
        Add (and only add) bedrooms and/or bathrooms to a unit
        """
        request = self._client.resource.unit.set_room_count(unit_id=unit_id, num_bedrooms=num_bedrooms, num_bathrooms=num_bathrooms)
        await self._client.process_request(request)
