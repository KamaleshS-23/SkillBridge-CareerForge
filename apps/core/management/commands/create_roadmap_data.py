from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import RoadmapCategory, RoadmapItem

User = get_user_model()

class Command(BaseCommand):
    help = 'Create roadmap categories and items for technical skills tracking'

    def handle(self, *args, **options):
        # Create roadmap categories
        categories_data = [
            {
                'name': 'Programming Languages',
                'description': 'Essential programming languages for software development',
                'icon': 'fas fa-code',
                'order': 1,
                'items': [
                    {'title': 'Python Fundamentals', 'difficulty': 'beginner', 'estimated_hours': 40, 'description': 'Learn Python basics, data types, control flow, functions, and basic OOP concepts.'},
                    {'title': 'Python Advanced Concepts', 'difficulty': 'intermediate', 'estimated_hours': 60, 'description': 'Master decorators, generators, context managers, metaclasses, and advanced OOP.'},
                    {'title': 'Python Web Development', 'difficulty': 'intermediate', 'estimated_hours': 50, 'description': 'Build web applications using Django, Flask, or FastAPI frameworks.'},
                    {'title': 'Python Data Science', 'difficulty': 'advanced', 'estimated_hours': 80, 'description': 'Learn NumPy, Pandas, Matplotlib, and machine learning basics with Python.'},
                    {'title': 'JavaScript Basics', 'difficulty': 'beginner', 'estimated_hours': 30, 'description': 'Learn JavaScript fundamentals, DOM manipulation, and basic web interactions.'},
                    {'title': 'JavaScript Advanced', 'difficulty': 'intermediate', 'estimated_hours': 50, 'description': 'Master async programming, closures, prototypes, and modern ES6+ features.'},
                    {'title': 'TypeScript', 'difficulty': 'intermediate', 'estimated_hours': 40, 'description': 'Learn TypeScript for type-safe JavaScript development.'},
                    {'title': 'Java Fundamentals', 'difficulty': 'beginner', 'estimated_hours': 50, 'description': 'Learn Java syntax, OOP concepts, and basic application development.'},
                    {'title': 'Java Enterprise', 'difficulty': 'advanced', 'estimated_hours': 80, 'description': 'Master Spring Boot, microservices, and enterprise Java patterns.'},
                ]
            },
            {
                'name': 'Web Development',
                'description': 'Frontend and backend web technologies',
                'icon': 'fas fa-globe',
                'order': 2,
                'items': [
                    {'title': 'HTML5 & CSS3', 'difficulty': 'beginner', 'estimated_hours': 30, 'description': 'Master semantic HTML and modern CSS including Flexbox and Grid.'},
                    {'title': 'Responsive Design', 'difficulty': 'intermediate', 'estimated_hours': 25, 'description': 'Learn mobile-first design and media queries for all devices.'},
                    {'title': 'CSS Frameworks', 'difficulty': 'intermediate', 'estimated_hours': 35, 'description': 'Master Bootstrap, Tailwind CSS, or other CSS frameworks.'},
                    {'title': 'React.js', 'difficulty': 'intermediate', 'estimated_hours': 60, 'description': 'Build dynamic user interfaces with React.js and hooks.'},
                    {'title': 'Vue.js', 'difficulty': 'intermediate', 'estimated_hours': 50, 'description': 'Learn Vue.js for progressive web applications.'},
                    {'title': 'Angular', 'difficulty': 'advanced', 'estimated_hours': 70, 'description': 'Master Angular framework for enterprise applications.'},
                    {'title': 'Node.js', 'difficulty': 'intermediate', 'estimated_hours': 45, 'description': 'Build server-side applications with Node.js and Express.'},
                    {'title': 'REST APIs', 'difficulty': 'intermediate', 'estimated_hours': 40, 'description': 'Design and build RESTful APIs and services.'},
                    {'title': 'GraphQL', 'difficulty': 'advanced', 'estimated_hours': 35, 'description': 'Learn GraphQL for efficient API queries.'},
                ]
            },
            {
                'name': 'Database Technologies',
                'description': 'Database management and optimization',
                'icon': 'fas fa-database',
                'order': 3,
                'items': [
                    {'title': 'SQL Fundamentals', 'difficulty': 'beginner', 'estimated_hours': 35, 'description': 'Learn basic SQL queries, joins, and database design principles.'},
                    {'title': 'MySQL/PostgreSQL', 'difficulty': 'intermediate', 'estimated_hours': 45, 'description': 'Master popular relational database systems.'},
                    {'title': 'Database Design', 'difficulty': 'intermediate', 'estimated_hours': 40, 'description': 'Learn normalization, indexing, and performance optimization.'},
                    {'title': 'NoSQL Databases', 'difficulty': 'intermediate', 'estimated_hours': 35, 'description': 'Work with MongoDB, Redis, and other NoSQL systems.'},
                    {'title': 'Database Administration', 'difficulty': 'advanced', 'estimated_hours': 50, 'description': 'Learn backup, recovery, security, and monitoring.'},
                    {'title': 'ORM Frameworks', 'difficulty': 'intermediate', 'estimated_hours': 30, 'description': 'Master Django ORM, SQLAlchemy, or similar frameworks.'},
                ]
            },
            {
                'name': 'DevOps & Cloud',
                'description': 'Development operations and cloud platforms',
                'icon': 'fas fa-cloud',
                'order': 4,
                'items': [
                    {'title': 'Git & GitHub', 'difficulty': 'beginner', 'estimated_hours': 20, 'description': 'Version control fundamentals and collaborative development.'},
                    {'title': 'Linux Basics', 'difficulty': 'beginner', 'estimated_hours': 30, 'description': 'Essential Linux commands and shell scripting.'},
                    {'title': 'Docker', 'difficulty': 'intermediate', 'estimated_hours': 40, 'description': 'Containerization and Docker orchestration.'},
                    {'title': 'Kubernetes', 'difficulty': 'advanced', 'estimated_hours': 60, 'description': 'Container orchestration and microservices management.'},
                    {'title': 'AWS Fundamentals', 'difficulty': 'intermediate', 'estimated_hours': 50, 'description': 'Learn core AWS services and cloud architecture.'},
                    {'title': 'CI/CD Pipelines', 'difficulty': 'advanced', 'estimated_hours': 45, 'description': 'Automated testing, building, and deployment.'},
                    {'title': 'Infrastructure as Code', 'difficulty': 'advanced', 'estimated_hours': 40, 'description': 'Terraform, CloudFormation, and IaC principles.'},
                ]
            },
            {
                'name': 'Software Testing',
                'description': 'Quality assurance and testing methodologies',
                'icon': 'fas fa-bug',
                'order': 5,
                'items': [
                    {'title': 'Unit Testing', 'difficulty': 'intermediate', 'estimated_hours': 30, 'description': 'Write effective unit tests using frameworks like pytest or JUnit.'},
                    {'title': 'Integration Testing', 'difficulty': 'intermediate', 'estimated_hours': 35, 'description': 'Test component interactions and system integration.'},
                    {'title': 'End-to-End Testing', 'difficulty': 'advanced', 'estimated_hours': 40, 'description': 'Automated testing of complete user workflows.'},
                    {'title': 'Performance Testing', 'difficulty': 'advanced', 'estimated_hours': 45, 'description': 'Load testing, stress testing, and optimization.'},
                    {'title': 'Test Automation', 'difficulty': 'intermediate', 'estimated_hours': 35, 'description': 'Selenium, Cypress, or other automation frameworks.'},
                ]
            },
            {
                'name': 'Mobile Development',
                'description': 'iOS and Android app development',
                'icon': 'fas fa-mobile-alt',
                'order': 6,
                'items': [
                    {'title': 'React Native', 'difficulty': 'intermediate', 'estimated_hours': 60, 'description': 'Build cross-platform mobile apps with React Native.'},
                    {'title': 'Flutter', 'difficulty': 'intermediate', 'estimated_hours': 55, 'description': 'Develop mobile apps using Flutter and Dart.'},
                    {'title': 'iOS Development', 'difficulty': 'advanced', 'estimated_hours': 80, 'description': 'Native iOS app development with Swift.'},
                    {'title': 'Android Development', 'difficulty': 'advanced', 'estimated_hours': 80, 'description': 'Native Android app development with Kotlin/Java.'},
                ]
            },
            {
                'name': 'AI & Machine Learning',
                'description': 'Artificial intelligence and ML technologies',
                'icon': 'fas fa-brain',
                'order': 7,
                'items': [
                    {'title': 'Machine Learning Basics', 'difficulty': 'intermediate', 'estimated_hours': 60, 'description': 'Supervised and unsupervised learning fundamentals.'},
                    {'title': 'Deep Learning', 'difficulty': 'advanced', 'estimated_hours': 80, 'description': 'Neural networks, CNNs, RNNs, and transformers.'},
                    {'title': 'TensorFlow/PyTorch', 'difficulty': 'advanced', 'estimated_hours': 70, 'description': 'Master popular ML frameworks.'},
                    {'title': 'NLP Fundamentals', 'difficulty': 'advanced', 'estimated_hours': 65, 'description': 'Natural language processing and text analysis.'},
                    {'title': 'Computer Vision', 'difficulty': 'expert', 'estimated_hours': 75, 'description': 'Image processing and computer vision applications.'},
                ]
            },
            {
                'name': 'Cybersecurity',
                'description': 'Security best practices and ethical hacking',
                'icon': 'fas fa-shield-alt',
                'order': 8,
                'items': [
                    {'title': 'Security Fundamentals', 'difficulty': 'intermediate', 'estimated_hours': 40, 'description': 'Basic security concepts and common vulnerabilities.'},
                    {'title': 'Web Security', 'difficulty': 'advanced', 'estimated_hours': 50, 'description': 'OWASP top 10 and web application security.'},
                    {'title': 'Network Security', 'difficulty': 'advanced', 'estimated_hours': 55, 'description': 'Network protocols, firewalls, and intrusion detection.'},
                    {'title': 'Cryptography', 'difficulty': 'expert', 'estimated_hours': 60, 'description': 'Encryption, digital signatures, and secure communication.'},
                ]
            },
        ]

        # Create categories and items
        for cat_data in categories_data:
            category, created = RoadmapCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'order': cat_data['order']
                }
            )
            
            if created:
                self.stdout.write(f"Created category: {category.name}")
            
            # Create items for this category
            for item_data in cat_data['items']:
                item, created = RoadmapItem.objects.get_or_create(
                    category=category,
                    title=item_data['title'],
                    defaults={
                        'description': item_data['description'],
                        'difficulty': item_data['difficulty'],
                        'estimated_hours': item_data['estimated_hours'],
                        'order': len(RoadmapItem.objects.filter(category=category)) + 1
                    }
                )
                
                if created:
                    self.stdout.write(f"  Created item: {item.title}")
        
        self.stdout.write(self.style.SUCCESS('Roadmap data created successfully!'))
