from django.db import models
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from django.db.models import Sum,Exists,Count, OuterRef
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.db import transaction

User = get_user_model()

class Tag(models.Model):
    word = models.CharField(max_length=55)

    def __str__(self):
        return self.word

    #class Meta:
    #    app_label = 'hasker.qa'


class AbstractPost(models.Model):
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Question(AbstractPost):
    header = models.CharField(max_length=500, verbose_name='Title')
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True)
    votes = models.ManyToManyField(User, through='VoteQuestion',related_name='questions_votes')

    def __str__(self):
        return self.header



class Answer(AbstractPost):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    votes = models.ManyToManyField(User, through='VoteAnswer',related_name='answers_votes')


    def __str__(self):
        return self.body

    class Meta:
        ordering = ('date_created',)

class AbstractVote(models.Model):
    value = models.SmallIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True

class VoteQuestion(AbstractVote):
    post = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['author','post']

    def __str__(self):
        return "%s - %s %d"%(self.author, self.post, self.value)

class VoteAnswer(AbstractVote):
    post = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['author','post']

    def __str__(self):
        return "%s - %s %d"%(self.author, self.post, self.value)

def vote(vote_model, is_unvote, **kwargs):
    result = True
    if is_unvote:
        vote_model.objects.filter(post_id = kwargs['post_id'], author_id=kwargs['author_id']).delete()
    else:
        try:
            with transaction.atomic():
                vote_model.objects.create(**kwargs)
        except IntegrityError:
            result = False

    return result, vote_model.objects.filter(post_id=kwargs['post_id']).aggregate(Sum('value'))['value__sum'] or 0

def accept_answer(pk, is_accept):
    result = True
    try:
        answer = get_object_or_404(Answer, pk=pk)
        answer.is_accepted = not answer.is_accepted
        answer.save()

        if is_accept:
            other_answers = Answer.objects.filter(question=answer.question, is_accepted=True).exclude(pk=answer.pk).update(is_accepted=True)
    except:
        result = False

    return result

def get_questions_with_stats(qs):
    # Ugly "num_answers" annotation goes from https://stackoverflow.com/questions/43770118/simple-subquery-with-outerref
    return qs.annotate(total_score=Coalesce(Sum('votequestion__value'), 0)) \
        .annotate(is_accepted=Exists(Answer.objects.filter(question=OuterRef('pk'), is_accepted=True))) \
        .annotate(num_answers=Coalesce(
        Answer.objects.filter(question=OuterRef('pk')).values('question').annotate(count=Count('question')).values(
            'count'), 0))
