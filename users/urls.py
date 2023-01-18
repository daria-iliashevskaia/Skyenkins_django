from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterUser, LoginUser, logout_user


app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginUser.as_view(), name="login"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('logout/', logout_user, name='logout'),
]
