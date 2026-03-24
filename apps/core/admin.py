from django.contrib import admin
from .models import (
    Internship, UserInternship, SavedInternship, AptitudeTestResult,
    RoadmapCategory, RoadmapItem, UserRoadmapProgress
)

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'status', 'is_featured', 'posted_date']
    list_filter = ['status', 'is_featured', 'location', 'posted_date']
    search_fields = ['title', 'company', 'description']
    readonly_fields = ['posted_date', 'created_at', 'updated_at']

@admin.register(UserInternship)
class UserInternshipAdmin(admin.ModelAdmin):
    list_display = ['user', 'internship', 'status', 'enrollment_date', 'completion_date']
    list_filter = ['status', 'enrollment_date', 'completion_date']
    search_fields = ['user__email', 'internship__title']
    readonly_fields = ['enrollment_date']

@admin.register(SavedInternship)
class SavedInternshipAdmin(admin.ModelAdmin):
    list_display = ['user', 'internship', 'saved_date']
    list_filter = ['saved_date']
    search_fields = ['user__email', 'internship__title']
    readonly_fields = ['saved_date']

@admin.register(AptitudeTestResult)
class AptitudeTestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test_date', 'total_score', 'max_score', 'percentage', 'difficulty_level']
    list_filter = ['difficulty_level', 'test_date']
    search_fields = ['user__email']
    readonly_fields = ['test_date']

@admin.register(RoadmapCategory)
class RoadmapCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'icon']
    search_fields = ['name', 'description']
    ordering = ['order']

@admin.register(RoadmapItem)
class RoadmapItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'estimated_hours', 'order']
    list_filter = ['category', 'difficulty']
    search_fields = ['title', 'description']
    filter_horizontal = ['prerequisites']
    ordering = ['category', 'order']

@admin.register(UserRoadmapProgress)
class UserRoadmapProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'roadmap_item', 'completed', 'completed_at', 'rating']
    list_filter = ['completed', 'rating', 'completed_at']
    search_fields = ['user__email', 'roadmap_item__title']
    readonly_fields = ['started_at', 'last_updated']
