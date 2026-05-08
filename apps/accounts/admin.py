from django.contrib import admin
from .models import APIKey

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['label', 'user', 'prefix', 'is_active', 'last_used_at', 'created_at']
    readonly_fields = ['prefix', 'hashed_key', 'last_used_at']
    list_filter = ['is_active']