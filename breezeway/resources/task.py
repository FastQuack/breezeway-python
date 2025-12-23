from typing import TypedDict, Unpack, Literal, Never

from httpx import Request

from .base import BaseResource, DateRange
from ..models.task import Department


class TaskCreateDict(TypedDict):
    pass


class BaseTaskListDict(TypedDict, total=False):
    type_department: Department
    scheduled_date: DateRange | str
    created_at: DateRange | str
    finished_at: DateRange | str
    updated_at: DateRange | str
    assignee_ids: list[int]
    limit: int
    page: int
    sort_by: str
    sort_order: Literal['asc', 'desc']
    reference_company_id: str  # required if using cross-company access


class TaskListWithHomeID(BaseTaskListDict):
    home_id: int
    reference_property_id: Never | None


class TaskListWithReferencePropertyID(BaseTaskListDict):
    reference_property_id: int
    home_id: Never | None


class TaskResource(BaseResource):
    def create_task(self, **kwargs: Unpack[TaskCreateDict]) -> Request:
        pass

    def list_tasks(self, **kwargs: Unpack[TaskListWithHomeID | TaskListWithReferencePropertyID]) -> Request:
        """
        Get a paginated list of tasks.
        Company ID is required for clients with multi-company access.
        """
        endpoint = 'public/inventory/v1/property'
        params = kwargs
        return self._build_request('GET', endpoint, params=params)

    def list_task_tags(self, company_id):
        pass

    def retrieve_task(self, unit_id: int) -> Request:
        pass