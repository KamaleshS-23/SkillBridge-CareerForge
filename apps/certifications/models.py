from django.db import models
from django.utils import timezone

class Certification(models.Model):
    """Model for storing certification information"""
    
    PROVIDER_CHOICES = [
        ('coursera', 'Coursera'),
        ('aws', 'AWS'),
        ('google', 'Google'),
        ('microsoft', 'Microsoft'),
        ('cisco', 'Cisco'),
        ('pmi', 'PMI'),
        ('scrum_alliance', 'Scrum Alliance'),
        ('adobe', 'Adobe'),
        ('tableau', 'Tableau'),
        ('oracle', 'Oracle'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    domain = models.CharField(max_length=100)
    description = models.TextField()
    registration_url = models.URLField()
    rating = models.FloatField(default=4.0)
    duration = models.CharField(max_length=100)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    is_active = models.BooleanField(default=True)
    is_synced = models.BooleanField(default=False)
    source = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['name', 'provider']
        ordering = ['-rating', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_provider_display()})"
    
    def get_difficulty_level_display(self):
        return dict(self.DIFFICULTY_CHOICES).get(self.difficulty_level, self.difficulty_level)
