# Developer's Quick Reference - Real Data Integration

## 🔧 For Developers Making Changes

This guide helps developers understand and modify the real data integration system.

---

## 📂 File Locations

| File | Purpose | Key Content |
|------|---------|-------------|
| `apps/core/views.py` | Backend logic | Database queries, API endpoint, comparisons |
| `apps/core/urls.py` | URL routing | API route mapping |
| `templates/core/skillgap.html` | Frontend UI | HTML structure + JavaScript |
| `apps/skills/models.py` | Database schema | UserSkill, Skill, SkillCategory models |
| `apps/jobs/models.py` | Database schema | Job, Company, skill relationships |

---

## 🔌 Core Functions

### Backend: views.py

#### 1. skill_gap_analysis(request)

**Purpose**: Load skill gap analysis page with user's real data

```python
@login_required
def skill_gap_analysis(request):
    # Get user object
    user = request.user
    
    # Query user's skills from database
    user_skills = UserSkill.objects.filter(user=user).select_related(
        'skill', 'skill__category'
    )
    
    # Convert to JSON-friendly dictionary list
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
    categories_data = [{'id': c.id, 'name': c.name} for c in categories]
    
    # Pass to template as JSON
    context = {
        'user_skills_json': json.dumps(user_skills_data),
        'categories_json': json.dumps(categories_data),
    }
    return render(request, 'core/skillgap.html', context)
```

**Modify if**: You need different user data fields

---

#### 2. get_role_requirements(request) [API ENDPOINT]

**Purpose**: REST API that returns role requirements and compares with user skills

**Request**: 
```json
POST /api/get-role-requirements/
{
  "role_title": "Senior React Developer",
  "experience_level": "Senior",
  "industry": "Technology/Software"
}
```

**Response**:
```json
{
  "status": "success",
  "source": "job_database",
  "benchmark": {
    "required_skills": [...],
    "preferred_skills": [...],
    "met_skills": [...],
    "missing_skills": [...],
    "proficiency_gaps": [...],
    "emerging_skills": [...],
    "met_count": 5,
    "gap_count": 2,
    "missing_count": 3
  }
}
```

**Key Logic**:
```python
@login_required
@require_http_methods(["POST"])
def get_role_requirements(request):
    data = json.loads(request.body)
    role_title = data.get('role_title')
    
    # 1. Search for matching job in database
    job = Job.objects.filter(
        is_active=True,
        title__icontains=role_title
    ).first()
    
    # 2. If no job found, use generic benchmark
    if not job:
        return JsonResponse({
            'benchmark': _get_generic_benchmark(role_title, ...)
        })
    
    # 3. Get user's skills as quick lookup dict
    user_skills = UserSkill.objects.filter(user=request.user)
    user_skills_dict = {
        us.skill.id: {
            'proficiency_numeric': _get_proficiency_numeric(us.proficiency_level),
            'years': us.years_experience
        }
        for us in user_skills
    }
    
    # 4. Compare user skills with job requirements
    met_skills = []
    missing_skills = []
    proficiency_gaps = []
    emerging_skills = []
    
    for skill in job.skills_required.all():
        if skill.id in user_skills_dict:
            user_proficiency = user_skills_dict[skill.id]['proficiency_numeric']
            
            if user_proficiency >= 3:  # advanced level or higher
                met_skills.append({'skill_name': skill.name, ...})
            else:
                gap = 3 - user_proficiency
                proficiency_gaps.append({
                    'skill_name': skill.name,
                    'gap_level': gap,
                    ...
                })
        else:
            missing_skills.append({'skill_name': skill.name, ...})
    
    # 5. Add preferred skills to emerging
    for skill in job.skills_preferred.all():
        if skill.id not in user_skills_dict:
            emerging_skills.append({'skill_name': skill.name, ...})
    
    # 6. Return comparison
    return JsonResponse({
        'status': 'success',
        'source': 'job_database',
        'benchmark': {
            'met_skills': met_skills,
            'missing_skills': missing_skills,
            'proficiency_gaps': proficiency_gaps,
            'emerging_skills': emerging_skills,
            'met_count': len(met_skills),
            'gap_count': len(proficiency_gaps),
            'missing_count': len(missing_skills)
        }
    })
```

**Modify if**: You need different comparison logic

---

#### 3. _get_proficiency_numeric(level)

**Purpose**: Convert proficiency string to numeric scale (1-4)

