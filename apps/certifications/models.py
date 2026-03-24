from django.db import models
from django.utils import timezone

class Certification(models.Model):
    """Model for storing certification information"""
    
    PROVIDER_CHOICES = [
        ('Coursera', 'Coursera'),
        ('AWS', 'AWS'),
        ('Google Cloud', 'Google Cloud'),
        ('Microsoft', 'Microsoft'),
        ('Cisco', 'Cisco'),
        ('PMI', 'PMI'),
        ('Scrum Alliance', 'Scrum Alliance'),
        ('Adobe', 'Adobe'),
        ('Tableau', 'Tableau'),
        ('Oracle', 'Oracle'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    domain = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    registration_url = models.URLField(max_length=500, blank=True)
    rating = models.FloatField(default=4.0)
    duration = models.CharField(max_length=100, blank=True)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    
    # Additional fields for real-time data
    partner_name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    is_synced = models.BooleanField(default=False)
    source = models.CharField(max_length=100, default='manual')
    last_synced = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['name', 'provider']
        ordering = ['-rating', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.provider})"
    
    def get_difficulty_level_display(self):
        return dict(self.DIFFICULTY_CHOICES).get(self.difficulty_level, self.difficulty_level.title())
    
    def get_provider_display(self):
        return dict(self.PROVIDER_CHOICES).get(self.provider, self.provider)
