import pytest
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import RequestFactory
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from hasker.qa.models import Question
from hasker.qa.forms import QuestionForm, AnswerForm
from hasker.qa.tests.factories import QuestionFactory
from hasker.qa.views import (
    AskView,
    CreateAnswerView,
    SearchView,
    VoteView
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

class TestSearchView:

    def dummy_get_response(self, request: HttpRequest):
        return None


    def test_valid_search(self, user: User, rf: RequestFactory):
        request = rf.get("/search/?q=test")

        response = SearchView.as_view()(request)
        assert response.context_data['object_list'][0].body == "Test question body"


class TestVoteView:

    def dummy_get_response(self, request: HttpRequest):
        return None


    def test_vote(self, user: User, rf: RequestFactory):
        view = VoteView()
        request = rf.post("/vote/", {'is_answ':0,'pk':9,'val':1,'unvote':'false','user':user.pk}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user
        response = VoteView.as_view()(request)
        assert json.loads(str(response.content,encoding='utf-8')) == {'success':True,'rating':1}
