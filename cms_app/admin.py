from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token
from .models import *

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("first_name", "last_name", "email")


admin.site.register(Author, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Like)
