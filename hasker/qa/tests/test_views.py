import pytest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import RequestFactory
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

#from hasker.users.forms import UserChangeForm
from hasker.qa.models import Question
from hasker.qa.forms import QuestionForm, AnswerForm
from hasker.qa.tests.factories import QuestionFactory
from hasker.qa.views import (
    AskView,
    CreateAnswerView
)

User = get_user_model()

pytestmark = pytest.mark.django_db

class TestAskView:

    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_form_valid(self, user: User, rf: RequestFactory):
        view = AskView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        view.request = request

        form = QuestionForm({'header':'Test question header', 'body':'Test question body'})
        form.cleaned_data = []
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == ["Your question was added successfully"]


class TestAnswerView:

    def dummy_get_response(self, request: HttpRequest):
        return None


    def test_valid_data(self, user: User, rf: RequestFactory):
        view = CreateAnswerView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        view.request = request
        view.kwargs = {'pk': 9}


        form = AnswerForm({
            'body': "42",
        })
        view.form_valid(form)
        answer = form.save()
        assert answer.body == "42"
        assert answer.question.id == int(view.kwargs['pk'])