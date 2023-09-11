from django.contrib import admin
from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("is_superuser", "is_staff", "is_active")
    list_display = ("username", "email", "last_name", "first_name")
    search_fields = ("email", "first_name", "last_name", "username")
    exclude = ("last_login", "date_joined")