```python
def _get_proficiency_numeric(proficiency_level):
    """
    Convert proficiency level to numeric scale
    beginner (1) → intermediate (2) → advanced (3) → expert (4)
    """
    numeric_map = {
        'beginner': 1,
        'intermediate': 2,
        'advanced': 3,
        'expert': 4
    }
    return numeric_map.get(proficiency_level.lower(), 0)
```

**Modify if**: Your proficiency levels are different (e.g., 0-10 scale)

---

#### 4. _get_generic_benchmark(role_title, experience_level)

**Purpose**: Fallback when no job found - returns generic benchmark

```python
def _get_generic_benchmark(role_title, experience_level):
    """
    Generic role benchmarks when job not found in database
    Used as fallback for common roles
    """
    role_skill_mapping = {
        'react': {
            'required': ['React', 'JavaScript', 'HTML/CSS', 'Git'],
            'preferred': ['TypeScript', 'Node.js', 'REST API', 'Testing']
        },
        'django': {
            'required': ['Django', 'Python', 'SQL', 'Git'],
            'preferred': ['Django REST Framework', 'PostgreSQL', 'Docker', 'Testing']
        },
        # ... more role mappings
    }
    
    # Find matching role
    role_key = next(
        (k for k in role_skill_mapping.keys() if k in role_title.lower()),
        'generic'
    )
    
    skills = role_skill_mapping.get(role_key, {})
    
    # Convert to same format as job requirement response
    return {
        'met_skills': [],
        'missing_skills': [{'skill_name': s} for s in skills.get('required', [])],
        'proficiency_gaps': [],
        'emerging_skills': [{'skill_name': s} for s in skills.get('preferred', [])]
    }
```

**Modify if**: You want to change fallback behaviors

---

## 🖥️ Frontend Functions

### skillgap.html JavaScript

#### Data Reception

```javascript
// Receives from server (server injects these)
const userSkillsData = {{ user_skills_json|safe }};
const categoriesData = {{ categories_json|safe }};

// Create lookup map for quick access
const userSkillsMap = new Map(
    userSkillsData.map(s => [s.skill_name.toLowerCase(), s])
);
```

---

#### generateAnalysis()

**Triggered**: When user clicks "Run Market Analysis" button

```javascript
function generateAnalysis() {
    // Get form values
    const targetRole = document.getElementById('targetRole').value;
    const expLevel = document.getElementById('expLevel').value;
    const industry = document.getElementById('industry').value;
    
    // Show loading state
    showLoadingAnimation();
    
    // Call API endpoint
    fetch('/api/get-role-requirements/', {
        method: 'POST',
        body: JSON.stringify({
            'role_title': targetRole,
            'experience_level': expLevel,
            'industry': industry
        }),
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    })
    .then(data => {
        // Data contains: {status, source, benchmark: {...}}
        const benchmark = data.benchmark;
        
        // Update all 8 modules
        updateBenchmarkCard(benchmark);
        updateComparativeVisualization(benchmark);
        updateSkillGapAnalysis(benchmark);
        updatePriorityMatrix(benchmark);
        updateLearningPath(benchmark);
        updateRoleComparison(benchmark);
        updateProgressTracker(benchmark);
        renderCharts(benchmark);
        
        // Hide loading
        hideLoadingAnimation();
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorMessage('Failed to analyze role. Please try again.');
        hideLoadingAnimation();
    });
}
```

**Modify if**: You want different form fields or API parameters

---

#### Module Update Functions

##### updateSkillGapAnalysis(benchmark)

```javascript
function updateSkillGapAnalysis(benchmark) {
    // benchmark = {met_skills: [], missing_skills: [], ...}
    
    // Clear previous display
    document.getElementById('metSkillsList').innerHTML = '';
    document.getElementById('missingSkillsList').innerHTML = '';
    document.getElementById('gapsList').innerHTML = '';
    document.getElementById('emergingList').innerHTML = '';
    
    // Display met skills (green)
    benchmark.met_skills.forEach(skill => {
        const html = `
            <div class="skill-item met">
                <span class="skill-name">${skill.skill_name}</span>
                <span class="badge badge-success">Met</span>
            </div>
        `;
        document.getElementById('metSkillsList').innerHTML += html;
    });
    
    // Display missing skills (red)
    benchmark.missing_skills.forEach(skill => {
        const html = `
            <div class="skill-item missing">
                <span class="skill-name">${skill.skill_name}</span>
                <span class="badge badge-danger">Missing</span>
            </div>
        `;
        document.getElementById('missingSkillsList').innerHTML += html;
    });
    
    // Display proficiency gaps (yellow)
    benchmark.proficiency_gaps.forEach(skill => {
        const html = `
            <div class="skill-item gap">
                <span class="skill-name">${skill.skill_name}</span>
                <span class="badge badge-warning">Gap: +${skill.gap_level}</span>
            </div>
        `;
        document.getElementById('gapsList').innerHTML += html;
    });
    
    // Display emerging skills (blue)
    benchmark.emerging_skills.forEach(skill => {
        const html = `
            <div class="skill-item emerging">
                <span class="skill-name">${skill.skill_name}</span>
                <span class="badge badge-info">Emerging</span>
            </div>
        `;
        document.getElementById('emergingList').innerHTML += html;
    });
}
```

