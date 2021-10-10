import json

import logging
from smtplib import SMTPException


# Get an instance of a logger
logger = logging.getLogger(__name__)


from django.shortcuts import render
from hasker.qa.models import Question,Answer,VoteAnswer,VoteQuestion,vote, accept_answer, get_questions_with_stats
from django.views.generic import ListView, View, CreateView
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Sum, F, Count, Case, When, BooleanField, Exists,Max, OuterRef
from django.shortcuts import get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import send_mail

from django.http import JsonResponse

from django.db.models.functions import Coalesce

from hasker.qa.forms import QuestionForm,AnswerForm


class SearchView(ListView):
    template_name = 'qa/search_results.html'
    model = Question
    paginate_by = 20


    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        if q.startswith('tag:'):
            tag = q[len('tag:'):]
            self.results = get_questions_with_stats(Question.objects.filter(tags__word=tag))
        else:
            self.results = get_questions_with_stats(Question.objects.filter(Q(header__icontains=q)|Q(body__icontains=q)))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.results, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        context['object_list'] = object_list
        return context

class AskView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "qa/ask_form.html"
    form_class = QuestionForm
    success_message = "Your question was added successfully"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView,self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('qa:question',args=(self.object.id,))

class CreateAnswerView(FormMixin, ListView, LoginRequiredMixin, SuccessMessageMixin):
    template_name = 'qa/create_answer_form.html'
    paginate_by = 30
    form_class = AnswerForm

    def get_queryset(self):
        qs = Answer.objects.filter(question=self.kwargs['pk'])\
                           .annotate(total_score=Coalesce(Sum('voteanswer__value'),0))

        if self.request.user.is_authenticated:
            qs = qs.annotate(voted_by_user=Sum('voteanswer__value', filter=Q(voteanswer__author=self.request.user)))

        qs = qs.order_by('-total_score', '-date_created')

        return qs

    def form_valid(self, form):
        form.instance.author = self.request.user
        question = get_object_or_404(Question,pk=self.kwargs['pk'])
        form.instance.question = question
        form.save()

        try:
            send_mail(
                'New answer on "%s"'%(question.header),
                'Hello, %s.\nThere is a new answer on your question "%s". You can check it here: %s.\n\nRegards,\nHasker Team'%(question.author,
                question.header,self.request.build_absolute_uri(reverse('qa:question', kwargs={'pk':question.pk}))),
                'Hue from Hasker <hasker@hasker.com>',
                [question.author.email],
                fail_silently=False,
            )
        except SMTPException as e:
            logger.exception('There was an error sending an email')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = Question.objects.annotate(total_score=Coalesce(Sum('votequestion__value'),0))

        if self.request.user.is_authenticated:
            question = question.annotate(voted_by_user=Sum('votequestion__value', filter=Q(votequestion__author=self.request.user)))

        question = question.get(pk=self.kwargs['pk'])

        context['question'] = question

        return context

    def get_success_url(self):
        return reverse_lazy('qa:question',args=(self.kwargs['pk'],))

    def post(self, request, *args, **kwargs):

       # self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class VoteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            # Добавить проверки полей
            pk = self.request.POST.get('pk')
            params = {}
            params['post_id'] = pk
            params['value'] = self.request.POST.get('val')
            params['author_id'] = self.request.POST.get('user')
            is_unvote = json.loads(self.request.POST.get('unvote'))

            vote_model = VoteAnswer if int(self.request.POST.get('is_answ')) else VoteQuestion

            result, rating = vote(vote_model, is_unvote=is_unvote, **params)

            return JsonResponse({'success':result,'rating':rating})

class AcceptAnswerView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            # Добавить проверки полей
            pk = self.request.POST.get('pk')
            is_accept = int(self.request.POST.get('is_accept'))
            result = True
            accepted = False

            result = accept_answer(pk, is_accept)

            return JsonResponse({'success':result})

class TopQuestionsView(ListView):
    template_name = 'qa/top_questions.html'
    model = Question
    paginate_by = 20


    def get(self, request, *args, **kwargs):

        self.results = get_questions_with_stats(Question.objects)
                            #.order_by('-total_score')[:5]

        hot = int(request.GET.get('hot', 0))

        if hot:
            self.results = self.results.order_by('-total_score')
        else:
            self.results = self.results.order_by('-date_created')

        self.hot = hot


        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.results, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)

        context['questions'] = questions
        context['hot'] = self.hot
        return context
