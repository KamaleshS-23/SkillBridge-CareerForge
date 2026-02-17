from django.db import models
from apps.accounts.models import User

class SkillCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Skill categories"
    
    def __str__(self):
        return self.name

class Skill(models.Model):
    SKILL_TYPES = (
        ('technical', 'Technical'),
        ('soft', 'Soft'),
        ('domain', 'Domain'),
    )
    
    PROFICIENCY_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    )
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    skill_type = models.CharField(max_length=20, choices=SKILL_TYPES)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=20, choices=Skill.PROFICIENCY_LEVELS)
    years_experience = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'skill']
    
    def __str__(self):
        return f"{self.user.email} - {self.skill.name}"

class SkillGap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_gaps')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    target_role = models.CharField(max_length=100)
    current_proficiency = models.CharField(max_length=20, choices=Skill.PROFICIENCY_LEVELS)
    required_proficiency = models.CharField(max_length=20, choices=Skill.PROFICIENCY_LEVELS)
    priority = models.IntegerField(default=1)  # 1 = highest priority
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.skill.name} Gap"