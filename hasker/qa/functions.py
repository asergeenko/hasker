from django.db import IntegrityError
from django.db import transaction
from django.db.models import Sum,Exists,Count, OuterRef
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404

from hasker.qa.models import Answer 

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
            Answer.objects.filter(question=answer.question, is_accepted=True).exclude(pk=answer.pk).update(is_accepted=True)
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
