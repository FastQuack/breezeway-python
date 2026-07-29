import asyncio
from pathlib import Path
from typing import TYPE_CHECKING, Never

from typing_extensions import overload

from breezeway.clients.task.comments import CommentClient, AsyncCommentClient
from breezeway.models.base import Paginated
from breezeway.models.task import Task, TaskAttachment

if TYPE_CHECKING:
    from breezeway.breezeway import BreezewayClient, AsyncBreezewayClient
    from typing import Unpack
    from breezeway.resources.task import TaskCreateDict, TaskListDict, TaskDict


class TaskClient:
    def __init__(self, client: BreezewayClient):
        self._client = client
        self.comments = CommentClient(client)

    def approve(self, task_id: int) -> None:
        """
        Approve a task
        """
        request = self._client.resource.task.approve_task(task_id=task_id)
        self._client.process_request(request)

    def close(self, task_id: int) -> Task:
        """
        Close a task
        """
        request = self._client.resource.task.close_task(task_id=task_id)
        task = self._client.process_request(request)
        return Task.model_validate(task)

    def create(self, **kwargs: Unpack[TaskCreateDict]) -> Task:
        """
        Create a task
        """
        request = self._client.resource.task.create_task(**kwargs)
        task = self._client.process_request(request)
        return Task.model_validate(task)

    def delete(self, task_id: int) -> None:
        """
        Mark a task as deleted
        """
        request = self._client.resource.task.delete_task(task_id=task_id)
        self._client.process_request(request)

    def list_page(self, **kwargs: Unpack[TaskListDict]) -> Paginated[Task]:
        """
        List tasks for a unit.
        When retrieving multiple tasks, include either home_id or reference_property_id
        """
        request = self._client.resource.task.list_tasks(**kwargs)
        page = self._client.process_request(request)
        return Paginated[Task].model_validate(page)


    def list_all(self, **kwargs: Unpack[TaskListDict]) -> list[Task]:
        """
        List all tasks for a unit.
        When retrieving multiple tasks, include either home_id or reference_property_id
        """
        paginated_tasks = self.list_page(**kwargs)
        tasks = paginated_tasks.results
        for page in range(2, paginated_tasks.total_pages + 1):
            tasks += self.list_page(page=page, **kwargs).results
        return tasks


    def get(self, task_id: int) -> Task:
        """
        Retrieve a task
        """
        request = self._client.resource.task.retrieve_task(task_id=task_id)
        task = self._client.process_request(request)
        return Task.model_validate(task)

    def update(self, task_id: int, **kwargs: Unpack[TaskDict]) -> Task:
        """
        Update a task
        """
        request = self._client.resource.task.update_task(task_id=task_id, **kwargs)
        task = self._client.process_request(request)
        return Task.model_validate(task)

    @overload
    def upload_attachment(self, *, task_id: int, file_path: Never = ..., file_name: Never = ..., file_bytes: bytes, include_in_report: bool = True) -> TaskAttachment: ...

    @overload
    def upload_attachment(self, *, task_id: int, file_path: str, file_name: str, file_bytes: Never = ..., include_in_report: bool = True) -> TaskAttachment: ...

    def upload_attachment(
            self, *,
            task_id: int,
            file_path: str | None = None,
            file_name: str | None = None,
            file_bytes: bytes | None = None,
            include_in_report: bool = True
    ) -> TaskAttachment:
        """
        Upload an attachment to a task
        """
        if file_path:
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
            file_name = file_path.split('/')[-1] or ''
        request = self._client.resource.task.upload_attachment(
            task_id=task_id,
            file_name=file_name,
            file_bytes=file_bytes,
            include_in_report=include_in_report
        )
        photo = self._client.process_request(request)
        return TaskAttachment.model_validate(photo)

class AsyncTaskClient:
    def __init__(self, client: AsyncBreezewayClient):
        self._client = client
        self.comments = AsyncCommentClient(client)

    async def approve(self, task_id: int) -> None:
        """
        Approve a task
        """
        request = await self._client.resource.task.approve_task(task_id=task_id)
        await self._client.process_request(request)

    async def close(self, task_id: int) -> Task:
        """
        Close a task
        """
        request = self._client.resource.task.close_task(task_id=task_id)
        task = await self._client.process_request(request)
        return Task.model_validate(task)

    async def create(self, **kwargs: Unpack[TaskCreateDict]) -> Task:
        """
        Create a task
        """
        request = self._client.resource.task.create_task(**kwargs)
        task = await self._client.process_request(request)
        return Task.model_validate(task)

    async def delete(self, task_id: int) -> None:
        """
        Mark a task as deleted
        """
        request = self._client.resource.task.delete_task(task_id=task_id)
        await self._client.process_request(request)

    async def list_page(self, **kwargs: Unpack[TaskListDict]) -> Paginated[Task]:
        """
        List tasks for a unit.
        When retrieving multiple tasks, include either home_id or reference_property_id
        """
        request = self._client.resource.task.list_tasks(**kwargs)
        page = await self._client.process_request(request)
        return Paginated[Task].model_validate(page)


    async def list_all(self, **kwargs: Unpack[TaskListDict]) -> list[Task]:
        """
        List all tasks for a unit.
        When retrieving multiple tasks, include either home_id or reference_property_id
        """
        paginated_tasks = await self.list_page(**kwargs)
        tasks = paginated_tasks.results
        if paginated_tasks.total_pages == 1:
            return tasks
        async_tasks = [self.list_page(page=page, **kwargs) for page in range(2, paginated_tasks.total_pages + 1)]
        remaining_pages = await asyncio.gather(*async_tasks)
        for page in remaining_pages:
            tasks += page.results
        return tasks

    async def get(self, task_id: int) -> Task:
        """
        Retrieve a task
        """
        request = self._client.resource.task.retrieve_task(task_id=task_id)
        task = await self._client.process_request(request)
        return Task.model_validate(task)

    async def update(self, task_id: int, **kwargs: Unpack[TaskDict]) -> Task:
        """
        Update a task
        """
        request = self._client.resource.task.update_task(task_id=task_id, **kwargs)
        task = await self._client.process_request(request)
        return Task.model_validate(task)

    @overload
    async def upload_attachment(self, *, task_id: int, file_path: Never = ..., file_name: Never = ..., file_bytes: bytes, include_in_report: bool = True) -> TaskAttachment: ...

    @overload
    async def upload_attachment(self, *, task_id: int, file_path: str, file_name: str, file_bytes: Never = ..., include_in_report: bool = True) -> TaskAttachment: ...

    async def upload_attachment(
            self, *,
            task_id: int,
            file_path: str | None = None,
            file_name: str | None = None,
            file_bytes: bytes | None = None,
            include_in_report: bool = True
    ) -> TaskAttachment:
        """
        Upload an attachment to a task
        """
        if file_path:
            file_name = file_path.split('/')[-1] or ''
            file_path = Path(file_path)
            file_bytes = await asyncio.to_thread(file_path.read_bytes)
        request = self._client.resource.task.upload_attachment(
            task_id=task_id,
            file_name=file_name,
            file_bytes=file_bytes,
            include_in_report=include_in_report
        )
        photo = await self._client.process_request(request)
        return TaskAttachment.model_validate(photo)
