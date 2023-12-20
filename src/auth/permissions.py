from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.requests import Request

from src.auth.jwt import AccessToken
from src.database import AsyncDbSession


class BasePermission(ABC):

    @abstractmethod
    async def has_required_permissions(self) -> bool:
        ...

    def __init__(self, request: Request, session: AsyncSession):
        self.user_id: int | None = None
        self._request = request
        self._session = session

        if bearer_token := request.headers.get("authorization"):
            token = AccessToken(bearer_token[7:])
            self.user_id = int(token['sub'])

    @property
    def session(self) -> AsyncSession:
        return self._session

    @property
    def request(self) -> Request:
        return self._request


class PermissionControl:
    def __init__(self, permissions_classes: tuple[Type[BasePermission]]):
        self.permissions_classes = permissions_classes

    async def __call__(self, request: Request, session: AsyncDbSession) -> None:
        for permission_class in self.permissions_classes:
            await permission_class(
                request=request, session=session
            ).has_required_permissions()
