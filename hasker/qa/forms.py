from django import forms

from hasker.qa.models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['header','body','tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs.update({'id': 'slim-select'})

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = 'Your answer'
