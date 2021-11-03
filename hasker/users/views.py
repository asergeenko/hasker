from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView,View
from django.views.generic.edit import CreateView
from django.contrib.auth import logout
from django.shortcuts import redirect,render
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserCreationForm


User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = "user_detail.html"
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "user_form.html"
    model = User
    fields = ["email","avatar"]
    success_message = "Information successfully updated"

    def get_success_url(self):
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class AccountLogoutView(LoginRequiredMixin,LogoutView):
    template_name = "logout.html"

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return redirect('users:account_login')

class AccountLoginView(LoginView):
    template_name = "login.html"

class AccountSignupView(SuccessMessageMixin, CreateView):
    template_name = "signup.html"
    success_url = reverse_lazy('users:account_login')
    form_class = UserCreationForm
    success_message = "Your profile was created successfully"


user_signup_view = AccountSignupView.as_view()