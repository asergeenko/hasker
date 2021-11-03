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
from hasker.qa.views import (
    AskView,
    CreateAnswerView,
    SearchView,
    AjaxVoteView
)

User = get_user_model()

pytestmark = pytest.mark.django_db

class TestAskView:
    @classmethod
    def setup_class(cls):
        cls.question = {'header':'Test question header', 'body':'Test question body'}


    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_ask_form(self):
        form = QuestionForm(self.question)
        assert form.is_valid()

    def test_ask_request(self,client):
        client.force_login(User.objects.get_or_create(username='user1')[0])
        response = client.post("/ask", self.question, follow=True)
        assert response.status_code == 200


class TestAnswerView:
    @classmethod
    def setup_class(cls):
        cls.question = {'header':'Test question header', 'body':'Test question body','pk':9}
        cls.answer = {'body': "42"}
        cls.answer_view = CreateAnswerView()
        cls.answer_view.kwargs = {'pk': cls.question['pk']}        
        cls.answer_form = AnswerForm(cls.answer)

    def dummy_get_response(self, request: HttpRequest):
        return None


    def test_valid_data(self, user: User, rf: RequestFactory):
       
        request = rf.get("/fake-url/")

        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        self.answer_view.request = request
        
        response = self.answer_view.form_valid(self.answer_form)
        assert self.answer_form.is_valid()
        answer = self.answer_form.save()
        assert answer.body == self.answer["body"]
        assert answer.question.id == int(self.answer_view.kwargs['pk'])

class TestSearchView:

    @classmethod
    def setup_class(cls):
        cls.body = "Test question body"

    def dummy_get_response(self, request: HttpRequest):
        return None


    def test_valid_search(self, user: User, rf: RequestFactory):
        request = rf.get("/search/?q=test")

        response = SearchView.as_view()(request)
        assert response.context_data['object_list'][0].body == self.body


class TestVoteView:

    @classmethod
    def setup_class(cls):
        cls.success = {'success':True,'rating':1}

    def dummy_get_response(self, request: HttpRequest):
        return None


    def test_vote(self, user: User, rf: RequestFactory):
        view = AjaxVoteView()
        request = rf.post("/vote/", {'is_answ':0,'pk':9,'val':1,'unvote':'false','user':user.pk}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user
        response = AjaxVoteView.as_view()(request)
        assert json.loads(str(response.content,encoding='utf-8')) == self.success
