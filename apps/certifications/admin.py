from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Certification

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'domain', 'rating', 'difficulty_level', 'duration', 'is_active', 'certification_link']
    list_filter = ['provider', 'domain', 'difficulty_level', 'is_active']
    search_fields = ['name', 'domain', 'description']
    list_editable = ['rating', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'provider', 'domain', 'description')
        }),
        ('Certification Details', {
            'fields': ('registration_url', 'rating', 'duration', 'difficulty_level')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def certification_link(self, obj):
        if obj.registration_url:
            return format_html(
                '<a href="{}" target="_blank" style="color: #7C3AED;">View Certification →</a>',
                obj.registration_url
            )
        return "No URL"
    certification_link.short_description = 'External Link'
    
    actions = ['activate_certifications', 'deactivate_certifications', 'bulk_import_sample_data']
    
    def activate_certifications(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"Activated {queryset.count()} certifications.")
    activate_certifications.short_description = "Activate selected certifications"
    
    def deactivate_certifications(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"Deactivated {queryset.count()} certifications.")
    deactivate_certifications.short_description = "Deactivate selected certifications"
    
    def bulk_import_sample_data(self, request, queryset):
        from django.core.management import call_command
        call_command('create_sample_data')
        self.message_user(request, "Sample data imported successfully!")
    bulk_import_sample_data.short_description = "Import sample data"
