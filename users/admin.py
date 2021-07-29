""" Users Admin Config """
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.models import User
from users.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'rank', 'level', 'missions']
    list_display_links = ['id', 'user']
    list_editable = ['title', 'rank', 'level', 'missions']
    search_fields = ['user__email', 'user__is_staff', 'created_at', 'modified_at']
    list_filter = ['user__is_active', 'user__is_staff', 'created_at', 'modified_at']

class ProfileInLine(admin.StackedInline):
    """ Profile in-line admin for users """

    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

class UserAdmin(BaseUserAdmin):
    """ Add Profile Admin to base user admin """
    inlines = [ProfileInLine]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
    list_editable = ['is_active', 'is_staff']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)