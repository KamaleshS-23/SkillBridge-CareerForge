from django.core.management.base import BaseCommand
from apps.certifications.models import Certification

class Command(BaseCommand):
    help = 'Create sample certification data'

    def handle(self, *args, **kwargs):
        certifications = [
            # AWS Certifications
            {
                'name': 'AWS Certified Solutions Architect - Associate',
                'provider': 'aws',
                'domain': 'Cloud Computing',
                'description': 'Validate your ability to design distributed systems on AWS platform and deploy scalable, highly available infrastructure.',
                'registration_url': 'https://aws.amazon.com/certification/certified-solutions-architect-associate/',
                'rating': 4.7,
                'duration': '3-6 months',
                'difficulty_level': 'intermediate',
            },
            {
                'name': 'AWS Certified Developer - Associate',
                'provider': 'aws',
                'domain': 'Cloud Computing',
                'description': 'Demonstrate your ability to develop, deploy, and debug cloud-based applications using AWS.',
                'registration_url': 'https://aws.amazon.com/certification/certified-developer-associate/',
                'rating': 4.6,
                'duration': '2-4 months',
                'difficulty_level': 'intermediate',
            },
            {
                'name': 'AWS Certified Machine Learning - Specialty',
                'provider': 'aws',
                'domain': 'Machine Learning',
                'description': 'Validate your ability to build, train, tune, and deploy machine learning models on AWS.',
                'registration_url': 'https://aws.amazon.com/certification/machine-learning/',
                'rating': 4.5,
                'duration': '6-12 months',
                'difficulty_level': 'advanced',
            },
            
            # Infosys Certifications
            {
                'name': 'Infosys Certified Python Developer',
                'provider': 'infosys',
                'domain': 'Programming',
                'description': 'Comprehensive certification covering Python programming, frameworks, and enterprise application development.',
                'registration_url': 'https://www.infosys.com/services/digital/certification/python-developer',
                'rating': 4.3,
                'duration': '3 months',
                'difficulty_level': 'intermediate',
            },
            {
                'name': 'Infosys Cloud Computing Certification',
                'provider': 'infosys',
                'domain': 'Cloud Computing',
                'description': 'Master cloud architecture, deployment models, and enterprise cloud solutions with Infosys expertise.',
                'registration_url': 'https://www.infosys.com/services/digital/certification/cloud-computing',
                'rating': 4.4,
                'duration': '4 months',
                'difficulty_level': 'intermediate',
            },
            
            # TCS Certifications
            {
                'name': 'TCS Digital Certification Program',
                'provider': 'tcs',
                'domain': 'Digital Transformation',
                'description': 'Comprehensive program covering digital technologies, AI, IoT, and blockchain for enterprise solutions.',
                'registration_url': 'https://www.tcs.com/digital-certification',
                'rating': 4.5,
                'duration': '6 months',
                'difficulty_level': 'intermediate',
            },
            {
                'name': 'TCS Cybersecurity Expert Certification',
                'provider': 'tcs',
                'domain': 'Cybersecurity',
                'description': 'Advanced cybersecurity certification covering network security, ethical hacking, and compliance frameworks.',
                'registration_url': 'https://www.tcs.com/cybersecurity-certification',
                'rating': 4.6,
                'duration': '5 months',
                'difficulty_level': 'advanced',
            },
            
            # Coursera Certifications
            {
                'name': 'Google Data Analytics Professional Certificate',
                'provider': 'coursera',
                'domain': 'Data Science',
                'description': 'Learn data analysis skills with Google. Gain skills in R programming, data cleaning, and visualization.',
                'registration_url': 'https://www.coursera.org/professional-certificates/google-data-analytics',
                'rating': 4.7,
                'duration': '6 months',
                'difficulty_level': 'beginner',
            },
            {
                'name': 'IBM Machine Learning Professional Certificate',
                'provider': 'coursera',
                'domain': 'Machine Learning',
                'description': 'Master machine learning concepts, algorithms, and practical applications with IBM expertise.',
                'registration_url': 'https://www.coursera.org/professional-certificates/ibm-machine-learning',
                'rating': 4.6,
                'duration': '8 months',
                'difficulty_level': 'intermediate',
            },
            {
                'name': 'Deep Learning Specialization',
                'provider': 'coursera',
                'domain': 'Deep Learning',
                'description': 'Master deep learning fundamentals, neural networks, and AI applications with Andrew Ng.',
                'registration_url': 'https://www.coursera.org/specializations/deep-learning',
                'rating': 4.8,
                'duration': '4 months',
                'difficulty_level': 'advanced',
            },
            
            # NASSCOM Certifications
            {
                'name': 'NASSCOM Certified IT Professional',
                'provider': 'nasscom',
                'domain': 'Information Technology',
                'description': 'Industry-recognized certification for IT professionals covering software development and project management.',
                'registration_url': 'https://www.nasscom.in/certification/it-professional',
                'rating': 4.4,
                'duration': '3 months',
                'difficulty_level': 'intermediate',
            },
            {
                'name': 'NASSCOM AI/ML Certification',
                'provider': 'nasscom',
                'domain': 'Artificial Intelligence',
                'description': 'Comprehensive AI and machine learning certification aligned with industry standards.',
                'registration_url': 'https://www.nasscom.in/certification/ai-ml',
                'rating': 4.5,
                'duration': '6 months',
                'difficulty_level': 'intermediate',
            },
            
            # Government Certifications
            {
                'name': 'Digital India Certification Program',
                'provider': 'govt',
                'domain': 'Digital Literacy',
                'description': 'Government certification promoting digital literacy and e-governance skills for citizens.',
                'registration_url': 'https://digitalindia.gov.in/certification',
                'rating': 4.2,
                'duration': '2 months',
                'difficulty_level': 'beginner',
            },
            {
                'name': 'National Skill Development Certification',
                'provider': 'govt',
                'domain': 'Skill Development',
                'description': 'NSDC certification covering various technical and vocational skills for employment.',
                'registration_url': 'https://www.nsdcindia.org/certification',
                'rating': 4.3,
                'duration': '3 months',
                'difficulty_level': 'beginner',
            },
            {
                'name': 'Pradhan Mantri Kaushal Vikas Yojana (PMKVY)',
                'provider': 'govt',
                'domain': 'Vocational Training',
                'description': 'Flag government skill development program offering industry-relevant certifications.',
                'registration_url': 'https://pmkvyofficial.org/certification',
                'rating': 4.1,
                'duration': '2-4 months',
                'difficulty_level': 'beginner',
            },
            {
                'name': 'Cyber Swachhata Certification',
                'provider': 'govt',
                'domain': 'Cybersecurity',
                'description': 'Government certification for cybersecurity awareness and digital security practices.',
                'registration_url': 'https://cyberswachhata.gov.in/certification',
                'rating': 4.0,
                'duration': '1 month',
                'difficulty_level': 'beginner',
            },
        ]
        
        created_count = 0
        for cert_data in certifications:
            cert, created = Certification.objects.get_or_create(
                name=cert_data['name'],
                provider=cert_data['provider'],
                defaults=cert_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created certification: {cert.name}")
            else:
                self.stdout.write(f"Certification already exists: {cert.name}")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} certifications'))
