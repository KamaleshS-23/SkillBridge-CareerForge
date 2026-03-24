from django.db import models
from django.utils import timezone
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
        ('language', 'Language'),
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


# ==================== AI PROFILING MODELS ====================

class ProfessionalIdentity(models.Model):
    """Store professional identity data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professional_identity')
    full_name = models.CharField(max_length=255)
    education_level = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    native_language = models.CharField(max_length=100, blank=True)
    
    # Source tracking
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    resume_url = models.URLField(blank=True)
    
    # Data extraction metadata
    last_linkedin_sync = models.DateTimeField(null=True, blank=True)
    last_resume_upload = models.DateTimeField(null=True, blank=True)
    last_github_sync = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.user.email}"


class Education(models.Model):
    """Store education and degree information"""
    DEGREE_CHOICES = (
        ('high_school', 'High School'),
        ('bachelor', "Bachelor's"),
        ('master', "Master's"),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    degree_type = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    field_of_study = models.CharField(max_length=255)
    school_name = models.CharField(max_length=255)
    graduation_year = models.PositiveIntegerField()
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-graduation_year']
    
    def __str__(self):
        return f"{self.user.email} - {self.degree_type} in {self.field_of_study}"


class Certification(models.Model):
    """Store certifications and credentials"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certifications')
    certification_name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=255, blank=True)
    credential_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.user.email} - {self.certification_name}"


class Course(models.Model):
    """Store completed courses and learning activities"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    course_name = models.CharField(max_length=255)
    platform = models.CharField(max_length=100)  # Coursera, Udemy, LinkedIn Learning, etc.
    completion_date = models.DateField()
    certificate_url = models.URLField(blank=True)
    skills_acquired = models.ManyToManyField(Skill, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-completion_date']
    
    def __str__(self):
        return f"{self.user.email} - {self.course_name}"


class SkillContextMetadata(models.Model):
    """Store contextual metadata for skills"""
    user_skill = models.OneToOneField(UserSkill, on_delete=models.CASCADE, related_name='metadata')
    
    # Context of use
    context_of_use = models.TextField(help_text="e.g., 'Built production APIs', 'Took a course'")
    frequency = models.CharField(
        max_length=20,
        choices=(
            ('rare', 'Mentioned once'),
            ('occasional', 'Mentioned few times'),
            ('frequent', 'Throughout resume/profile'),
            ('primary', 'Primary focus'),
        ),
        default='occasional'
    )
    
    # Recency
    last_used_date = models.DateField(null=True, blank=True)
    
    # Source of knowledge
    source = models.CharField(
        max_length=50,
        choices=(
            ('resume', 'Resume'),
            ('linkedin', 'LinkedIn'),
            ('github', 'GitHub'),
            ('project', 'Project'),
            ('certification', 'Certification'),
            ('course', 'Course'),
            ('manual', 'Manual Entry'),
        )
    )
    
    # Related entities
    related_project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True)
    related_certification = models.ForeignKey(Certification, on_delete=models.SET_NULL, null=True, blank=True)
    related_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Metadata for {self.user_skill}"


class Project(models.Model):
    """Store projects and work experience"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Associated skills
    skills_used = models.ManyToManyField(Skill, blank=True)
    
    # Metrics
    team_size = models.PositiveIntegerField(null=True, blank=True)
    impact = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.user.email} - {self.project_name}"


class Language(models.Model):
    """Store language proficiencies"""
    PROFICIENCY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('fluent', 'Fluent'),
        ('native', 'Native'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='languages')
    language_name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'language_name']
    
    def __str__(self):
        return f"{self.user.email} - {self.language_name} ({self.proficiency})"


class AIProfilingSession(models.Model):
    """Track AI profiling sessions and extractions"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiling_sessions')
    session_type = models.CharField(
        max_length=20,
        choices=(
            ('linkedin', 'LinkedIn'),
            ('resume', 'Resume'),
            ('github', 'GitHub'),
            ('manual', 'Manual'),
        )
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Source data
    source_url = models.URLField(blank=True)
    file_path = models.CharField(max_length=500, blank=True)
    
    # Extraction results
    extracted_data = models.JSONField(default=dict, blank=True)
    skills_extracted = models.PositiveIntegerField(default=0)
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    
    # Error handling
    error_message = models.TextField(blank=True)
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.session_type} ({self.status})"

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


class UserRoadmapProgress(models.Model):
    """Track user's progress through career roadmap skills"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roadmap_progress')
    career_path = models.CharField(max_length=100)  # e.g., "Software Engineer", "Data Scientist"
    category_name = models.CharField(max_length=100)  # e.g., "Frontend", "Backend"
    skill_name = models.CharField(max_length=100)  # e.g., "React", "Python"
    is_completed = models.BooleanField(default=False)
    category_index = models.IntegerField(default=0)  # Position in roadmap
    skill_index = models.IntegerField(default=0)  # Position within category
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'career_path', 'skill_name']
        ordering = ['career_path', 'category_index', 'skill_index']
    
    def __str__(self):
        return f"{self.user.email} - {self.career_path}: {self.skill_name} ({'✓' if self.is_completed else '○'})"


class TechnicalTestResult(models.Model):
    """Store user's technical assessment test results"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='technical_test_results')
    subject = models.CharField(max_length=100)  # e.g., "Data Structures", "Operating Systems", "Algorithms"
    difficulty = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'), 
        ('advanced', 'Advanced')
    ])
    score = models.IntegerField()  # Number of correct answers
    total_questions = models.IntegerField()  # Total questions in test
    percentage = models.FloatField()  # Score percentage
    grade = models.CharField(max_length=20)  # e.g., "Excellent", "Good", "Need More Practice"
    correct_answers = models.TextField()  # JSON string of correct question numbers
    incorrect_answers = models.TextField()  # JSON string of incorrect question numbers
    time_taken = models.IntegerField(null=True, blank=True)  # Time taken in seconds
    test_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-test_date']
        indexes = [
            models.Index(fields=['user', 'subject']),
            models.Index(fields=['user', 'test_date']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.subject}: {self.score}/{self.total_questions} ({self.percentage:.1f}%)" 