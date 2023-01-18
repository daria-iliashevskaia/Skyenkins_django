from django.urls import path

from users.views import RegisterUser, LoginUser, logout_user, home

urlpatterns = [
    path('', home, name="home"),
    path('login/', LoginUser.as_view(), name="login"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('logout/', logout_user, name='logout'),
]
