from typing import TYPE_CHECKING

from breezeway.models.unit import UnitTag

if TYPE_CHECKING:
    from breezeway.breezeway import BreezewayClient, AsyncBreezewayClient


class UnitTagClient:
    def __init__(self, client: BreezewayClient):
        self._client = client

    def add(self, *, unit_id: int, tag_ids: int | list[int]) -> list[UnitTag]:
        """
        Add tags to the unit.
        """
        if isinstance(tag_ids, int):
            tag_ids = [tag_ids]
        request = self._client.resource.unit.tag.add_tags(unit_id=unit_id, tag_ids=tag_ids)
        tags = self._client.process_request(request)
        return [UnitTag.model_validate(tag) for tag in tags]

    def delete(self, *, unit_id: int, tag_ids: int | list[int]) -> list[UnitTag]:
        """
        Delete tags from the unit.
        """
        if isinstance(tag_ids, int):
            tag_ids = [tag_ids]
        request = self._client.resource.unit.tag.delete_tags(unit_id=unit_id, tag_ids=[tag_ids])
        tags = self._client.process_request(request)
        return [UnitTag.model_validate(tag) for tag in tags]

    def get(self, *, unit_id: int) -> list[UnitTag]:
        """
        Get tags of the unit.
        """
        request = self._client.resource.unit.tag.get_tags(unit_id=unit_id)
        tags = self._client.process_request(request)
        return [UnitTag.model_validate(tag) for tag in tags]

    def set(self, *, unit_id: int, tag_ids: list[int]) -> list[UnitTag]:
        """
        Set tags of the unit.
        """
        request = self._client.resource.unit.tag.set_tags(unit_id=unit_id, tags=tag_ids)
        tags = self._client.process_request(request)
        return [UnitTag.model_validate(tag) for tag in tags]

    def list_all(self, *, company_id: int | None = None) -> list[UnitTag]:
        """
        List unit tags configured for a Breezeway company
        Creation of company tags must be performed within the app.
        Company ID is required for clients with multi-company access.
        """
        request = self._client.resource.unit.tag.list_unit_tags(company_id=company_id)
        tags = self._client.process_request(request)
        return [UnitTag.model_validate(tag) for tag in tags]


class AsyncUnitTagClient:
    def __init__(self, client: AsyncBreezewayClient):
        self._client = client

    async def add(self, *, unit_id: int, tag_ids: int | list[int]) -> list[UnitTag]:
        """
        Add tags to the unit.
        """
        if isinstance(tag_ids, int):
            tag_ids = [tag_ids]
        request = self._client.resource.unit.tag.add_tags(unit_id=unit_id, tag_ids=tag_ids)
        tags = await self._client.process_request(request)
        return [UnitTag.model_validate(tag) for tag in tags]

    async def delete(self, *, unit_id: int, tag_ids: int | list[int]) -> list[UnitTag]:
        """
        Delete tags from the unit.
        """
        if isinstance(tag_ids, int):
            tag_ids = [tag_ids]
        request = self._client.resource.unit.tag.delete_tags(unit_id=unit_id, tag_ids=[tag_ids])
        tags = await self._client.process_request(request)
        return [UnitTag.model_validate(tag) for tag in tags]

    async def get(self, *, unit_id: int) -> list[UnitTag]:
        """
        Get tags of the unit.
        """
        request = self._client.resource.unit.tag.get_tags(unit_id=unit_id)
        tags = await self._client.process_request(request)
        return [UnitTag.model_validate(tag) for tag in tags]

    async def set(self, *, unit_id: int, tag_ids: list[int]) -> list[UnitTag]:
        """
        Set tags of the unit.
        """
        request = self._client.resource.unit.tag.set_tags(unit_id=unit_id, tags=tag_ids)
        tags = await self._client.process_request(request)
        return [UnitTag.model_validate(tag) for tag in tags]

    async def list_all(self, *, company_id: int | None = None) -> list[UnitTag]:
        """
        List unit tags configured for a Breezeway company
        Creation of company tags must be performed within the app.
        Company ID is required for clients with multi-company access.
        """
        request = self._client.resource.unit.tag.list_unit_tags(company_id=company_id)
        tags = await self._client.process_request(request)
        return [UnitTag.model_validate(tag) for tag in tags]