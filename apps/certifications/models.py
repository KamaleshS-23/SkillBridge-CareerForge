from django.db import models
from django.utils import timezone

class Certification(models.Model):
    PROVIDER_CHOICES = [
        ('aws', 'AWS'),
        ('google', 'Google Cloud'),
        ('microsoft', 'Microsoft'),
        ('coursera', 'Coursera'),
        ('linkedin', 'LinkedIn Learning'),
        ('edx', 'edX'),
        ('udacity', 'Udacity'),
        ('pluralsight', 'Pluralsight'),
        ('nasscom', 'NASSCOM'),
        ('tcs', 'TCS'),
        ('nasscom', 'NASSCOM'),
        ('govt', 'Government'),
        ('comptia', 'CompTIA'),
        ('isc2', '(ISC)²'),
        ('giac', 'GIAC'),
        ('eccouncil', 'EC-Council'),
        ('isaca', 'ISACA'),
        ('offsec', 'Offensive Security'),
        ('cisco', 'Cisco'),
        ('juniper', 'Juniper'),
        ('vmware', 'VMware'),
        ('apple', 'Apple'),
        ('google', 'Google'),
        ('udemy', 'Udemy'),
        ('consensys', 'ConsenSys'),
        ('bca', 'Blockchain Council'),
        ('linux_foundation', 'Linux Foundation'),
        ('oracle', 'Oracle'),
        ('mongodb', 'MongoDB'),
        ('postgresql', 'PostgreSQL'),
        ('pmi', 'PMI'),
        ('scrum_alliance', 'Scrum Alliance'),
        ('scrum_org', 'Scrum.org'),
        ('hubspot', 'HubSpot'),
        ('meta', 'Meta'),
        ('tableau', 'Tableau'),
        ('adobe', 'Adobe'),
        ('other', 'Other'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    SOURCE_CHOICES = [
        ('manual', 'Manual Entry'),
        ('csv_import', 'CSV Import'),
        ('microsoft_api', 'Microsoft API'),
        ('coursera_api', 'Coursera API'),
        ('linkedin_api', 'LinkedIn API'),
        ('aws_scraped', 'AWS Web Scraping'),
        ('google_scraped', 'Google Web Scraping'),
        ('other_api', 'Other API'),
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
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='manual')
    last_updated = models.DateTimeField(default=timezone.now)
    external_id = models.CharField(max_length=100, blank=True, null=True, help_text="External API ID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-rating', 'name']
        indexes = [
            models.Index(fields=['provider', 'is_active']),
            models.Index(fields=['domain', 'is_active']),
            models.Index(fields=['source', 'last_updated']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.provider}"
