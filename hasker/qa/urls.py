from django.conf import settings
print(settings.INSTALLED_APPS)

from django.urls import path

from hasker.qa import views

app_name = "qa"
urlpatterns = [
    path("", view=views.TopQuestionsView.as_view(), name="home"),
    path("search/", view=views.SearchView.as_view(), name="search"),
    path("ask/", view=views.AskView.as_view(), name="ask"),
    path("vote/", view=views.VoteView.as_view(), name="vote"),
    path("question/<slug:pk>/", view=views.CreateAnswerView.as_view(), name="question"),
    path("accept/", view=views.AcceptAnswerView.as_view(), name="accept"),
]
