from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from apps.skills.models import UserSkill, Skill, SkillCategory
from apps.jobs.models import Job

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your context data here
        return context

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
def skill_gap_analysis(request):
    """
    Skill Gap Analysis Page - PAGE 2
    Displays market benchmark analysis, skill gap identification,
    and personalized learning paths for skill development
    
    Fetches real user skills from database and compares with role requirements
    """
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
            'years_experience': str(us.years_experience),
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


@login_required
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
        
        # Fetch jobs matching the criteria
        jobs_query = Job.objects.filter(is_active=True)
        
        if role_title:
            jobs_query = jobs_query.filter(title__icontains=role_title)
        if experience_level:
            jobs_query = jobs_query.filter(experience_level=experience_level)
        
        # Get the first matching job as the benchmark
        job = jobs_query.first()
        
        if not job:
            # Return sample/benchmark data if no matching job found
            benchmark_data = _get_generic_benchmark(role_title, experience_level)
            return JsonResponse({
                'status': 'success',
                'source': 'benchmark',
                'job_title': role_title or 'Senior Developer',
                'benchmark': benchmark_data,
                'message': 'Using industry benchmark data'
            })
        
        # Get required and preferred skills from the job
        required_skills = job.skills_required.all()
        preferred_skills = job.skills_preferred.all()
        
        # Get user's skills
        user = request.user
        user_skills_dict = {}
        user_skills = UserSkill.objects.filter(user=user).select_related('skill')
        for us in user_skills:
            user_skills_dict[us.skill.id] = {
                'name': us.skill.name,
                'proficiency_level': us.proficiency_level,
                'proficiency_numeric': _get_proficiency_numeric(us.proficiency_level),
                'years_experience': str(us.years_experience),
                'is_verified': us.is_verified
            }
        
        # Build comparison data
        benchmark_data = {
            'job_title': job.title,
            'company': job.company.name if job.company else 'Unknown',
            'experience_level': job.get_experience_level_display(),
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
        for skill in required_skills:
            skill_data = {
                'skill_id': skill.id,
                'skill_name': skill.name,
                'skill_type': skill.skill_type,
                'category': skill.category.name,
                'requirement_level': 'required',
                'requirement_description': f'{skill.name}: Level 3 (Advanced) - Required',
                'recommended_proficiency': 'advanced'
            }
            
            if skill.id in user_skills_dict:
                user_skill = user_skills_dict[skill.id]
                skill_data['user_proficiency'] = user_skill['proficiency_level']
                skill_data['user_proficiency_numeric'] = user_skill['proficiency_numeric']
                skill_data['user_years_experience'] = user_skill['years_experience']
                skill_data['is_verified'] = user_skill['is_verified']
                
                # Check if meets requirement
                if user_skill['proficiency_numeric'] >= 3:
                    benchmark_data['met_skills'].append(skill_data)
                    benchmark_data['met_count'] += 1
                else:
                    skill_data['gap_level'] = 3 - user_skill['proficiency_numeric']
                    benchmark_data['proficiency_gaps'].append(skill_data)
                    benchmark_data['gap_count'] += 1
            else:
                skill_data['user_proficiency'] = 'none'
                skill_data['user_proficiency_numeric'] = 0
                benchmark_data['missing_skills'].append(skill_data)
                benchmark_data['missing_count'] += 1
            
            benchmark_data['required_skills'].append(skill_data)
        
        # Process preferred skills (emerging skills)
        for skill in preferred_skills:
            skill_data = {
                'skill_id': skill.id,
                'skill_name': skill.name,
                'skill_type': skill.skill_type,
                'category': skill.category.name,
                'requirement_level': 'preferred',
                'requirement_description': f'{skill.name} - Preferred',
                'recommended_proficiency': 'intermediate'
            }
            
            if skill.id in user_skills_dict:
                user_skill = user_skills_dict[skill.id]
                skill_data['user_proficiency'] = user_skill['proficiency_level']
                skill_data['user_proficiency_numeric'] = user_skill['proficiency_numeric']
            else:
                skill_data['user_proficiency'] = 'none'
                skill_data['user_proficiency_numeric'] = 0
                benchmark_data['emerging_skills'].append(skill_data)
            
            benchmark_data['preferred_skills'].append(skill_data)
        
        return JsonResponse({
            'status': 'success',
            'source': 'job_database',
            'job_title': job.title,
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
        'react': {
            'required': ['React', 'JavaScript', 'HTML/CSS', 'Git'],
            'preferred': ['TypeScript', 'Node.js', 'REST API', 'Testing']
        },
        'senior react': {
            'required': ['React', 'JavaScript', 'TypeScript', 'System Design', 'State Management'],
            'preferred': ['Node.js', 'Docker', 'AWS', 'GraphQL', 'Testing Frameworks']
        },
        'full stack': {
            'required': ['JavaScript', 'React', 'Node.js', 'Database', 'REST API'],
            'preferred': ['TypeScript', 'Docker', 'AWS', 'Git', 'DevOps']
        },
        'backend': {
            'required': ['Python', 'Node.js', 'Database', 'REST API', 'Git'],
            'preferred': ['Docker', 'Kubernetes', 'Microservices', 'System Design']
        },
        'data scientist': {
            'required': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Processing'],
            'preferred': ['TensorFlow', 'PyTorch', 'Big Data', 'Cloud Platforms']
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
        'mid': 'advanced',
        'senior': 'advanced',
        'lead': 'expert'
    }
    recommended_level = level_map.get(experience_level.lower(), 'advanced')
    
    return {
        'job_title': role_title or 'Senior Developer',
        'experience_level': experience_level or 'Senior Level',
        'required_skills': [
            {'skill_name': s, 'requirement_level': 'required', 'recommended_proficiency': recommended_level}
            for s in matched_role.get('required', [])
        ],
        'preferred_skills': [
            {'skill_name': s, 'requirement_level': 'preferred', 'recommended_proficiency': 'intermediate'}
            for s in matched_role.get('preferred', [])
        ],
        'met_skills': [],
        'missing_skills': [],
        'proficiency_gaps': [],
        'emerging_skills': []
    }