**Modify if**: You want different HTML structure or styling

---

#### renderCharts(benchmark)

```javascript
function renderCharts(benchmark) {
    // Chart 1: Radar Chart (User vs Job Skills)
    const ctx1 = document.getElementById('radarChart').getContext('2d');
    
    // Prepare data for radar
    const allSkills = [...new Set([
        ...benchmark.met_skills.map(s => s.skill_name),
        ...benchmark.missing_skills.map(s => s.skill_name),
        ...benchmark.proficiency_gaps.map(s => s.skill_name)
    ])];
    
    const userValues = allSkills.map(skill => {
        const found = findUserSkill(skill);
        return found ? found.proficiency_numeric : 0;
    });
    
    const jobValues = allSkills.map(skill => {
        // Assume required skills need level 3 (advanced)
        return benchmark.required_skills.includes(skill) ? 3 : 2;
    });
    
    new Chart(ctx1, {
        type: 'radar',
        data: {
            labels: allSkills,
            datasets: [
                {
                    label: 'Your Skills',
                    data: userValues,
                    borderColor: '#4CAF50',
                    backgroundColor: 'rgba(76, 175, 80, 0.1)'
                },
                {
                    label: 'Job Requirements',
                    data: jobValues,
                    borderColor: '#FF9800',
                    backgroundColor: 'rgba(255, 152, 0, 0.1)'
                }
            ]
        },
        options: { responsive: true }
    });
    
    // Chart 2: Bar Chart (Gap Analysis)
    // ... similar structure
}
```

**Modify if**: You want different chart types or data

---

#### findUserSkill(skillName)

**Helper function to find user's skill in array:**

```javascript
function findUserSkill(skillName) {
    return userSkillsData.find(
        s => s.skill_name.toLowerCase() === skillName.toLowerCase()
    );
}
```

---

#### getCookie(name)

**Extract CSRF token for secure API calls:**

```javascript
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
```

---

## 🔄 Data Flow Modification

### To Change Where Data Comes From

**Current Flow**: Database → Python View → JSON → JavaScript

**Example: Add API Source**

```python
# In get_role_requirements(), before database query:
if data.get('source') == 'api':
    job = fetch_from_external_api(role_title)  # New function
elif data.get('source') == 'database':
    job = Job.objects.filter(...).first()
else:
    job = Job.objects.filter(...).first()  # Default
```

---

### To Change How Data Is Compared

**Current**: User proficiency >= 3 means "met"

**Example: Custom Comparison**

```python
# In get_role_requirements(), comparison logic:
# Current:
if user_proficiency >= 3:  # advanced or expert
    met_skills.append(...)

# Change to:
experience = user_skills_dict[skill.id]['years']
if user_proficiency >= 3 and experience >= 2:  # Also check years
    met_skills.append(...)
```

---

## 📊 Database Model Integration

### Adding New User Data to Comparison

**Current Models**:
- UserSkill: skill, proficiency_level, years_experience, is_verified
- ProfessionalIdentity: education_level, location, languages
- Certification: certification_name, issuing_organization, issue_date, expiry_date

**Example: Add Certifications**

```python
# In skill_gap_analysis() view:
certifications = Certification.objects.filter(user=user)
cert_skills = [c.skill for c in certifications if c.skill]

# In frontend:
const certificationSkills = [...];
// Use in comparison logic
```

---

### Adding New Job Requirements

**Current Models**:
- Job: title, skills_required, skills_preferred
- Company: name, industry, location
- JobApplication: user, job, status, applied_date

**Example: Add Company Size**

```python
# In get_role_requirements():
job = Job.objects.filter(...).first()
company_size = job.company.size  # New field

# Return with response:
return JsonResponse({
    'company_size': company_size,
    'benchmark': {...}
})
```

