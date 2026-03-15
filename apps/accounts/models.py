from django.contrib.auth.models import AbstractUser
from django.db import models


# 🔹 Field Choices
FIELD_CHOICES = [
    ('data_science', 'Data Science'),
    ('web_dev', 'Web Development'),
    ('ai_ml', 'AI / ML'),
    ('cyber_security', 'Cyber Security'),
    ('cloud', 'Cloud Computing'),
]


class User(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('professional', 'Professional'),
        ('employer', 'Employer'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')

    # 🔥 Important for recommendation system
    field_of_interest = models.CharField(
        max_length=50,
        choices=FIELD_CHOICES,
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


# 🔹 User Earned Certifications
class Certification(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='certifications'
    )
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=200, blank=True)
    credential_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.email}"


# 🔹 Admin Managed Certification Catalog (Recommendations)
class CertificationCatalog(models.Model):
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    field = models.CharField(max_length=50, choices=FIELD_CHOICES)
    description = models.TextField()
    official_url = models.URLField()

    def __str__(self):
        return f"{self.title} - {self.organization}"