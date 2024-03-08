from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.orm import Session


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    @classmethod
    def set_session(cls, session: Session) -> None:
        if cls is BaseFactory:
            for factory in cls.__subclasses__():
                factory.set_session(session)
        else:
            cls._meta.sqlalchemy_session = session

    @classmethod
    def get_current_session(cls) -> Session:
        return cls._meta.sqlalchemy_session
