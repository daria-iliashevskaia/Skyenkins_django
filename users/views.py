from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import CustomUserCreationForm


def home(request):
    return render(request, "users/home.html")


def login(request):
    return render(request, "users/registration.html")


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')