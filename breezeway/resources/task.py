from datetime import time, date
from typing import TypedDict, Unpack, Literal

from httpx import Request

from .base import BaseResource, DateRange
from ..models.task import Department, Priority, RateType, Requester

class TaskDict(TypedDict, total=False):
    name: str
    type_department: Department
    type_priority: Priority
    description: str
    template_id: int
    schedule_date: date
    schedule_time: time
    assignments: list[int]
    tags: list[int]
    subdepartment_id: int
    rate_paid: float
    rate_type: RateType
    requested_by: Requester

class TaskCreateDict(TaskDict, total=False):
    home_id: int
    reference_property_id: int
    assign_default_workers: bool

class TaskListDict(TypedDict, total=False):
    home_id: int
    reference_property_id: int
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



class TaskResource(BaseResource):

    def add_comment(self, *, task_id: int, user_id: int, content: str) -> Request:
        """
        Add a comment to a task as a specific user.
        """
        endpoint = f'/public/inventory/v1/task/{task_id}/comments'
        return self._build_request('POST', endpoint, payload={'company_people_id': user_id, 'comment': content})

    def approve_task(self, *, task_id: int) -> Request:
        """
        Approve a task.
        """
        endpoint = f'/public/inventory/v1/task/{task_id}/approve'
        return self._build_request('POST', endpoint)

    def close_task(self, *, task_id: int) -> Request:
        """
        Close a task.
        """
        endpoint = f'/public/inventory/v1/task/{task_id}/close'
        return self._build_request('POST', endpoint)

    def create_task(self, **kwargs: Unpack[TaskCreateDict]) -> Request:
        """
        Create a new task.
        """
        endpoint = '/public/inventory/v1/task'
        return self._build_request('POST', endpoint, payload=kwargs)

    def delete_task(self, *, task_id: int) -> Request:
        """
        Mark a task as deleted.
        """
        endpoint = f'/public/inventory/v1/task/{task_id}'
        return self._build_request('DELETE', endpoint)

    def list_tasks(self, **kwargs: Unpack[TaskListDict]) -> Request:
        """
        Get a paginated list of tasks.
        Company ID is required for clients with multi-company access.
        """
        endpoint = '/public/inventory/v1/task'
        return self._build_request('GET', endpoint, params=kwargs)

    def reopen_task(self, *, task_id: int) -> Request:
        """
        Reopen a closed task.
        """
        endpoint = f'/public/inventory/v1/task/{task_id}/reopen'
        return self._build_request('POST', endpoint)

    def retrieve_task(self, task_id: int) -> Request:
        """
        Retrieve a specific task by ID.
        """
        endpoint = f'/public/inventory/v1/task/{task_id}'
        return self._build_request('GET', endpoint)

    def retrieve_task_comments(self, task_id: int) -> Request:
        """
        Retrieve comments for a specific task by ID.
        """
        endpoint = f'/public/inventory/v1/task/{task_id}/comments'
        return self._build_request('GET', endpoint)

    def update_task(self, *, task_id: int, **kwargs: Unpack[TaskDict]) -> Request:
        """
        Update an existing task.
        """
        endpoint = f'/public/inventory/v1/task/{task_id}'
        return self._build_request('PATCH', endpoint, payload=kwargs)

    def upload_attachment(
            self, *,
            task_id: int,
            file_name: str,
            file_bytes: bytes,
            include_in_report: bool
    ) -> Request:
        """
        Upload an attachment for a task.

        The file content must be provided as bytes so this method performs no
        file-system I/O and can be used safely from both sync and async clients.
        """
        endpoint = f'/public/inventory/v1/task/{task_id}/photos'
        file = {'file': (file_name, file_bytes)}
        return self._build_request('POST', endpoint, files=file, payload={'include_in_report': include_in_report})
