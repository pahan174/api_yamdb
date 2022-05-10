from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'bio',
                    'role', 'is_staff', 'confirmation_code']


admin.site.register(CustomUser, CustomUserAdmin)
