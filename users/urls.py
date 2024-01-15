from django.urls import path
from django.views.generic import TemplateView

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserUpdateView, generate_new_password, \
    UserForgotPasswordView, UserPasswordResetConfirmView, EmailVerify

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('invalid-verify/', TemplateView.as_view(template_name='users/invalid_verify.html'), name='invalid_verify'),
    path('confirm-email/', TemplateView.as_view(template_name='users/confirm_email.html'), name='confirm_email'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='genpassword'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
