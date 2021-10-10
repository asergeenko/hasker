from django.contrib import admin

from hasker.qa import models

admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Tag)
admin.site.register(models.VoteQuestion)
admin.site.register(models.VoteAnswer)



