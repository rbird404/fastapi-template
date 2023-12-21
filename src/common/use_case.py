from abc import abstractmethod, ABC
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.schemas import DefaultResponse
from src.database import AsyncDbSession


class BaseUseCase(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        ...


class BaseAsyncUseCase(BaseUseCase, ABC):
    def __init__(self, session: AsyncDbSession):
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session

    @abstractmethod
    async def __call__(self, *args, **kwargs) -> DefaultResponse:
        ...
