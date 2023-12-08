from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "team",
        "is_staff",
        "is_admin",
    )
    list_display_links = (
        "id",
        "username",
        "team",
    )
    list_filter = ("team",)
    search_fields = (
        "username",
        "team",
    )
    # ordering = ("team",)
