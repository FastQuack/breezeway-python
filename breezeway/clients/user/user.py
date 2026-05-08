from typing import TYPE_CHECKING

from breezeway.models.user import User, UserStatus

if TYPE_CHECKING:
    from breezeway.breezeway import BreezewayClient, AsyncBreezewayClient

class UserClient:
    def __init__(self, client: BreezewayClient):
        self._client = client

    def list_all(self, user_status: UserStatus = UserStatus.ACTIVE) -> list[User]:
        """Get users associated with the client."""
        request = self._client.resource.user.list_users(status=user_status)
        users = self._client.process_request(request)
        return [User.model_validate(user) for user in users]

    def get(self, *, user_id: int) -> User:
        """Get a user by their ID."""
        request = self._client.resource.user.retrieve_user(user_id=user_id)
        user = self._client.process_request(request)
        return User.model_validate(user)


class AsyncUserClient:
    def __init__(self, client: AsyncBreezewayClient):
        self._client = client

    async     def list_all(self, user_status: UserStatus = UserStatus.ACTIVE) -> list[User]:
        """Get users associated with the client."""
        request = self._client.resource.user.list_users(status=user_status)
        users = await self._client.process_request(request)
        return [User.model_validate(user) for user in users]

    async def get(self, *, user_id: int) -> User:
        """Get a user by their ID."""
        request = self._client.resource.user.retrieve_user(user_id=user_id)
        user = await self._client.process_request(request)
        return User.model_validate(user)
