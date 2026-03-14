from django.contrib import admin
from .models import Company, Job

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'location', 'website', 'created_at']
    list_filter = ['industry', 'created_at']
    search_fields = ['name', 'industry', 'location']
    readonly_fields = ['created_at']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'job_type', 'experience_level', 'location', 'salary_min', 'salary_max']
    list_filter = ['job_type', 'experience_level', 'company']
    search_fields = ['title', 'company__name', 'location', 'description']
    filter_horizontal = ['skills_required']
