#!/usr/bin/env python
import os
import sys
import django

# Add the project path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

from apps.core.models import Internship
from django.contrib.auth import get_user_model

User = get_user_model()

def create_basic_internships():
    """Create basic internship data for testing"""
    
    # Sample internships
    internships_data = [
        {
            'title': 'Frontend Developer Intern',
            'company': 'TechCorp Solutions',
            'description': 'Join our team to build modern web applications using React and TypeScript. Work on real projects and learn from experienced developers.',
            'location': 'Remote',
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
            'duration': '6 months',
            'stipend': '$800/month',
            'requirements': 'Knowledge of Python, JavaScript, databases. Full stack experience preferred.',
            'skills_required': 'Python, Django, React, PostgreSQL, Git',
            'application_url': 'https://startuphub.io/jobs/fullstack-intern',
            'source': 'LinkedIn',
            'is_featured': True
        },
        {
            'title': 'React Developer Intern',
            'company': 'Innovation Labs',
            'description': 'Focus on React development for cutting-edge web applications. Work with modern tools and frameworks.',
            'location': 'Remote',
            'duration': '3 months',
            'stipend': '$700/month',
            'requirements': 'Strong JavaScript skills, React experience, understanding of state management.',
            'skills_required': 'React, Redux, JavaScript ES6+, CSS, Git',
            'application_url': 'https://innovationlabs.tech/careers/react-intern',
            'source': 'AngelList',
            'is_featured': True
        }
    ]
    
    # Create internships
    created_internships = []
    for data in internships_data:
        internship, created = Internship.objects.get_or_create(
            title=data['title'],
            company=data['company'],
            defaults=data
        )
        created_internships.append(internship)
        print(f"{'Created' if created else 'Found'} internship: {internship.title}")
    
    print(f"\nSample data creation completed!")
    print(f"Created {len(created_internships)} internships")
    
    # Display summary
    total_internships = Internship.objects.count()
    print(f"\nDatabase Summary:")
    print(f"Total Internships: {total_internships}")

if __name__ == '__main__':
    create_basic_internships()
