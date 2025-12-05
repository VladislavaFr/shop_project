from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Регистрация прошла успешно!")
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthenticationForm

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['username', 'avatar', 'phone', 'country']
    template_name = 'users/profile.html'
    success_url = reverse_lazy('product_list')

    def get_object(self):
        return self.request.user
