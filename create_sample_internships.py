#!/usr/bin/env python
import os
import sys
import django

# Add the project path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

from apps.core.models import Internship, UserInternship, SavedInternship
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def create_sample_internships():
    """Create sample internship data for testing"""
    
    # Sample internships
    internships_data = [
        {
            'title': 'Frontend Developer Intern',
            'company': 'TechCorp Solutions',
            'description': 'Join our team to build modern web applications using React and TypeScript. Work on real projects and learn from experienced developers.',
            'location': 'Remote',
            'type': 'remote',
            'duration': '3 months',
            'stipend': '$500/month',
            'requirements': 'Basic knowledge of HTML, CSS, JavaScript. Experience with React is a plus.',
            'skills_required': 'React, JavaScript, TypeScript, HTML, CSS',
            'application_url': 'https://techcorp.com/careers/frontend-intern',
            'source': 'Company Website',
            'is_featured': True
        },
        {
            'title': 'Full Stack Developer Intern',
            'company': 'StartupHub',
            'description': 'Work on both frontend and backend development. Build features from database to user interface.',
            'location': 'Hybrid',
            'type': 'hybrid',
            'duration': '6 months',
            'stipend': '$800/month',
            'requirements': 'Knowledge of Python, JavaScript, databases. Full stack experience preferred.',
            'skills_required': 'Python, Django, React, PostgreSQL, Git',
            'application_url': 'https://startuphub.io/jobs/fullstack-intern',
            'source': 'LinkedIn',
            'is_featured': True
        },
        {
            'title': 'Web Development Intern',
            'company': 'Digital Agency',
            'description': 'Create websites for various clients. Learn project management and client communication.',
            'location': 'On-site',
            'type': 'onsite',
            'duration': '4 months',
            'stipend': '$600/month',
            'requirements': 'HTML, CSS, JavaScript basics. Portfolio of web projects required.',
            'skills_required': 'HTML, CSS, JavaScript, WordPress, Photoshop',
            'application_url': 'https://digitalagency.com/careers',
            'source': 'Indeed',
            'is_featured': False
        },
        {
            'title': 'React Developer Intern',
            'company': 'Innovation Labs',
            'description': 'Focus on React development for cutting-edge web applications. Work with modern tools and frameworks.',
            'location': 'Remote',
            'type': 'remote',
            'duration': '3 months',
            'stipend': '$700/month',
            'requirements': 'Strong JavaScript skills, React experience, understanding of state management.',
            'skills_required': 'React, Redux, JavaScript ES6+, CSS, Git',
            'application_url': 'https://innovationlabs.tech/careers/react-intern',
            'source': 'AngelList',
            'is_featured': True
        },
        {
            'title': 'Backend Developer Intern',
            'company': 'DataTech Inc',
            'description': 'Work on API development, database design, and server-side logic.',
            'location': 'Remote',
            'type': 'remote',
            'duration': '5 months',
            'stipend': '$750/month',
            'requirements': 'Python or Node.js experience, database knowledge, API understanding.',
            'skills_required': 'Python, Django, REST APIs, PostgreSQL, Docker',
            'application_url': 'https://datatech.com/jobs/backend-intern',
            'source': 'Company Website',
            'is_featured': False
        }
    ]
    
    created_internships = []
    for data in internships_data:
        internship, created = Internship.objects.get_or_create(
            title=data['title'],
            company=data['company'],
            defaults=data
        )
        created_internships.append(internship)
        print(f"{'Created' if created else 'Found'} internship: {internship.title}")
    
    return created_internships

def create_sample_user_internships(user, internships):
    """Create sample user internship enrollments"""
    
    if not user:
        print("No user provided")
        return
    
    # Create sample enrollments
    enrollments_data = [
        {
            'internship': internships[0],  # Frontend Developer Intern
            'status': 'enrolled',
            'notes': 'Just started this internship. Excited to learn React best practices.'
        },
        {
            'internship': internships[1],  # Full Stack Developer Intern
            'status': 'in_progress',
            'notes': 'Working on the main dashboard feature. Learning a lot about Django.',
            'start_date': timezone.now()
        },
        {
            'internship': internships[2],  # Web Development Intern
            'status': 'completed',
            'notes': 'Great experience! Built 3 client websites and improved my CSS skills.',
            'completion_date': timezone.now(),
            'skills_gained': 'Advanced CSS, Client Communication, Project Management, WordPress',
            'experience_rating': 4,
            'would_recommend': True
        }
    ]
    
    for data in enrollments_data:
        enrollment, created = UserInternship.objects.get_or_create(
            user=user,
            internship=data['internship'],
            defaults=data
        )
        print(f"{'Created' if created else 'Found'} enrollment: {enrollment.internship.title} - {enrollment.status}")
    
    # Create saved internships
    saved_data = [
        {
            'internship': internships[3],  # React Developer Intern
            'notes': 'Interested in this for the React focus and modern tech stack.'
        },
        {
            'internship': internships[4],  # Backend Developer Intern
            'notes': 'Good opportunity to learn backend development and APIs.'
        }
    ]
    
    for data in saved_data:
        saved, created = SavedInternship.objects.get_or_create(
            user=user,
            internship=data['internship'],
            defaults=data
        )
        print(f"{'Created' if created else 'Found'} saved internship: {saved.internship.title}")

if __name__ == '__main__':
    print("Creating sample internship data...")
    
    # Create internships
    internships = create_sample_internships()
    
    # Get or create a test user
    try:
        user = User.objects.get(email='test@example.com')
        print(f"Found existing user: {user.email}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print(f"Created new user: {user.email}")
    
    # Create user internships
    create_sample_user_internships(user, internships)
    
    print("\nSample data creation completed!")
    print("You can now test the internship tracking functionality.")
