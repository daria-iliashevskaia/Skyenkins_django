from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager


class UserRoles:

    USER = "user"
    ADMIN = "admin"
    ROLE = [(USER, "user"), (ADMIN, "admin")]


class User(AbstractUser):

    objects = UserManager()

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    email = models.EmailField(max_length=254, unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    password = models.CharField(max_length=128, verbose_name='Пароль')
    role = models.CharField(max_length=100, choices=UserRoles.ROLE, default=UserRoles.USER, verbose_name='Роль')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']

    def __str__(self):
        return self.email

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER
