from typing import Any, Sequence

from factory import Faker, post_generation
from factory.django import DjangoModelFactory
from hasker.qa.models import Question


class QuestionFactory(DjangoModelFactory):

    header = Faker("The most important question in the Universe")
    body = Faker("Do you know the answer?")
    author = Faker("sasha")

    class Meta:
        model = Question