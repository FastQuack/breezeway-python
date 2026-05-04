from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from breezeway.breezeway import Breezeway, AsyncBreezeway
    from breezeway.models.base import BaseBreezewayModel


class Entity[T: BaseBreezewayModel]:
    _client: Breezeway | None = None

    def __init__(self, model: T):
        if Entity._client is None:
            raise RuntimeError("Not configured")
        self.model: T = model

    @classmethod
    def configure(cls, client: Breezeway):
        if cls._client is not None:
            raise RuntimeError("Already configured")
        cls._client = client


class AsyncEntity[T: BaseBreezewayModel]:
    _client: AsyncBreezeway

    def __init__(self, model: T):
        self.model: T = model

    @classmethod
    def configure(cls, client: AsyncBreezeway):
        if cls._client is not None:
            raise RuntimeError("Already configured")
        cls._client = client
