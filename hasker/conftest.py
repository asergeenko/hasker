import pytest

from hasker.users.models import User
from hasker.users.tests.factories import UserFactory

from hasker.qa.models import Question
from hasker.qa.tests.factories import QuestionFactory



@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def question() -> Question:
    return QuestionFactory()

