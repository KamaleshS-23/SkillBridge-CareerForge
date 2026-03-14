from django.contrib import admin
from .models import (
    Skill, SkillCategory, ProfessionalIdentity, Education, Certification, Course,
    Project, Language, UserSkill, SkillContextMetadata, AIProfilingSession, SkillGap
)

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'skill_type', 'category']
    list_filter = ['skill_type', 'category']
    search_fields = ['name', 'description']

@admin.register(ProfessionalIdentity)
class ProfessionalIdentityAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'education_level', 'gender', 'location']
    list_filter = ['education_level', 'gender', 'created_at']
    search_fields = ['user__email', 'full_name', 'education_level', 'location']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['user', 'school_name', 'degree_type', 'field_of_study', 'graduation_year']
    list_filter = ['graduation_year', 'degree_type', 'created_at']
    search_fields = ['user__email', 'school_name', 'degree_type']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'certification_name', 'issuing_organization', 'issue_date', 'expiry_date']
    list_filter = ['issue_date', 'is_active', 'created_at']
    search_fields = ['user__email', 'certification_name', 'issuing_organization']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course_name', 'platform', 'completion_date']
    list_filter = ['platform', 'completion_date', 'created_at']
    search_fields = ['user__email', 'course_name', 'platform']
    filter_horizontal = ['skills_acquired']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['user', 'project_name', 'start_date', 'end_date', 'team_size']
    list_filter = ['start_date', 'is_active', 'created_at']
    search_fields = ['user__email', 'project_name', 'description']
    filter_horizontal = ['skills_used']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['user', 'language_name', 'proficiency']
    list_filter = ['proficiency', 'created_at']
    search_fields = ['user__email', 'language_name']
    readonly_fields = ['created_at']

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'proficiency_level', 'years_experience', 'is_verified']
    list_filter = ['proficiency_level', 'is_verified', 'created_at']
    search_fields = ['user__email', 'skill__name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SkillContextMetadata)
class SkillContextMetadataAdmin(admin.ModelAdmin):
    list_display = ['user_skill', 'context_of_use', 'frequency', 'source']
    list_filter = ['source', 'frequency', 'created_at']
    search_fields = ['user_skill__user__email', 'context_of_use']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(AIProfilingSession)
class AIProfilingSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_type', 'status', 'started_at', 'confidence_score']
    list_filter = ['status', 'session_type', 'started_at']
    search_fields = ['user__email', 'source_url']
    readonly_fields = ['started_at', 'completed_at']

@admin.register(SkillGap)
class SkillGapAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'target_role', 'priority']
    list_filter = ['priority', 'target_role', 'created_at']
    search_fields = ['user__email', 'skill__name', 'target_role']
    readonly_fields = ['created_at']
