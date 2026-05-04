from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Entity, AsyncEntity
    from breezeway.models.unit import Unit, UnitPhoto, UnitTag


class UnitEntity(Entity[Unit]):

    def add_tag(self, tag: UnitTag) -> list[UnitTag]:
        """
        Add a tag to the unit.
        """
        return self.add_tags([tag])

    def add_tags(self, tags: list[UnitTag]) -> list[UnitTag]:
        """
        Add tags to the unit.
        """
        return self._client.unit.tag.add(unit_id=self.model.id, tags=[tag.id for tag in tags])

    def delete_tag(self, tag: UnitTag) -> list[UnitTag]:
        """
        Delete a tag from the unit.
        """
        return self.delete_tags([tag])

    def delete_tags(self, tags: list[UnitTag]) -> list[UnitTag]:
        """
        Delete tags from the unit.
        """
        return self._client.unit.tag.delete(unit_id=self.model.id, tag_ids=[tag.id for tag in tags])

    def set_tags(self, tags: list[UnitTag]) -> list[UnitTag]:
        """
        Set tags of the unit.
        """
        return self._client.unit.tag.set(unit_id=self.model.id, tags=[tag.id for tag in tags])

    def update(self) -> None:
        return self._client.unit.update(self.model.id, self.model)

    def update_default_photo(self, photo: UnitPhoto) -> UnitPhoto:
        """
        Set a default photo for a unit.
        """
        return self._client.unit.update_default_photo(unit_id=self.model.id, photo_id=photo.id)

    def update_room_count(self, num_bedrooms: int, num_bathrooms: int):
        """
        Add (and only add) bedrooms and/or bathrooms to a unit
        """
        return self._client.unit.update_room_count(unit_id=self.model.id, num_bedrooms=num_bedrooms, num_bathrooms=num_bathrooms)


class AsyncUnitEntity(AsyncEntity[Unit]):

    async def add_tag(self, tag: UnitTag) -> list[UnitTag]:
        """
        Add a tag to the unit.
        """
        return await self.add_tags([tag])

    async def add_tags(self, tags: list[UnitTag]) -> list[UnitTag]:
        """
        Add tags to the unit.
        """
        return await self._client.unit.tag.add(unit_id=self.model.id, tags=[tag.id for tag in tags])

    async def delete_tag(self, tag: UnitTag) -> list[UnitTag]:
        """
        Delete a tag from the unit.
        """
        return await self.delete_tags([tag])

    async def delete_tags(self, tags: list[UnitTag]) -> list[UnitTag]:
        """
        Delete tags from the unit.
        """
        return await self._client.unit.tag.delete(unit_id=self.model.id, tag_ids=[tag.id for tag in tags])

    async def set_tags(self, tags: list[UnitTag]) -> list[UnitTag]:
        """
        Set tags of the unit.
        """
        return await self._client.unit.tag.set(unit_id=self.model.id, tags=[tag.id for tag in tags])

    async def update(self) -> None:
        return await self._client.unit.update(self.model.id, self.model)

    async def update_default_photo(self, photo: UnitPhoto) -> UnitPhoto:
        """
        Set a default photo for a unit.
        """
        return await self._client.unit.update_default_photo(unit_id=self.model.id, photo_id=photo.id)

    async def update_room_count(self, num_bedrooms: int, num_bathrooms: int):
        """
        Add (and only add) bedrooms and/or bathrooms to a unit
        """
        return await self._client.unit.update_room_count(unit_id=self.model.id, num_bedrooms=num_bedrooms, num_bathrooms=num_bathrooms)
