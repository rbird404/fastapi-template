import factory
from factory.fuzzy import FuzzyText

from src.auth.jwt import AccessToken
from src.users.models import User
from tests.factories.base import BaseFactory


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = FuzzyText(length=10)
    password = factory.Sequence(lambda x: bytes(x))

    @classmethod
    def get_credentials(cls, user: User):
        from src.auth.service import create_token
        return f"Bearer {create_token(AccessToken, user)}"
