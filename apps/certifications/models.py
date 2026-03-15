from django.db import models

class Certification(models.Model):
    PROVIDER_CHOICES = [
        ('aws', 'AWS'),
        ('infosys', 'Infosys'),
        ('tcs', 'TCS'),
        ('coursera', 'Coursera'),
        ('nasscom', 'NASSCOM'),
        ('govt', 'Government'),
        ('other', 'Other'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    name = models.CharField(max_length=200)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    domain = models.CharField(max_length=100)
    description = models.TextField()
    registration_url = models.URLField(max_length=500)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    duration = models.CharField(max_length=100, help_text="Duration of the certification")
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-rating', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.provider}"
