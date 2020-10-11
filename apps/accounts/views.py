from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView

from .forms import ProfileForm, RegisterForm
from .models import Profile


# Create your views here.
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('profile', kwargs={'slug': self.object.slug})


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/account_edit.html'
    fields = ['username', 'first_name', 'last_name', 'email']

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'slug': self.object.profile.slug})


class RegisterUserView(FormView):
    template_name = 'accounts/register.html'
    success_url = '/'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        messages.info(
            self.request, "Thanks for registering. You are now logged in.")
        authenticate(user=user.username, password=user.password)
        login(self.request, user)
        return super(RegisterUserView, self).form_valid(form)
