from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff','is_active']


admin.site.register(User,UserAdmin)
