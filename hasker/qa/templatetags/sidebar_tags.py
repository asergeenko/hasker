from django.db.models.functions import Coalesce
from django.db.models import Sum, Exists,OuterRef
from django import template

from hasker.qa.models import Question,Answer

register = template.Library()

@register.inclusion_tag('qa/trending.html')
def trending_tag():
    return {'trending': Question.objects.annotate(total_score=Coalesce(Sum('votequestion__value'),0))\
                            .annotate(is_accepted=Exists(Answer.objects.filter(question=OuterRef('pk'), is_accepted=True)))\
                            .order_by('-total_score')[:5]}
