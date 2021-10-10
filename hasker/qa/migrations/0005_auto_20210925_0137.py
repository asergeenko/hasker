# Generated by Django 3.1 on 2021-09-24 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qa', '0004_auto_20210925_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='votes',
            field=models.ManyToManyField(related_name='answers_votes', through='qa.VoteAnswer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='votes',
            field=models.ManyToManyField(related_name='questions_votes', through='qa.VoteQuestion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='voteanswer',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa.answer'),
        ),
        migrations.AlterField(
            model_name='votequestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa.question'),
        ),
    ]
