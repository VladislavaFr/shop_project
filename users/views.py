from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # отправка email
        send_mail(
            subject="Добро пожаловать!",
            message="Спасибо за регистрацию на сайте!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[form.instance.email],
            fail_silently=False,
        )

        messages.success(self.request, 'Регистрация прошла успешно!')
        return response


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'


class ProfileUpdateView(UpdateView):
    model = CustomUser
    fields = ['username', 'avatar', 'phone', 'country']
    template_name = 'users/profile.html'
    success_url = reverse_lazy('product_list')

    def get_object(self):
        return self.request.user
