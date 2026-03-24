from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Internship(models.Model):
    """Internship opportunities from various sources"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('closed', 'Closed'),
    )
    
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, default='Remote')
    duration = models.CharField(max_length=100, default='3 months')  # e.g., "3 months", "6 months"
    stipend = models.CharField(max_length=100, blank=True, default='Unpaid')
    requirements = models.TextField(blank=True)
    skills_required = models.TextField(blank=True)
    application_url = models.URLField(blank=True)
    source = models.CharField(max_length=100, default='Company Website')  # e.g., "LinkedIn", "Indeed", "Company Website"
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-posted_date', '-is_featured']
    
    def __str__(self):
        return f"{self.title} at {self.company}"


class UserInternship(models.Model):
    """Track user's internship enrollment and completion status"""
    STATUS_CHOICES = (
        ('enrolled', 'Enrolled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='internships')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    skills_gained = models.TextField(blank=True)
    experience_rating = models.IntegerField(null=True, blank=True)  # 1-5 rating
    would_recommend = models.BooleanField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'internship']
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.user.email} - {self.internship.title}"


class SavedInternship(models.Model):
    """Internships saved by users for later application"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_internships')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='saved_by')
    saved_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['user', 'internship']
        ordering = ['-saved_date']
    
    def __str__(self):
        return f"{self.user.email} saved {self.internship.title}"


class TechnicalTestResult(models.Model):
    """Store user's technical test results with detailed scoring"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_date = models.DateTimeField(auto_now_add=True)
    
    # Test information
    topic = models.CharField(max_length=100, help_text="Test topic or subject")
    difficulty = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'), 
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ], default='beginner')
    
    # Scoring
    score = models.IntegerField(help_text="Score obtained")
    max_score = models.IntegerField(help_text="Maximum possible score")
    percentage = models.FloatField(default=0.0, help_text="Percentage score")
    correct_answers = models.IntegerField(default=0, help_text="Number of correct answers")
    incorrect_answers = models.IntegerField(default=0, help_text="Number of incorrect answers")
    
    # Time tracking
    time_taken = models.CharField(max_length=20, default='00:00:00', help_text="Time taken to complete the test")
    
    class Meta:
        app_label = 'core'
        verbose_name = 'Technical Test Result'
        verbose_name_plural = 'Technical Test Results'
        ordering = ['-test_date']
    
    def __str__(self):
        return f"{self.user.email} - {self.topic} ({self.percentage}%)"
    
    @property
    def score_display(self):
        """Return formatted score display like '8/10'"""
        return f"{self.score}/{self.max_score}"


class AptitudeTestResult(models.Model):
    """Store user's aptitude test results with detailed breakdown"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_date = models.DateTimeField(auto_now_add=True)
    
    # Score breakdown by section
    quantitative_score = models.IntegerField(default=0)
    verbal_score = models.IntegerField(default=0)
    logical_score = models.IntegerField(default=0)
    data_interpretation_score = models.IntegerField(default=0)
    abstract_reasoning_score = models.IntegerField(default=0)
    
    # Overall metrics
    total_score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    
    # Test metadata
    time_taken = models.CharField(max_length=20, default='00:00:00', help_text="Time taken to complete the test")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('mixed', 'Mixed')
    ], default='mixed')
    
    class Meta:
        app_label = 'core'
        verbose_name = 'Aptitude Test Result'
        verbose_name_plural = 'Aptitude Test Results'
        ordering = ['-test_date']
    
    def __str__(self):
        return f"{self.user.email} - {self.test_date.strftime('%Y-%m-%d')} - {self.percentage}%"
    
    def save(self, *args, **kwargs):
        # Calculate total and percentage before saving
        self.total_score = self.quantitative_score + self.verbal_score + self.logical_score + self.data_interpretation_score + self.abstract_reasoning_score
        if self.max_score > 0:
            self.percentage = round((self.total_score / self.max_score) * 100, 2)
        super().save(*args, **kwargs)


class RoadmapCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fas fa-code')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Roadmap Categories"
    
    def __str__(self):
        return self.name


class RoadmapItem(models.Model):
    category = models.ForeignKey(RoadmapCategory, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'), 
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ], default='beginner')
    estimated_hours = models.IntegerField(default=0)
    resources = models.JSONField(default=dict, blank=True)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'order']
        verbose_name_plural = "Roadmap Items"
    
    def __str__(self):
        return f"{self.category.name} - {self.title}"


class UserRoadmapProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='core_roadmap_progress')
    roadmap_item = models.ForeignKey(RoadmapItem, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    rating = models.IntegerField(choices=[
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent')
    ], null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'roadmap_item']
        verbose_name_plural = "User Roadmap Progress"
    
    def __str__(self):
        return f"{self.user.username} - {self.roadmap_item.title}"
    
    @property
    def completion_percentage(self):
        """Calculate completion percentage for this item"""
        return 100 if self.completed else 0
