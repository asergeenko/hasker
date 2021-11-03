from django.urls import path

from hasker.users.views import (
    user_detail_view,
    user_update_view,
)
from hasker.users.views import AccountLogoutView, AccountLoginView,AccountSignupView


app_name = "users"
urlpatterns = [
    path("~logout/",AccountLogoutView.as_view(),name="account_logout"),
    path("~login/",AccountLoginView.as_view(), name="account_login"),
    path("~signup/",AccountSignupView.as_view(),name="account_signup"),

    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

]
