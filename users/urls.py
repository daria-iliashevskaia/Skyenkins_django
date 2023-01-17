from django.contrib import admin
from django.urls import path, include

from users import views
from users.views import login, RegisterUser, LoginUser

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', LoginUser.as_view(), name="login"),
    path('register/', RegisterUser.as_view(), name="register")
]
