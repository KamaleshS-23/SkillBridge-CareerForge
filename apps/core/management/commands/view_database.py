from django.core.management.base import BaseCommand
from django.db import connection
from apps.accounts.models import User
from apps.skills.models import (
    ProfessionalIdentity, Education, Certification, Course, 
    Project, Language, UserSkill, Skill, SkillContextMetadata, 
    AIProfilingSession
)
from apps.jobs.models import Job
from django.utils import timezone

class Command(BaseCommand):
    help = 'Display all database contents in a formatted way'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*80))
        self.stdout.write(self.style.SUCCESS('DATABASE CONTENTS - SkillBridge & CareerForge'))
        self.stdout.write(self.style.SUCCESS('='*80 + '\n'))

        # Users
        self.display_users()
        
        # Professional Identities
        self.display_professional_identities()
        
        # Education
        self.display_education()
        
        # Skills
        self.display_skills()
        
        # Certifications
        self.display_certifications()
        
        # Projects
        self.display_projects()
        
        # Languages
        self.display_languages()
        
        # Courses
        self.display_courses()
        
        # Jobs
        self.display_jobs()
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*80))
        self.stdout.write(self.style.SUCCESS('Database Statistics'))
        self.stdout.write(self.style.SUCCESS('='*80 + '\n'))
        
        self.display_statistics()

    def display_users(self):
        self.stdout.write(self.style.WARNING('\n▸ USERS\n'))
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.ERROR('  No users found'))
            return
        
        for idx, user in enumerate(users, 1):
            self.stdout.write(f"  {idx}. Email: {user.email}")
            self.stdout.write(f"     Username: {user.username}")
            self.stdout.write(f"     Full Name: {user.first_name} {user.last_name or '(No name set)'}")
            self.stdout.write(f"     Active: {user.is_active}")
            self.stdout.write(f"     Joined: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
            self.stdout.write('')

    def display_professional_identities(self):
        self.stdout.write(self.style.WARNING('▸ PROFESSIONAL IDENTITIES\n'))
        profiles = ProfessionalIdentity.objects.all()
        
        if not profiles.exists():
            self.stdout.write(self.style.ERROR('  No professional identities found'))
            return
        
        for idx, profile in enumerate(profiles, 1):
            self.stdout.write(f"  {idx}. User: {profile.user.email}")
            self.stdout.write(f"     Full Name: {profile.full_name or '(Not set)'}")
            self.stdout.write(f"     Education Level: {profile.education_level or '(Not set)'}")
            self.stdout.write(f"     Date of birth: {profile.date_of_birth or '(Not set)'}")
            self.stdout.write(f"     Gender: {profile.gender or '(Not set)'}")
            self.stdout.write(f"     Phone: {profile.phone_number or '(Not set)'}")
            self.stdout.write(f"     Location: {profile.location or '(Not set)'}")
            self.stdout.write(f"     Native Language: {profile.native_language or '(Not set)'}")
            self.stdout.write(f"     LinkedIn: {profile.linkedin_url or '(Not set)'}")
            self.stdout.write(f"     GitHub: {profile.github_url or '(Not set)'}")
            self.stdout.write('')

    def display_education(self):
        self.stdout.write(self.style.WARNING('▸ EDUCATION\n'))
        education = Education.objects.all()
        
        if not education.exists():
            self.stdout.write(self.style.ERROR('  No education records found'))
            return
        
        for idx, edu in enumerate(education, 1):
            self.stdout.write(f"  {idx}. User: {edu.user.email}")
            self.stdout.write(f"     School: {edu.school_name}")
            self.stdout.write(f"     Degree: {edu.degree_type}")
            self.stdout.write(f"     Field: {edu.field_of_study}")
            self.stdout.write(f"     Graduation: {edu.graduation_year}")
            self.stdout.write(f"     GPA: {edu.gpa or '(Not set)'}")
            self.stdout.write('')

    def display_skills(self):
        self.stdout.write(self.style.WARNING('▸ SKILLS\n'))
        skills = UserSkill.objects.all()
        
        if not skills.exists():
            self.stdout.write(self.style.ERROR('  No skills found'))
            return
        
        for idx, skill in enumerate(skills, 1):
            self.stdout.write(f"  {idx}. User: {skill.user.email}")
            self.stdout.write(f"     Skill: {skill.skill.name}")
            self.stdout.write(f"     Proficiency: {skill.get_proficiency_level_display()}")
            self.stdout.write(f"     Years: {skill.years_of_experience}")
            self.stdout.write(f"     Verified: {'Yes' if skill.is_verified else 'No'}")
            self.stdout.write('')

    def display_certifications(self):
        self.stdout.write(self.style.WARNING('▸ CERTIFICATIONS\n'))
        certs = Certification.objects.all()
        
        if not certs.exists():
            self.stdout.write(self.style.ERROR('  No certifications found'))
            return
        
        for idx, cert in enumerate(certs, 1):
            self.stdout.write(f"  {idx}. User: {cert.user.email}")
            self.stdout.write(f"     Certification: {cert.cert_name}")
            self.stdout.write(f"     Organization: {cert.issuing_org}")
            self.stdout.write(f"     Issue Date: {cert.issue_date}")
            self.stdout.write(f"     Expiry: {cert.expiry_date or '(No expiry)'}")
            self.stdout.write(f"     Credential URL: {cert.credential_url or '(Not set)'}")
            self.stdout.write('')

    def display_projects(self):
        self.stdout.write(self.style.WARNING('▸ PROJECTS\n'))
        projects = Project.objects.all()
        
        if not projects.exists():
            self.stdout.write(self.style.ERROR('  No projects found'))
            return
        
        for idx, project in enumerate(projects, 1):
            self.stdout.write(f"  {idx}. User: {project.user.email}")
            self.stdout.write(f"     Project: {project.project_name}")
            self.stdout.write(f"     Description: {project.description[:100]}{'...' if len(project.description) > 100 else ''}")
            self.stdout.write(f"     Start Date: {project.start_date}")
            self.stdout.write(f"     End Date: {project.end_date or '(Ongoing)'}")
            self.stdout.write(f"     Team Size: {project.team_size}")
            self.stdout.write('')

    def display_languages(self):
        self.stdout.write(self.style.WARNING('▸ LANGUAGES\n'))
        languages = Language.objects.all()
        
        if not languages.exists():
            self.stdout.write(self.style.ERROR('  No languages found'))
            return
        
        for idx, lang in enumerate(languages, 1):
            self.stdout.write(f"  {idx}. User: {lang.user.email}")
            self.stdout.write(f"     Language: {lang.language_name}")
            self.stdout.write(f"     Proficiency: {lang.get_proficiency_level_display()}")
            self.stdout.write('')

    def display_courses(self):
        self.stdout.write(self.style.WARNING('▸ COURSES\n'))
        courses = Course.objects.all()
        
        if not courses.exists():
            self.stdout.write(self.style.ERROR('  No courses found'))
            return
        
        for idx, course in enumerate(courses, 1):
            self.stdout.write(f"  {idx}. User: {course.user.email}")
            self.stdout.write(f"     Course: {course.course_name}")
            self.stdout.write(f"     Platform: {course.platform}")
            self.stdout.write(f"     Completion Date: {course.completion_date or '(Not completed)'}")
            self.stdout.write(f"     Certificate URL: {course.certificate_url or '(Not set)'}")
            self.stdout.write('')

    def display_jobs(self):
        self.stdout.write(self.style.WARNING('▸ JOBS\n'))
        jobs = Job.objects.all()
        
        if not jobs.exists():
            self.stdout.write(self.style.ERROR('  No jobs found'))
            return
        
        for idx, job in enumerate(jobs, 1):
            self.stdout.write(f"  {idx}. Title: {job.title if hasattr(job, 'title') else 'N/A'}")
            self.stdout.write(f"     Company: {job.company if hasattr(job, 'company') else 'N/A'}")
            self.stdout.write('')

    def display_statistics(self):
        users_count = User.objects.count()
        profiles_count = ProfessionalIdentity.objects.count()
        education_count = Education.objects.count()
        skills_count = UserSkill.objects.count()
        certs_count = Certification.objects.count()
        projects_count = Project.objects.count()
        languages_count = Language.objects.count()
        courses_count = Course.objects.count()
        jobs_count = Job.objects.count()
        
        self.stdout.write(f"  Total Users: {users_count}")
        self.stdout.write(f"  Total Professional Identities: {profiles_count}")
        self.stdout.write(f"  Total Education Records: {education_count}")
        self.stdout.write(f"  Total Skills: {skills_count}")
        self.stdout.write(f"  Total Certifications: {certs_count}")
        self.stdout.write(f"  Total Projects: {projects_count}")
        self.stdout.write(f"  Total Languages: {languages_count}")
        self.stdout.write(f"  Total Courses: {courses_count}")
        self.stdout.write(f"  Total Jobs: {jobs_count}")
        self.stdout.write(f"\n  Total Records: {users_count + profiles_count + education_count + skills_count + certs_count + projects_count + languages_count + courses_count + jobs_count}")
        self.stdout.write('\n')
