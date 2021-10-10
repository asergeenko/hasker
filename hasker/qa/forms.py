from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_str
#from django.forms.utils import flatatt
from hasker.qa.models import Tag, Question, Answer
from django.template import loader



class CommaTags(forms.Widget):
    #def render(self, name, value, attrs=None, renderer=None):
        #context = self.get_context(name, value, attrs)
        #template = loader.get_template(self.template_name).render(context)
        #return mark_safe(template)
    def get_context(self, name, value, attrs):
        context = super().get_context(name,value,attrs)
        print (context)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['header','body','tags']
        #exclude = ['author','date_created','votes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['tags'].widget.choices = []#Tag.objects.none()
        self.fields['tags'].widget.attrs.update({'id': 'slim-select'})

        #fields = ('header','body','tags')
        #tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
        #tags.widget.attrs['data-role'] = "tagsinput"# = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), attrs={'data-role':"tagsinput"})

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = 'Your answer'
