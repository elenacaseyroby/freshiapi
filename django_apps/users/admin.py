from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email', 'username')
