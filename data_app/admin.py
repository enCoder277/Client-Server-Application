from django.contrib import admin
from .models import UserData

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age')
    search_fields = ('name', 'email')