---

## 🧪 Testing Changes

### Unit Test Example

```python
# In apps/core/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from apps.skills.models import UserSkill, Skill, SkillCategory

class SkillGapAnalysisTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        
        # Create test skill
        category = SkillCategory.objects.create(name='Backend')
        skill = Skill.objects.create(name='Django', category=category)
        
        # Assign skill to user
        UserSkill.objects.create(
            user=self.user,
            skill=skill,
            proficiency_level='advanced'
        )
    
    def test_skill_gap_page_loads(self):
        self.client.force_login(self.user)
        response = self.client.get('/skill-gap-analysis/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Django', response.content)
    
    def test_api_returns_comparison(self):
        self.client.force_login(self.user)
        response = self.client.post(
            '/api/get-role-requirements/',
            {'role_title': 'Django Developer'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('benchmark', data)
```

---

## 🚀 Performance Optimization

### Current Performance Issues & Fixes

**Issue 1**: N+1 query problem

**Current**:
```python
user_skills = UserSkill.objects.filter(user=user)  # 1 query
for us in user_skills:
    print(us.skill.name)  # N queries (1 per skill)
```

**Fixed**:
```python
user_skills = UserSkill.objects.filter(user=user).select_related('skill')  # 1 query with join
```

---

**Issue 2**: Dictionary conversion is slow

**Current**:
```python
for us in user_skills:
    if us.skill.id == skill.id:  # O(n) lookup in loop
        ...
```

**Fixed**:
```python
user_skills_dict = {us.skill.id: us for us in user_skills}  # O(1) lookup
if skill.id in user_skills_dict:
    ...
```

---

## 📚 Command Reference

### Add Skills to User (Manual Testing)

```bash
python manage.py shell

from django.contrib.auth.models import User
from apps.skills.models import Skill, UserSkill, SkillCategory

# Get or create user
user = User.objects.get(email='test@example.com')

# Get or create skill
category = SkillCategory.objects.get_or_create(name='Frontend')[0]
skill = Skill.objects.get_or_create(name='React', defaults={'category': category})[0]

# Add to user
UserSkill.objects.get_or_create(
    user=user,
    skill=skill,
    defaults={'proficiency_level': 'advanced'}
)
```

---

### Add Test Job

```bash
python manage.py shell

from apps.jobs.models import Job, Company
from apps.skills.models import Skill

company = Company.objects.first()
job = Job.objects.create(
    title='Senior React Developer',
    company=company,
    experience_level='senior'
)

# Add required skills
react = Skill.objects.get(name='React')
job.skills_required.add(react)

# Add preferred skills
typescript = Skill.objects.get(name='TypeScript')
job.skills_preferred.add(typescript)
```

---

## 🐛 Debug Logging

### Add Logging to Views

```python
import logging

logger = logging.getLogger(__name__)

def get_role_requirements(request):
    try:
        data = json.loads(request.body)
        logger.info(f'Role analysis for: {data.get("role_title")}')
        
        job = Job.objects.filter(...).first()
        logger.info(f'Found job: {job.title if job else "No match"}')
        
        # ... comparison logic
        logger.info(f'Met: {len(met_skills)}, Missing: {len(missing_skills)}')
        
        return JsonResponse({'benchmark': {...}})
    except Exception as e:
        logger.error(f'Error in get_role_requirements: {e}', exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
```

---

### Check Django Logs

```bash
# Run with debug output
python manage.py runserver --verbosity 3

# Or tail log file
tail -f logs/django.log
```

---

## 📖 Common Modifications Checklist

- [ ] **Change proficiency scale** → Modify `_get_proficiency_numeric()`
- [ ] **Add new skill comparison logic** → Modify `get_role_requirements()` comparison section
- [ ] **Add new job data source** → Create new API client + integrate in `get_role_requirements()`
- [ ] **Customize benchmark skills** → Update `role_skill_mapping` in `_get_generic_benchmark()`
- [ ] **Change module display** → Update function in `updateSkillGapAnalysis()`
- [ ] **Add new chart type** → Create in `renderCharts()`
- [ ] **Fetch additional user data** → Query model in `skill_gap_analysis()` view
- [ ] **Add new API parameter** → Update both frontend form + backend function

---

**Version**: 1.0  
**Created**: February 22, 2026  
**Last Updated**: February 22, 2026  
**Status**: ✅ Complete Reference
