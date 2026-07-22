from typing import TYPE_CHECKING


from breezeway.models.task import Comment

if TYPE_CHECKING:
    from breezeway.breezeway import BreezewayClient, AsyncBreezewayClient
    from breezeway.models.task import Task
    from breezeway.models.user import User


class CommentClient:
    def __init__(self, client: BreezewayClient):
        self._client = client

    def add(self, *, task: Task, user: User, content: str) -> Comment:
        request = self._client.resource.task.add_comment(task_id=task.id, user_id=user.id, content=content)
        comment = self._client.process_request(request)
        return Comment.model_validate(comment)

    def list_all(self, * , task: Task) -> list[Comment]:
        request = self._client.resource.task.retrieve_task_comments(task_id=task.id)
        comments = self._client.process_request(request)
        return [Comment.model_validate(comment) for comment in comments]


class AsyncCommentClient:
    def __init__(self, client: AsyncBreezewayClient):
        self._client = client

    async def add(self, *, task: Task, user: User, content: str) -> Comment:
        request = self._client.resource.task.add_comment(task_id=task.id, user_id=user.id, content=content)
        comment = await self._client.process_request(request)
        return Comment.model_validate(comment)

    async def list_all(self, * , task: Task) -> list[Comment]:
        request = self._client.resource.task.list_comments(task_id=task.id)
        comments = await self._client.process_request(request)
        return [Comment.model_validate(comment) for comment in comments]
