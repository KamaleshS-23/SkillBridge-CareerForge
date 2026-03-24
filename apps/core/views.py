from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import TemplateView
import json
from datetime import datetime, timedelta
from django.utils import timezone
import json
from apps.skills.models import UserSkill, Skill, SkillCategory, UserRoadmapProgress, TechnicalTestResult
from apps.jobs.models import Job
from .models import Internship, UserInternship, SavedInternship, AptitudeTestResult
from . import profile_api

# Make technical test functions available
@login_required
@require_http_methods(["POST"])
def submit_technical_test(request):
    """
    Save technical test results to database
    Expects: {subject, difficulty, score, total_questions, percentage, grade, correct_answers, incorrect_answers, time_taken}
    """
    try:
        data = json.loads(request.body)
        subject = data.get('subject', '').strip()
        difficulty = data.get('difficulty', '').strip()
        score = data.get('score', 0)
        total_questions = data.get('total_questions', 0)
        percentage = data.get('percentage', 0.0)
        grade = data.get('grade', '').strip()
        correct_answers = data.get('correct_answers', [])
        incorrect_answers = data.get('incorrect_answers', [])
        time_taken = data.get('time_taken', None)
        
        if not all([subject, difficulty]):
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields: subject, difficulty'
            }, status=400)
        
        # Create test result record
        test_result = TechnicalTestResult.objects.create(
            user=request.user,
            subject=subject,
            difficulty=difficulty,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            grade=grade,
            correct_answers=json.dumps(correct_answers),
            incorrect_answers=json.dumps(incorrect_answers),
            time_taken=time_taken
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Test results saved successfully',
            'test_id': test_result.id,
            'subject': subject,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
            'grade': grade,
            'test_date': test_result.test_date.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def get_technical_test_results(request):
    """
    Get user's technical test results
    Query params: subject (optional), limit (optional)
    """
    try:
        subject_filter = request.GET.get('subject', '').strip()
        limit = int(request.GET.get('limit', 10))
        
        # Build query
        results_query = TechnicalTestResult.objects.filter(user=request.user)
        
        if subject_filter:
            results_query = results_query.filter(subject__icontains=subject_filter)
        
        # Order by test date and limit
        results = results_query.order_by('-test_date')[:limit]
        
        # Format results
        results_data = []
        for result in results:
            results_data.append({
                'id': result.id,
                'subject': result.subject,
                'difficulty': result.difficulty,
                'score': result.score,
                'total_questions': result.total_questions,
                'percentage': result.percentage,
                'grade': result.grade,
                'correct_answers': json.loads(result.correct_answers) if result.correct_answers else [],
                'incorrect_answers': json.loads(result.incorrect_answers) if result.incorrect_answers else [],
                'time_taken': result.time_taken,
                'test_date': result.test_date.isoformat()
            })
        
        return JsonResponse({
            'status': 'success',
            'results': results_data,
            'total_count': results_query.count(),
            'subject_filter': subject_filter or 'all'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def get_technical_test_stats(request):
    """
    Get user's technical test statistics
    """
    try:
        # Get user's test results
        results = TechnicalTestResult.objects.filter(user=request.user)
        
        # Calculate statistics
        total_tests = results.count()
        total_score = sum(result.score for result in results)
        average_score = total_score / total_tests if total_tests > 0 else 0
        total_correct_answers = sum(json.loads(result.correct_answers).count() for result in results if result.correct_answers)
        total_incorrect_answers = sum(json.loads(result.incorrect_answers).count() for result in results if result.incorrect_answers)
        
        return JsonResponse({
            'status': 'success',
            'total_tests': total_tests,
            'total_score': total_score,
            'average_score': average_score,
            'total_correct_answers': total_correct_answers,
            'total_incorrect_answers': total_incorrect_answers
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


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
        
        # Get first matching job as benchmark
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
        }, status=400)


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
            'trend': 'AI modeling and Large Language Model integration are fastest-growing sub-sectors.'
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


# @login_required  # Temporarily commented for testing
def progress_tracking(request):
    """
    Progress Tracking & Career Insights Page
    Collects and displays comprehensive progress data from profile, skill gap analysis, 
    certifications, tests, and learning activities
    """
    # Handle both authenticated and non-authenticated Users
    if request.user.is_authenticated:
        user = request.user
    else:
        # Create a mock user for testing
        from django.contrib.auth.models import AnonymousUser
        user = type('MockUser', (), {
            'is_authenticated': lambda: True,
            'email': 'test@example.com'
        })()
    
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
        
        # Refresh query
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
                'name': us.skill.name,
                'proficiency': us.proficiency_level,
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
    user = request.user
    
    # Get user's internship enrollments
    enrolled_internships = UserInternship.objects.filter(user=user).select_related('internship')
    completed_internships = enrolled_internships.filter(status='completed')
    in_progress_internships = enrolled_internships.filter(status='in_progress')
    
    # Get saved internships
    saved_internships = SavedInternship.objects.filter(user=user).select_related('internship')
    
    # Prepare statistics
    stats = {
        'total_enrolled': enrolled_internships.count(),
        'completed': completed_internships.count(),
        'in_progress': in_progress_internships.count(),
        'saved': saved_internships.count(),
    }
    
    # Return JSON for API requests
    if request.headers.get('Accept') == 'application/json' or request.path.startswith('/api/'):
        return JsonResponse({
            'enrolled': [
                {
                    'id': enrollment.id,
                    'internship': {
                        'id': enrollment.internship.id,
                        'title': enrollment.internship.title,
                        'company': enrollment.internship.company,
                        'location': enrollment.internship.location,
                        'duration': enrollment.internship.duration,
                        'stipend': enrollment.internship.stipend,
                        'type': enrollment.internship.get_type_display(),
                        'description': enrollment.internship.description,
                        'requirements': enrollment.internship.requirements,
                        'skills_required': enrollment.internship.skills_required,
                        'application_url': enrollment.internship.application_url,
                        'source': enrollment.internship.source,
                        'posted_date': enrollment.internship.posted_date.isoformat(),
                        'deadline': enrollment.internship.deadline.isoformat() if enrollment.internship.deadline else None,
                        'status': enrollment.internship.status,
                        'is_featured': enrollment.internship.is_featured
                    },
                    'status': enrollment.status,
                    'enrollment_date': enrollment.enrollment_date.isoformat(),
                    'completion_date': enrollment.completion_date.isoformat() if enrollment.completion_date else None,
                    'start_date': enrollment.start_date.isoformat() if enrollment.start_date else None,
                    'end_date': enrollment.end_date.isoformat() if enrollment.end_date else None,
                    'notes': enrollment.notes,
                    'skills_gained': enrollment.skills_gained,
                    'experience_rating': enrollment.experience_rating,
                    'would_recommend': enrollment.would_recommend
                }
                for enrollment in enrolled_internships.filter(status='enrolled')
            ],
            'in_progress': [
                {
                    'id': enrollment.id,
                    'internship': {
                        'id': enrollment.internship.id,
                        'title': enrollment.internship.title,
                        'company': enrollment.internship.company,
                        'location': enrollment.internship.location,
                        'duration': enrollment.internship.duration,
                        'stipend': enrollment.internship.stipend,
                        'type': enrollment.internship.get_type_display(),
                        'description': enrollment.internship.description,
                        'requirements': enrollment.internship.requirements,
                        'skills_required': enrollment.internship.skills_required,
                        'application_url': enrollment.internship.application_url,
                        'source': enrollment.internship.source,
                        'posted_date': enrollment.internship.posted_date.isoformat(),
                        'deadline': enrollment.internship.deadline.isoformat() if enrollment.internship.deadline else None,
                        'status': enrollment.internship.status,
                        'is_featured': enrollment.internship.is_featured
                    },
                    'status': enrollment.status,
                    'enrollment_date': enrollment.enrollment_date.isoformat(),
                    'completion_date': enrollment.completion_date.isoformat() if enrollment.completion_date else None,
                    'start_date': enrollment.start_date.isoformat() if enrollment.start_date else None,
                    'end_date': enrollment.end_date.isoformat() if enrollment.end_date else None,
                    'notes': enrollment.notes,
                    'skills_gained': enrollment.skills_gained,
                    'experience_rating': enrollment.experience_rating,
                    'would_recommend': enrollment.would_recommend
                }
                for enrollment in in_progress_internships
            ],
            'completed': [
                {
                    'id': enrollment.id,
                    'internship': {
                        'id': enrollment.internship.id,
                        'title': enrollment.internship.title,
                        'company': enrollment.internship.company,
                        'location': enrollment.internship.location,
                        'duration': enrollment.internship.duration,
                        'stipend': enrollment.internship.stipend,
                        'type': enrollment.internship.get_type_display(),
                        'description': enrollment.internship.description,
                        'requirements': enrollment.internship.requirements,
                        'skills_required': enrollment.internship.skills_required,
                        'application_url': enrollment.internship.application_url,
                        'source': enrollment.internship.source,
                        'posted_date': enrollment.internship.posted_date.isoformat(),
                        'deadline': enrollment.internship.deadline.isoformat() if enrollment.internship.deadline else None,
                        'status': enrollment.internship.status,
                        'is_featured': enrollment.internship.is_featured
                    },
                    'status': enrollment.status,
                    'enrollment_date': enrollment.enrollment_date.isoformat(),
                    'completion_date': enrollment.completion_date.isoformat() if enrollment.completion_date else None,
                    'start_date': enrollment.start_date.isoformat() if enrollment.start_date else None,
                    'end_date': enrollment.end_date.isoformat() if enrollment.end_date else None,
                    'notes': enrollment.notes,
                    'skills_gained': enrollment.skills_gained,
                    'experience_rating': enrollment.experience_rating,
                    'would_recommend': enrollment.would_recommend
                }
                for enrollment in completed_internships
            ],
            'saved': [
                {
                    'id': saved.id,
                    'internship': {
                        'id': saved.internship.id,
                        'title': saved.internship.title,
                        'company': saved.internship.company,
                        'location': saved.internship.location,
                        'duration': saved.internship.duration,
                        'stipend': saved.internship.stipend,
                        'type': saved.internship.get_type_display(),
                        'description': saved.internship.description,
                        'requirements': saved.internship.requirements,
                        'skills_required': saved.internship.skills_required,
                        'application_url': saved.internship.application_url,
                        'source': saved.internship.source,
                        'posted_date': saved.internship.posted_date.isoformat(),
                        'deadline': saved.internship.deadline.isoformat() if saved.internship.deadline else None,
                        'status': saved.internship.status,
                        'is_featured': saved.internship.is_featured
                    },
                    'saved_date': saved.saved_date.isoformat(),
                    'notes': saved.notes
                }
                for saved in saved_internships
            ]
        })
    
    context = {
        'page_title': 'My Internships',
        'page_description': 'Track your internship journey from enrollment to completion',
        'enrolled_internships': enrolled_internships,
        'completed_internships': completed_internships,
        'in_progress_internships': in_progress_internships,
        'saved_internships': saved_internships,
        'stats': stats,
    }
    return render(request, 'core/my_internships.html', context)


@require_http_methods(["POST"])
def save_roadmap_progress(request):
    """
    Save user's roadmap progress to database
    Expects: {career_path, category_name, skill_name, is_completed, category_index, skill_index}
    """
    try:
        data = json.loads(request.body)
        career_path = data.get('career_path', '').strip()
        category_name = data.get('category_name', '').strip()
        skill_name = data.get('skill_name', '').strip()
        is_completed = data.get('is_completed', False)
        category_index = data.get('category_index', 0)
        skill_index = data.get('skill_index', 0)
        
        if not all([career_path, category_name, skill_name]):
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields: career_path, category_name, skill_name'
            }, status=400)
        
        # Get or create progress record
        progress, created = UserRoadmapProgress.objects.get_or_create(
            user=request.user,
            career_path=career_path,
            skill_name=skill_name,
            defaults={
                'category_name': category_name,
                'is_completed': is_completed,
                'category_index': category_index,
                'skill_index': skill_index,
                'completed_at': timezone.now() if is_completed else None
            }
        )
        
        if not created:
            # Update existing record
            progress.category_name = category_name
            progress.is_completed = is_completed
            progress.category_index = category_index
            progress.skill_index = skill_index
            if is_completed and not progress.completed_at:
                progress.completed_at = timezone.now()
            elif not is_completed:
                progress.completed_at = None
            progress.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Progress saved successfully',
            'created': created,
            'is_completed': progress.is_completed,
            'completed_at': progress.completed_at.isoformat() if progress.completed_at else None
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def load_roadmap_progress(request):
    """
    Load user's roadmap progress for a specific career path
    Query param: career_path
    """
    try:
        career_path = request.GET.get('career_path', '').strip()
        
        if not career_path:
            return JsonResponse({
                'status': 'error',
                'message': 'career_path parameter is required'
            }, status=400)
        
        # Get all progress for this career path
        progress_records = UserRoadmapProgress.objects.filter(
            user=request.user,
            career_path=career_path
        ).order_by('category_index', 'skill_index')
        
        # Format as {skill_name: is_completed} for easy lookup
        progress_data = {}
        for record in progress_records:
            progress_data[record.skill_name] = {
                'is_completed': record.is_completed,
                'category_name': record.category_name,
                'category_index': record.category_index,
                'skill_index': record.skill_index,
                'completed_at': record.completed_at.isoformat() if record.completed_at else None
            }
        
        return JsonResponse({
            'status': 'success',
            'career_path': career_path,
            'progress': progress_data,
            'total_skills': len(progress_data),
            'completed_skills': len([r for r in progress_records if r.is_completed])
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["POST"])
def bulk_update_roadmap_progress(request):
    """
    Bulk update roadmap progress for multiple skills
    Expects: {career_path, updates: [{skill_name, is_completed, category_name, category_index, skill_index}]}
    """
    try:
        data = json.loads(request.body)
        career_path = data.get('career_path', '').strip()
        updates = data.get('updates', [])
        
        if not career_path or not updates:
            return JsonResponse({
                'status': 'error',
                'message': 'career_path and updates are required'
            }, status=400)
        
        updated_count = 0
        created_count = 0
        
        for update in updates:
            skill_name = update.get('skill_name', '').strip()
            if not skill_name:
                continue
                
            progress, created = UserRoadmapProgress.objects.get_or_create(
                user=request.user,
                career_path=career_path,
                skill_name=skill_name,
                defaults={
                    'category_name': update.get('category_name', ''),
                    'is_completed': update.get('is_completed', False),
                    'category_index': update.get('category_index', 0),
                    'skill_index': update.get('skill_index', 0),
                    'completed_at': timezone.now() if update.get('is_completed', False) else None
                }
            )
            
            if created:
                created_count += 1
            else:
                # Update existing record
                progress.category_name = update.get('category_name', progress.category_name)
                progress.is_completed = update.get('is_completed', progress.is_completed)
                progress.category_index = update.get('category_index', progress.category_index)
                progress.skill_index = update.get('skill_index', progress.skill_index)
                if progress.is_completed and not progress.completed_at:
                    progress.completed_at = timezone.now()
                elif not progress.is_completed:
                    progress.completed_at = None
                progress.save()
                updated_count += 1
        
        return JsonResponse({
            'status': 'success',
            'message': f'Bulk update completed: {created_count} created, {updated_count} updated',
            'created_count': created_count,
            'updated_count': updated_count,
            'total_processed': len(updates)
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["POST"])
def enroll_internship(request, internship_id):
    """
    Enroll user in an internship
    """
    try:
        internship = get_object_or_404(Internship, id=internship_id)
        
        enrollment, created = UserInternship.objects.get_or_create(
            user=request.user,
            internship=internship,
            defaults={
                'status': 'enrolled',
                'start_date': timezone.now()
            }
        )
        
        if created:
            return JsonResponse({
                'status': 'success',
                'message': 'Successfully enrolled in internship',
                'enrollment_id': enrollment.id
            })
        else:
            return JsonResponse({
                'status': 'info',
                'message': 'Already enrolled in this internship'
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
        enrollment = get_object_or_404(UserInternship, id=enrollment_id, user=request.user)
        
        data = json.loads(request.body)
        new_status = data.get('status')
        notes = data.get('notes', '')
        skills_gained = data.get('skills_gained', '')
        experience_rating = data.get('experience_rating')
        would_recommend = data.get('would_recommend')
        
        if new_status in ['enrolled', 'in_progress', 'completed']:
            enrollment.status = new_status
            if new_status == 'completed':
                enrollment.completion_date = timezone.now()
            if notes:
                enrollment.notes = notes
            if skills_gained:
                enrollment.skills_gained = skills_gained
            if experience_rating:
                enrollment.experience_rating = experience_rating
            if would_recommend is not None:
                enrollment.would_recommend = would_recommend
            enrollment.save()
            
            return JsonResponse({
                'status': 'success',
                'message': f'Status updated to {new_status}',
                'new_status': new_status
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid status'
            }, status=400)
            
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
        internship = get_object_or_404(Internship, id=internship_id)
        
        saved, created = SavedInternship.objects.get_or_create(
            user=request.user,
            internship=internship,
            defaults={'notes': request.POST.get('notes', '')}
        )
        
        if created:
            return JsonResponse({
                'status': 'success',
                'message': 'Internship saved successfully'
            })
        else:
            return JsonResponse({
                'status': 'info',
                'message': 'Internship already saved'
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
        internship = get_object_or_404(Internship, id=internship_id)
        
        saved = SavedInternship.objects.filter(user=request.user, internship=internship).first()
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
        
        # Handle unauthenticated users
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'success',
                'stats': {
                    'total_enrolled': 0,
                    'completed': 0,
                    'in_progress': 0,
                    'saved': 0,
                    'completion_rate': 0
                }
            })
        
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


def profilepage(request):
    """Profile page with AI extraction and management"""
    context = {
        'page_title': 'AI Profile Management',
        'page_description': 'Manage your professional profile with AI-powered resume extraction',
    }
    return render(request, 'core/profilepage.html', context)


# Aptitude Test Functions - Added directly to fix import issues
@login_required
@require_http_methods(["POST"])
def submit_aptitude_test(request):
    """
    Submit aptitude test results and store in database
    """
    try:
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'Please login to submit test results'
            }, status=401)
        
        data = json.loads(request.body)
        
        # Extract scores from request
        scores = data.get('scores', {})
        time_taken_str = data.get('time_taken', '00:00:00')
        
        # Create test result record
        result = AptitudeTestResult.objects.create(
            user=request.user,
            quantitative_score=scores.get('quantitative', 0),
            verbal_score=scores.get('verbal', 0),
            logical_score=scores.get('logical', 0),
            data_interpretation_score=scores.get('data_interpretation', 0),
            abstract_reasoning_score=scores.get('abstract_reasoning', 0),
            max_score=data.get('max_score', 150),
            time_taken=time_taken_str,
            difficulty_level=data.get('difficulty_level', 'mixed')
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Test results saved successfully!',
            'result_id': result.id,
            'total_score': result.total_score,
            'percentage': result.percentage,
            'scores': {
                'quantitative': result.quantitative_score,
                'verbal': result.verbal_score,
                'logical': result.logical_score,
                'data_interpretation': result.data_interpretation_score,
                'abstract_reasoning': result.abstract_reasoning_score
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error saving test results: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["GET"])
def get_aptitude_results(request):
    """
    Get user's aptitude test history
    """
    try:
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'Please login to view test results'
            }, status=401)
        
        results = AptitudeTestResult.objects.filter(user=request.user).order_by('-test_date')
        
        results_data = []
        for result in results:
            results_data.append({
                'id': result.id,
                'test_date': result.test_date.strftime('%Y-%m-%d %H:%M'),
                'total_score': result.total_score,
                'max_score': result.max_score,
                'percentage': result.percentage,
                'difficulty_level': result.difficulty_level,
                'time_taken': str(result.time_taken),
                'scores': {
                    'quantitative': result.quantitative_score,
                    'verbal': result.verbal_score,
                    'logical': result.logical_score,
                    'data_interpretation': result.data_interpretation_score,
                    'abstract_reasoning': result.abstract_reasoning_score
                }
            })
        
        return JsonResponse({
            'status': 'success',
            'results': results_data,
            'total_count': results.count()
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def skill_gap_data(request):
    """
    API endpoint to fetch skill gap analysis data
    """
    try:
        user = request.user
        
        # Get user's skills from database
        user_skills = UserSkill.objects.filter(user=user).select_related('skill', 'skill__category')
        
        # Format skills for skill gap analysis
        current_skills = []
        for user_skill in user_skills:
            current_skills.append({
                'skill_name': user_skill.skill.name,
                'proficiency_level': user_skill.proficiency_level,
                'years_experience': float(user_skill.years_experience),
                'is_verified': user_skill.is_verified,
                'category': user_skill.skill.category.name if user_skill.skill.category else 'General'
            })
        
        # Sample skill gap analysis data (in real app, this would be calculated)
        gaps = [
            {'name': 'Docker', 'current': 'beginner', 'required': 'intermediate', 'priority': 'high'},
            {'name': 'AWS', 'current': 'beginner', 'required': 'intermediate', 'priority': 'medium'}
        ]
        
        upgrades = [
            {'name': 'Node.js', 'current': 'intermediate', 'required': 'advanced', 'priority': 'medium'}
        ]
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'current_skills': current_skills,
                'gaps': gaps,
                'upgrades': upgrades,
                'total_skills': len(current_skills),
                'verified_skills': len([s for s in current_skills if s['is_verified']]),
                'avg_proficiency': sum([s['proficiency_level'] for s in current_skills]) / len(current_skills) if current_skills else 0
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def profile_data(request):
    """
    API endpoint to fetch profile data
    """
    try:
        user = request.user
        
        # Get user's skills from database
        user_skills = UserSkill.objects.filter(user=user).select_related('skill', 'skill__category')
        
        # Format skills for profile
        skills = []
        for user_skill in user_skills:
            skills.append({
                'skill_name': user_skill.skill.name,
                'proficiency_level': user_skill.proficiency_level,
                'years_experience': float(user_skill.years_experience),
                'is_verified': user_skill.is_verified,
                'category': user_skill.skill.category.name if user_skill.skill.category else 'General'
            })
        
        # Get education, projects, certifications (sample data for now)
        education = [
            {'degree': 'Bachelor of Technology', 'field': 'Computer Science', 'year': '2022'}
        ]
        
        projects = [
            {'name': 'E-commerce Platform', 'description': 'Full-stack web application', 'technologies': ['React', 'Node.js']}
        ]
        
        certifications = [
            {'name': 'React Developer', 'issuer': 'Meta', 'date': '2024-01-15'}
        ]
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'skills': skills,
                'education': education,
                'projects': projects,
                'certifications': certifications,
                'total_skills': len(skills),
                'verified_skills': len([s for s in skills if s['is_verified']]),
                'avg_proficiency': sum([s['proficiency_level'] for s in skills]) / len(skills) if skills else 0
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
