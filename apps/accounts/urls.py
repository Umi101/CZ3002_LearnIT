from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy

from .views import (AccountUpdateView, ProfileDetailView, ProfileUpdateView,
                    RegisterUserView)

urlpatterns = [
    path('accounts/register', RegisterUserView.as_view(), name='register'),

    path('accounts/login/',
         LoginView.as_view(template_name='accounts/login.html'), name='login'),

    path('accounts/logout', LogoutView.as_view(next_page='/'), name='logout'),

    path('accounts/password_reset',
         PasswordResetView.as_view(
             template_name='accounts/password_reset_form.html'),
         name='password_reset'),

    path('accounts/password_reset/done',
         PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),

    path('accounts/reset/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('accounts/reset/done',
         PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

    path('accounts/edit-profile',
         ProfileUpdateView.as_view(), name='edit_profile'),

    path('accounts/edit-account',
         AccountUpdateView.as_view(), name='edit_account'),

    path('profiles/<slug:slug>', ProfileDetailView.as_view(), name='profile'),
]
