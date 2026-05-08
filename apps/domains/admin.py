from django.contrib import admin
from .models import SendingDomain


@admin.register(SendingDomain)
class SendingDomainAdmin(admin.ModelAdmin):
    list_display = ['domain_name', 'user', 'verified', 'created_at']
    readonly_fields = ['verification_token', 'created_at', 'updated_at']
    list_filter = ['verified']