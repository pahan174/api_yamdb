from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администатор')
)


class CustomUser(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    username = models.CharField('Логин', max_length=150, unique=True)
    email = models.EmailField('Электронная почта', max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль', max_length=9, choices=ROLE, default=USER)
    confirmation_code = models.CharField('Токен', max_length=254, blank=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ADMIN

        if self.role == self.ADMIN:
            self.is_staff = True
        else:
            self.is_staff = False
        super(CustomUser, self).save(*args, **kwargs)

    class Meta:
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]


