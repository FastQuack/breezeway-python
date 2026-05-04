from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BaseBreezewayModel(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True
    )


class Paginated[T: BaseBreezewayModel](BaseBreezewayModel):
    limit: int
    page: int
    results: list[T]
    total_pages: int
    total_results: int
