from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import json
from apps.skills.models import UserSkill, Skill, SkillCategory, UserRoadmapProgress
from apps.jobs.models import Job
from .models import Internship, UserInternship, SavedInternship


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your context data here
        context['page_title'] = 'Home'
        context['page_description'] = 'Welcome to Career Forge'
        return context


def dashboard(request):
    return render(request, 'core/dashboard.html')


def certification_recommendations(request):
    """
    Certification Recommendations Page
    Displays industry-recognized certifications from top providers
    """
    from apps.certifications.models import Certification

    demand_weights = {
        'Cloud Computing': 95, 'AI & Machine Learning': 92, 'Data Science': 90,
        'Cybersecurity': 88, 'DevOps': 85, 'Software Development': 82,
        'Project Management': 75, 'Digital Marketing': 70,
    }

    certifications = Certification.objects.filter(is_active=True, is_synced=True)
    recommendations = []
    for cert in certifications:
        recommendations.append({
            'id': cert.id,
            'name': cert.name,
            'provider': cert.provider,
            'domain': cert.domain,
            'description': cert.description,
            'rating': cert.rating,
            'duration': cert.duration,
            'difficulty_level': cert.difficulty_level,
            'get_difficulty_level_display': cert.get_difficulty_level_display(),
            'registration_url': cert.registration_url,
            'demand_score': demand_weights.get(cert.domain, 65),
        })
    recommendations.sort(key=lambda x: x['demand_score'], reverse=True)

    providers = [
        {'key': p, 'name': p.capitalize(),
         'status': 'active' if Certification.objects.filter(provider=p).exists() else 'pending',
         'count': Certification.objects.filter(provider=p, is_active=True).count(),
         'last_updated': Certification.objects.filter(provider=p).order_by('-last_updated').first().last_updated
                         if Certification.objects.filter(provider=p).exists() else None}
        for p in ['coursera', 'aws', 'google', 'microsoft', 'cisco']
    ]

    context = {
        'total_certifications': Certification.objects.filter(is_active=True).count(),
        'active_certifications': Certification.objects.filter(is_active=True, is_synced=True).count(),
        'providers_count': Certification.objects.values('provider').distinct().count(),
        'last_sync': Certification.objects.order_by('-last_updated').first().last_updated
                     if Certification.objects.exists() else None,
        'providers': providers,
        'recommendations': recommendations[:20],
    }
    return render(request, 'core/certification.html', context)


