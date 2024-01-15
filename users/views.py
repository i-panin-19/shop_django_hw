from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetView, PasswordResetConfirmView, UserModel
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserForm, UserForgotPasswordForm, UserSetNewPasswordForm, \
    UserAuthenticationForm
from users.models import User
from users.utils import send_email_for_verify


class LoginView(BaseLoginView):
    # template_name = 'users/login.html'
    form_class = UserAuthenticationForm


class LogoutView(BaseLogoutView):
    pass


class EmailVerify(View):
    model = User

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            user.email_is_verified = True
            user.save()
            login(request, user)
            '''
            send_mail(
                subject='Поздравляем с регистрацией!',
                message='Вы зарегистрировались на сайте OfficeShop.org, добро пожаловать!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
            '''
            return redirect('office_shop:index')
        return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


class RegisterView(View):
    model = User
    template_name = 'users/register.html'

    def get(self, request):
        context = {
            'form': UserRegisterForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('users:confirm_email')


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_pass = User.objects.make_random_password()
    send_mail(
        subject='Новый пароль!',
        message=f'Вы изменили пароль на сайте OfficeShop.org. Ваш пароль: {new_pass}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_pass)
    request.user.save()

    return redirect(reverse('office_shop:index'))


class UserForgotPasswordView(PasswordResetView):
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('office_shop:index')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/password_subject_reset_mail.txt'
    email_template_name = 'users/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context


