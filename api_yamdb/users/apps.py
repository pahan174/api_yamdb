from tabnanny import verbose
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Управление пользователеями проекта'
