from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    word = models.CharField(max_length=55)

    def __str__(self):
        return self.word


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