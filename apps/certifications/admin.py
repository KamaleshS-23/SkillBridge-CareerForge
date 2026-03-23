from django.contrib import admin
from .models import Certification

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'domain', 'difficulty_level', 'rating', 'is_active', 'last_updated')
    list_filter = ('provider', 'difficulty_level', 'domain', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('-last_updated',)