def skill_gap_analysis(request):
    """
    Skill Gap Analysis Page - PAGE 2
    Displays market benchmark analysis, skill gap identification,
    and personalized learning paths for skill development
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # For unauthenticated users, show empty data or redirect to login
        context = {
            'page_title': 'Skill Gap Analysis',
            'page_description': 'Market Comparison & Priority Mapping',
            'user_skills_json': json.dumps([]),
            'categories_json': json.dumps([]),
            'user_email': 'guest@example.com',
        }
        return render(request, 'core/skillgap.html', context)
    
    user = request.user
    
    # Get user's actual skills from database
    user_skills = UserSkill.objects.filter(user=user).select_related('skill', 'skill__category')
    
    # Convert user skills to JSON-serializable format
    user_skills_data = []
    for us in user_skills:
        user_skills_data.append({
            'skill_id': us.skill.id,
            'skill_name': us.skill.name,
            'category': us.skill.category.name,
            'skill_type': us.skill.skill_type,
            'proficiency_level': us.proficiency_level,
            'proficiency_numeric': _get_proficiency_numeric(us.proficiency_level),
            'years_experience': float(us.years_experience),  # Convert Decimal to float
            'is_verified': us.is_verified
        })
    
    # Get skill categories for filtering
    categories = SkillCategory.objects.all()
    categories_data = [{'id': cat.id, 'name': cat.name} for cat in categories]
    
    context = {
        'page_title': 'Skill Gap Analysis',
        'page_description': 'Market Comparison & Priority Mapping',
        'user_skills_json': json.dumps(user_skills_data),
        'categories_json': json.dumps(categories_data),
        'user_email': user.email,
    }
    return render(request, 'core/skillgap.html', context)


def _get_proficiency_numeric(proficiency_level):
    """Convert proficiency level string to numeric value"""
    level_map = {
        'beginner': 1,
        'intermediate': 2,
        'advanced': 3,
        'expert': 4
    }
    return level_map.get(proficiency_level.lower(), 0)


@require_http_methods(["POST"])
def get_role_requirements(request):
    """
    API endpoint to fetch job requirements by role title and get comparison
    Compares user skills with job/role requirements
    """
    try:
        data = json.loads(request.body)
        role_title = data.get('role_title', '').strip()
        experience_level = data.get('experience_level', '').strip()
        industry = data.get('industry', '').strip()
        
        # Fetch jobs matching criteria
        jobs_query = Job.objects.filter(is_active=True)
        
        if role_title:
            jobs_query = jobs_query.filter(title__icontains=role_title)
        if experience_level:
            jobs_query = jobs_query.filter(experience_level=experience_level)
        
        # Get the first matching job as the benchmark
        job = jobs_query.first()
        
        required_skills_data = []
        preferred_skills_data = []
        
        if job:
            job_title = job.title
            company = job.company.name if job.company else 'Unknown'
            exp_level_display = job.get_experience_level_display()
            source = 'job_database'
            trend = 'Active hiring based on live job database matches.'
            
            for skill in job.skills_required.all():
                required_skills_data.append({
                    'skill_id': skill.id,
                    'skill_name': skill.name,
                    'skill_type': skill.skill_type,
                    'category': skill.category.name,
                    'requirement_level': 'required',
                    'requirement_description': f'{skill.name}: Level 3 (Advanced) - Required',
                    'recommended_proficiency': 'advanced'
                })
                
            for skill in job.skills_preferred.all():
                preferred_skills_data.append({
                    'skill_id': skill.id,
                    'skill_name': skill.name,
                    'skill_type': skill.skill_type,
                    'category': skill.category.name,
                    'requirement_level': 'preferred',
                    'requirement_description': f'{skill.name} - Preferred',
                    'recommended_proficiency': 'intermediate'
                })
        else:
            # Fallback to generic benchmark
            generic_data = _get_generic_benchmark(role_title, experience_level)
            job_title = generic_data['job_title']
            company = 'Aggregated Market Data'
            exp_level_display = generic_data['experience_level']
            source = 'benchmark'
            trend = generic_data.get('trend', 'Standard industry growth projected.')
            
            required_skills_data = generic_data['required_skills']
            preferred_skills_data = generic_data['preferred_skills']

        # Get user's skills
        user = request.user
        user_skills_dict = {}
        user_skills = UserSkill.objects.filter(user=user).select_related('skill')
        for us in user_skills:
            # Use lowercase for flexible matching
            user_skills_dict[us.skill.name.lower()] = {
                'id': us.skill.id,
                'name': us.skill.name,
                'proficiency_level': us.proficiency_level,
                'proficiency_numeric': _get_proficiency_numeric(us.proficiency_level),
                'years_experience': float(us.years_experience),  # Convert Decimal to float
                'is_verified': us.is_verified
            }
        
        # Build comparison data
        benchmark_data = {
            'job_title': job_title,
            'company': company,
            'experience_level': exp_level_display,
            'trend': trend,
            'required_skills': [],
            'preferred_skills': [],
            'met_skills': [],
            'missing_skills': [],
            'proficiency_gaps': [],
            'emerging_skills': [],
            'met_count': 0,
            'gap_count': 0,
            'missing_count': 0
        }
        
        # Process required skills
        for skill_data in required_skills_data:
            skill_name_lower = skill_data['skill_name'].lower()
            
            if skill_name_lower in user_skills_dict:
                user_skill = user_skills_dict[skill_name_lower]
                skill_data['user_proficiency'] = user_skill['proficiency_level']
                skill_data['user_proficiency_numeric'] = user_skill['proficiency_numeric']
                skill_data['user_years_experience'] = user_skill['years_experience']
                skill_data['is_verified'] = user_skill['is_verified']
                
                # Minimum required numeric level logic
                req_level_str = skill_data.get('recommended_proficiency', 'advanced')
                req_num = _get_proficiency_numeric(req_level_str) or 3
                
                # Check if meets requirement
                if user_skill['proficiency_numeric'] >= req_num:
                    benchmark_data['met_skills'].append(skill_data)
                    benchmark_data['met_count'] += 1
                else:
                    skill_data['gap_level'] = req_num - user_skill['proficiency_numeric']
                    benchmark_data['proficiency_gaps'].append(skill_data)
                    benchmark_data['gap_count'] += 1
            else:
                skill_data['user_proficiency'] = 'none'
                skill_data['user_proficiency_numeric'] = 0
                benchmark_data['missing_skills'].append(skill_data)
                benchmark_data['missing_count'] += 1
            
            benchmark_data['required_skills'].append(skill_data)
        
        # Process preferred skills (emerging skills)
        for skill_data in preferred_skills_data:
            skill_name_lower = skill_data['skill_name'].lower()
            
            if skill_name_lower in user_skills_dict:
                user_skill = user_skills_dict[skill_name_lower]
                skill_data['user_proficiency'] = user_skill['proficiency_level']
                skill_data['user_proficiency_numeric'] = user_skill['proficiency_numeric']
            else:
                skill_data['user_proficiency'] = 'none'
                skill_data['user_proficiency_numeric'] = 0
                benchmark_data['emerging_skills'].append(skill_data)
            
            benchmark_data['preferred_skills'].append(skill_data)
        
        return JsonResponse({
            'status': 'success',
            'source': source,
            'job_title': job_title,
            'benchmark': benchmark_data
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)  # Changed status code from 500 to 400


def simple_internship_view(request):
    """Simple test view without authentication"""
    from django.http import HttpResponse
    from django.template import loader
    
    template = loader.get_template('core/internship.html')
    context = {
        'page_title': 'Internship Finder - Test',
        'page_description': 'Test page without database dependencies',
    }
    return HttpResponse(template.render(context, request))


def internship_finder(request):
    """
    Internship Finder Page - Live internship search across multiple platforms
    Integrates with Remotive, Adzuna, LinkedIn, AngelList, Indeed, Glassdoor, and company career pages
    """
    context = {
        'page_title': 'Internship Finder',
        'page_description': 'Search internships across top companies worldwide',
    }
    return render(request, 'core/internship.html', context)


def _get_generic_benchmark(role_title, experience_level):
    """
    Generate generic benchmark data based on role title and experience level
    """
    # Map role titles to typical required skills
    role_skill_mapping = {
        'ui/ux': {
            'required': ['React', 'JavaScript', 'TypeScript', 'System Design', 'State Management'],
            'preferred': ['Node.js', 'Docker', 'AWS', 'GraphQL', 'Testing Frameworks'],
            'trend': 'High Demand (15% YoY growth). Emphasis is shifting heavily towards TypeScript and State Management mastery.'
        },
        'designer': {
            'required': ['React', 'JavaScript', 'TypeScript', 'System Design', 'State Management'],
            'preferred': ['Node.js', 'Docker', 'AWS', 'GraphQL', 'Testing Frameworks'],
            'trend': 'Growing need for technical designers bridging gap between UI and frontend architectures.'
        },
        'data analyst': { # Specifically tailored to user's request for React/TS heavy Data Analyst
            'required': ['React', 'JavaScript', 'TypeScript', 'System Design', 'State Management'],
            'preferred': ['Docker', 'GraphQL', 'Node.js'],
            'trend': 'Heavy transition towards unified full-stack reporting with State Management.'
        },
        'senior react': {
            'required': ['React', 'JavaScript', 'TypeScript', 'System Design', 'State Management'],
            'preferred': ['Node.js', 'Docker', 'AWS', 'GraphQL', 'Testing Frameworks'],
            'trend': 'High demand for scalable component architectures and strong TS fundamentals.'
        },
        'react': {
            'required': ['React', 'JavaScript', 'HTML/CSS', 'Git'],
            'preferred': ['TypeScript', 'Node.js', 'REST API', 'Testing'],
            'trend': 'Steady requirement for core React ecosystem engineers.'
        },
        'full stack': {
            'required': ['JavaScript', 'React', 'Node.js', 'Database', 'REST API'],
            'preferred': ['TypeScript', 'Docker', 'AWS', 'Git', 'DevOps'],
            'trend': 'Full stack capabilities remain standard, with cloud deployment (AWS/Docker) becoming crucial.'
        },
        'backend': {
            'required': ['Python', 'Node.js', 'Database', 'REST API', 'Git'],
            'preferred': ['Docker', 'Kubernetes', 'Microservices', 'System Design'],
            'trend': 'Microservices and Kubernetes containerization are defining modern backend roles.'
        },
        'data scientist': {
            'required': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Processing'],
            'preferred': ['TensorFlow', 'PyTorch', 'Big Data', 'Cloud Platforms'],
            'trend': 'AI modeling and Large Language Model integration are the fastest-growing sub-sectors.'
        },
        'devops': {
            'required': ['Docker', 'Kubernetes', 'CI/CD', 'AWS', 'Linux'],
            'preferred': ['Terraform', 'Python', 'Bash', 'Prometheus'],
            'trend': 'Infrastructure as Code (IaC) is now a mandatory requirement for mid-level DevOps.'
        },
        'cloud': {
            'required': ['AWS', 'Docker', 'System Design', 'Networking', 'Security'],
            'preferred': ['Kubernetes', 'Terraform', 'Azure', 'Python'],
            'trend': 'Multi-cloud architectures and hybrid deployments are becoming more common.'
        }
    }
    
    # Find matching role
    matched_role = None
    for key in role_skill_mapping:
        if key.lower() in role_title.lower():
            matched_role = role_skill_mapping[key]
            break
    
    if not matched_role:
        matched_role = role_skill_mapping.get('senior react', role_skill_mapping['senior react'])
    
    # Calculate proficiency levels based on experience
    level_map = {
        'entry': 'intermediate',
        'fresher': 'intermediate',
        'junior': 'intermediate',
        'mid': 'advanced',
        'senior': 'advanced',
        'lead': 'expert'
    }
    recommended_level = 'advanced' # Default
    for key, val in level_map.items():
        if key in experience_level.lower():
            recommended_level = val
            break
    
    return {
        'job_title': role_title or 'Senior Developer',
        'experience_level': experience_level or 'Senior Level',
        'required_skills': [
            {'skill_name': s, 'requirement_level': 'required', 'recommended_proficiency': recommended_level, 'skill_type': 'Core', 'category': 'Technical'}
            for s in matched_role.get('required', [])
        ],
        'preferred_skills': [
            {'skill_name': s, 'requirement_level': 'preferred', 'recommended_proficiency': 'intermediate', 'skill_type': 'Additional', 'category': 'Technical'}
            for s in matched_role.get('preferred', [])
        ],
        'trend': matched_role.get('trend', 'Standard industry growth projected.')
    }


def progress_tracking(request):
    """
    Progress Tracking & Career Insights Page
    Collects and displays comprehensive progress data from profile, skill gap analysis, 
    certifications, tests, and learning activities
    """
    user = request.user
    
    # Get user's skills from database
    user_skills = UserSkill.objects.filter(user=user).select_related('skill', 'skill__category')
    
    # If no database skills, try to get from profile localStorage data
    if not user_skills.exists():
        # Create sample data for demonstration based on typical user profile
        from apps.skills.models import Skill, SkillCategory
        
        # Get or create categories
        tech_category, _ = SkillCategory.objects.get_or_create(name='Technical', defaults={'description': 'Technical skills'})
        soft_category, _ = SkillCategory.objects.get_or_create(name='Soft Skills', defaults={'description': 'Soft skills'})
        domain_category, _ = SkillCategory.objects.get_or_create(name='Domain', defaults={'description': 'Domain knowledge'})
        
        # Sample skills based on your profile showing 16 skills
        sample_skills_data = [
            # Technical Skills (12 skills)
            ('JavaScript', 'advanced', tech_category, 3, True),
            ('React', 'advanced', tech_category, 3, True),
            ('TypeScript', 'intermediate', tech_category, 2, True),
            ('Node.js', 'intermediate', tech_category, 2, False),
            ('Python', 'intermediate', tech_category, 2, True),
            ('HTML/CSS', 'advanced', tech_category, 3, True),
            ('Git', 'advanced', tech_category, 3, True),
            ('REST APIs', 'intermediate', tech_category, 2, True),
            ('MongoDB', 'beginner', tech_category, 1, False),
            ('Docker', 'beginner', tech_category, 1, False),
            ('AWS', 'beginner', tech_category, 1, False),
            ('GraphQL', 'beginner', tech_category, 1, False),
            # Soft Skills (2 skills)
            ('Communication', 'advanced', soft_category, 3, True),
            ('Teamwork', 'advanced', soft_category, 3, True),
            # Domain Skills (2 skills)
            ('E-commerce', 'intermediate', domain_category, 2, True),
            ('Web Development', 'advanced', domain_category, 3, True),
        ]
        
        skill_type_mapping = {
            tech_category: 'technical',
            soft_category: 'soft', 
            domain_category: 'domain'
        }
        
        for skill_name, proficiency, category, years, verified in sample_skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_name,
                defaults={
                    'category': category,
                    'skill_type': skill_type_mapping[category],
                    'description': f'{skill_name} skill'
                }
            )
            
            UserSkill.objects.get_or_create(
                user=user,
                skill=skill,
                defaults={
                    'proficiency_level': proficiency,
                    'years_experience': years,
                    'is_verified': verified
                }
            )
        
        # Refresh the query
        user_skills = UserSkill.objects.filter(user=user).select_related('skill', 'skill__category')
    
    # Get user's certifications (sample data for now)
    user_certifications = [
        {'name': 'React Developer', 'issuer': 'Meta', 'date': '2024-01-15', 'status': 'active'},
        {'name': 'JavaScript Advanced', 'issuer': 'Coursera', 'date': '2023-11-20', 'status': 'active'}
    ]
    
    # Get test results (sample data based on skills)
    test_results = []
    for user_skill in user_skills[:5]:  # Top 5 skills
        years_exp = float(user_skill.years_experience)  # Convert Decimal to float
        test_results.append({
            'skill': user_skill.skill.name,
            'score': 75 + (years_exp * 5),  # Score based on experience
            'date': '2024-03-15',
            'percentile': 60 + (years_exp * 8)
        })
    
    # Get learning activities (sample data)
    learning_activities = [
        {'type': 'skill_added', 'name': f'Added {user_skills.first().skill.name if user_skills.exists() else "JavaScript"} skill', 'date': '2024-03-18', 'progress': 100},
        {'type': 'profile_updated', 'name': 'Updated profile information', 'date': '2024-03-15', 'progress': 100},
        {'type': 'skill_verified', 'name': f'Verified {user_skills.filter(is_verified=True).first().skill.name if user_skills.filter(is_verified=True).exists() else "React"} skill', 'date': '2024-03-10', 'progress': 100}
    ]
    
    # Get user's goals (sample data)
    user_goals = [
        {'title': 'Master TypeScript', 'type': 'short', 'targetDate': '2024-04-15', 'progress': 60, 'skills': ['TypeScript']},
        {'title': 'Complete Full Stack Project', 'type': 'short', 'targetDate': '2024-04-30', 'progress': 30, 'skills': ['React', 'Node.js']},
        {'title': 'Get AWS Certified', 'type': 'medium', 'targetDate': '2024-06-30', 'progress': 25, 'skills': ['AWS']},
        {'title': 'Master System Design', 'type': 'medium', 'targetDate': '2024-07-31', 'progress': 40, 'skills': ['System Design']}
    ]
    
    # Prepare skill data for charts
    skills_by_category = {}
    for us in user_skills:
        category = us.skill.category.name
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append({
            'name': us.skill.name,
            'proficiency': us.proficiency_level,
            'proficiency_numeric': _get_proficiency_numeric(us.proficiency_level),
            'years_experience': float(us.years_experience),  # Convert Decimal to float
            'is_verified': us.is_verified
        })
    
    # Calculate skill statistics
    total_skills = len(user_skills)
    verified_skills = len([us for us in user_skills if us.is_verified])
    avg_proficiency = sum(_get_proficiency_numeric(us.proficiency_level) for us in user_skills) / total_skills if total_skills > 0 else 0
    
    # Prepare context data
    context = {
        'page_title': 'Progress Tracking & Career Insights',
        'page_description': 'Monitor your skill growth, track learning progress, and get personalized career recommendations',
        'user_skills_json': json.dumps([
            {
                'skill_name': us.skill.name,
                'proficiency_level': us.proficiency_level,
                'proficiency_numeric': _get_proficiency_numeric(us.proficiency_level),
                'years_experience': float(us.years_experience),  # Convert Decimal to float
                'is_verified': us.is_verified,
                'skill_name': us.skill.name,  # For compatibility
                'skill_type': us.skill.skill_type
            } for us in user_skills
        ]),
        'skills_by_category_json': json.dumps(skills_by_category),
        'total_skills': total_skills,
        'verified_skills': verified_skills,
        'avg_proficiency': round(avg_proficiency, 1),
        'user_email': user.email,
        'test_results_json': json.dumps(test_results),
        'certifications_json': json.dumps(user_certifications),
        'learning_activities_json': json.dumps(learning_activities),
        'goals_json': json.dumps(user_goals),
    }
    
    return render(request, 'core/progress_tracking.html', context)


def ai_mock_interview(request):
    """
    AI Mock Interview Page - Real LLM Powered Interview Practice
    Interactive mock interviews with personalized feedback using Gemini API
    """
    context = {
        'page_title': 'AI Mock Interview',
        'page_description': 'Practice interviews with real AI-powered feedback and analysis',
    }
    return render(request, 'core/aimockinterview.html', context)


def roadmap(request):
    """
    Skill Roadmap Page - Choose Your Career Path
    Interactive career roadmaps with comprehensive skill tracking and learning resources
    """
    context = {
        'page_title': 'Skill Roadmap',
        'page_description': 'Choose your career path and follow comprehensive skill roadmaps with learning resources',
    }
    return render(request, 'core/roadmap.html', context)


def technical_assessment(request):
    """
    Technical Assessment Page - Comprehensive Technical Test Engine
    Interactive technical tests with timer, progress tracking, and detailed scoring
    """
    context = {
        'page_title': 'Technical Assessment Engine',
        'page_description': 'Test your technical knowledge with comprehensive questions across multiple subjects and difficulty levels',
    }
    return render(request, 'core/technical.html', context)


def resume_builder(request):
    """
    Smart ATS Resume Builder Page - Drag & Drop Resume Builder
    Interactive resume builder with ATS optimization, templates, and export functionality
    """
    context = {
        'page_title': 'Smart ATS Resume Builder',
        'page_description': 'Build professional resumes with drag & drop sections, ATS optimization, and multiple templates',
    }
    return render(request, 'core/resume_builder.html', context)


def aptitude_test(request):
    """
    Aptitude & Reasoning Test Page - 150+ Questions Pool
    Comprehensive aptitude test with quantitative, verbal, logical reasoning, data interpretation, and abstract reasoning
    """
    context = {
        'page_title': 'Aptitude & Reasoning Tests',
        'page_description': '150+ curated questions across 5 sections with multiple difficulty levels',
    }
    return render(request, 'core/aptitude.html', context)


def my_internships(request):
    """
    My Internships Page - Display user's enrolled, completed, and saved internships
    """
    from django.http import JsonResponse
    
    user = request.user
    
    # Return JSON for API requests
    if request.headers.get('Accept') == 'application/json' or request.path.startswith('/api/'):
        return JsonResponse({
            'enrolled': [],
            'in_progress': [],
            'completed': [],
            'saved': []
        })
    
    context = {
        'page_title': 'My Internships',
        'page_description': 'Track your internship journey from enrollment to completion',
        'enrolled_internships': [],
        'completed_internships': [],
        'in_progress_internships': [],
        'saved_internships': [],
        'stats': {
            'total_enrolled': 0,
            'completed': 0,
            'in_progress': 0,
            'saved': 0,
        },
    }
    return render(request, 'core/my_internships.html', context)


@require_http_methods(["POST"])
def enroll_internship(request, internship_id):
    """
    Enroll user in an internship
    """
    try:
        from django.shortcuts import get_object_or_404
        from .models import Internship
        
        internship = get_object_or_404(Internship, id=internship_id)
        user = request.user

        # Check if already enrolled
        from .models import UserInternship
        if UserInternship.objects.filter(user=user, internship=internship).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'You are already enrolled in this internship'
            }, status=400)

        # Create enrollment
        enrollment = UserInternship.objects.create(
            user=user,
            internship=internship,
            status='enrolled'
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Successfully enrolled in internship!',
            'enrollment_id': enrollment.id
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@require_http_methods(["POST"])
def update_internship_status(request, enrollment_id):
    """
    Update internship status (enrolled -> in_progress -> completed)
    """
    try:
        from django.shortcuts import get_object_or_404
        from .models import UserInternship
        from django.utils import timezone
        import json
        
        data = json.loads(request.body)
        new_status = data.get('status')
        notes = data.get('notes', '')
        skills_gained = data.get('skills_gained', '')
        experience_rating = data.get('experience_rating')
        would_recommend = data.get('would_recommend')

        enrollment = get_object_or_404(UserInternship, id=enrollment_id, user=request.user)

        # Update status
        enrollment.status = new_status
        enrollment.notes = notes
        enrollment.skills_gained = skills_gained

        if experience_rating is not None:
            enrollment.experience_rating = int(experience_rating)
        if would_recommend is not None:
            enrollment.would_recommend = would_recommend.lower() == 'true'

        # Set completion date if completed
        if new_status == 'completed':
            enrollment.completion_date = timezone.now()

        enrollment.save()

        return JsonResponse({
            'status': 'success',
            'message': f'Internship status updated to {new_status}'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@require_http_methods(["POST"])
def save_internship(request, internship_id):
    """
    Save an internship for later application
    """
    try:
        from django.shortcuts import get_object_or_404
        from .models import Internship, SavedInternship
        
        internship = get_object_or_404(Internship, id=internship_id)
        user = request.user

        # Check if already saved
        if SavedInternship.objects.filter(user=user, internship=internship).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Internship already saved'
            }, status=400)

        # Create saved internship
        saved = SavedInternship.objects.create(
            user=user,
            internship=internship
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Internship saved successfully!',
            'saved_id': saved.id
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@require_http_methods(["DELETE"])
def unsave_internship(request, internship_id):
    """
    Remove saved internship
    """
    try:
        from django.shortcuts import get_object_or_404
        from .models import Internship, SavedInternship
        
        internship = get_object_or_404(Internship, id=internship_id)
        user = request.user

        saved = SavedInternship.objects.filter(user=user, internship=internship).first()
        if saved:
            saved.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Internship removed from saved list'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Internship not found in saved list'
            }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@require_http_methods(["GET"])
def get_internship_stats(request):
    """
    Get user's internship statistics
    """
    try:
        from .models import UserInternship, SavedInternship
        
        user = request.user

        enrollments = UserInternship.objects.filter(user=user)
        saved = SavedInternship.objects.filter(user=user)

        stats = {
            'total_enrolled': enrollments.count(),
            'completed': enrollments.filter(status='completed').count(),
            'in_progress': enrollments.filter(status='in_progress').count(),
            'saved': saved.count(),
            'completion_rate': 0
        }

        if stats['total_enrolled'] > 0:
            stats['completion_rate'] = round((stats['completed'] / stats['total_enrolled']) * 100, 1)

        return JsonResponse({
            'status': 'success',
            'stats': stats
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
