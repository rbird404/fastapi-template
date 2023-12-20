from abc import abstractmethod

from src.database import AsyncDbSession


class BaseAsyncUseCase:
    def __init__(self, session: AsyncDbSession):
        self._session = session

    @property
    def session(self):
        return self._session

    @abstractmethod
    async def __call__(self, *args, **kwargs):
        ...
