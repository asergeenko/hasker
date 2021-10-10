from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, RedirectView, UpdateView,View
from django.views.generic.edit import CreateView
from django.contrib.auth import logout,login
from django.shortcuts import redirect,render


from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserCreationForm
#from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["email","avatar"]
    success_message = "Information successfully updated"

    def get_success_url(self):
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


#class UserRedirectView(LoginRequiredMixin, RedirectView):

#    permanent = False

    #def get_redirect_url(self):
    #    return reverse("users:detail", kwargs={"username": self.request.user.username})

#user_redirect_view = UserRedirectView.as_view()

class AccountLogoutView(LoginRequiredMixin,LogoutView):#(,View):
    template_name = "account/logout.html"

    def post(self, *args, **kwargs):
        #url = self.request.path_info#self.get_redirect_url()
        if self.request.user.is_authenticated:
            logout(self.request)
        return redirect('qa:home')

class AccountLoginView(LoginView):
    template_name = "account/login.html"

class AccountSignupView(SuccessMessageMixin, CreateView):
    template_name = "account/signup.html"
    success_url = reverse_lazy('account_login')
    form_class = UserCreationForm
    success_message = "Your profile was created successfully"


user_signup_view = AccountSignupView.as_view()

class AccountResetPasswordView(LoginRequiredMixin,View):
    template_name = "account/password_reset.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        #url = self.request.path_info  # self.get_redirect_url()
        #if not self.request.user.is_authenticated:
        #    login(self.request)
        return redirect('qa:home')

