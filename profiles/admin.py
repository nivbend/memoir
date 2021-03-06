from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
