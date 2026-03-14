# Real Data Integration Guide - Skill Gap Analysis

## 🎯 Overview

The Skill Gap Analysis page now pulls **real user data from the database** and compares it against **actual job requirements** from your jobs database, providing genuine skill gap analysis.

---

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ User Profile Data                                           │
│ (Stored in Database)                                        │
│                                                              │
│ Models:                                                      │
│ - UserSkill (skill, proficiency_level, years_experience)  │
│ - ProfessionalIdentity                                      │
│ - Education, Certifications, Courses                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ skill_gap_analysis() view
                     │ Fetches user skills from DB
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ Skill Gap Analysis Page                                     │
│ (/skill-gap-analysis/)                                      │
│                                                              │
│ Displays:                                                    │
│ - User's current skills                                     │
│ - Target role form                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ User selects role and clicks
                     │ "Run Market Analysis"
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ API Request: /api/get-role-requirements/                   │
│                                                              │
│ POST Data:                                                   │
│ {                                                            │
│   "role_title": "Senior React Developer",                  │
│   "experience_level": "Senior",                             │
│   "industry": "Technology/Software"                         │
│ }                                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ get_role_requirements() view
                     │ - Search jobs database for matching role
                     │ - Get required & preferred skills
                     │ - Compare with user's skills
                     │ - Calculate gaps
                     │ - Return comparison data
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ Comparison Data (JSON Response)                             │
│                                                              │
│ {                                                            │
│   "met_skills": [...],      ✅ User has these skills      │
│   "missing_skills": [...],  ❌ User missing these skills  │
│   "proficiency_gaps": [...],⬆️ User needs to upgrade      │
│   "emerging_skills": [...] 💡 Future-relevant skills     │
│ }                                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ JavaScript processes response
                     │ - Updates benchmark display
                     │ - Renders comparison charts
                     │ - Shows priority matrix
                     │ - Updates learning path
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ Real Comparison Display                                     │
│ - Visualizations with real data                             │
│ - Gap analysis based on user's skills                       │
│ - Priority matrix with actual gaps                          │
│ - Learning path for real gaps                               │
│ - Progress tracking                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Structures

### 1. User Skills (From Database)

**Model**: `UserSkill`

```python
UserSkill {
    user: User  # Authenticated user
    skill: Skill  # The skill object
    proficiency_level: String  # 'beginner', 'intermediate', 'advanced', 'expert'
    years_experience: Decimal  # 0-50 years
    is_verified: Boolean  # LinkedIn/GitHub verified
}
```

**Converted to JSON for Template**:

```json
{
  "skill_id": 1,
  "skill_name": "React",
  "category": "Frontend Technologies",
  "skill_type": "technical",
  "proficiency_level": "advanced",
  "proficiency_numeric": 3,
  "years_experience": "3.5",
  "is_verified": true
}
```

### 2. Job Requirements (From Database)

**Model**: `Job`

```python
Job {
    title: String  # "Senior React Developer"
    experience_level: String  # 'entry', 'mid', 'senior', 'lead'
    skills_required: ManyToMany[Skill]
    skills_preferred: ManyToMany[Skill]
    description: Text
    requirements: Text
}
```

### 3. Comparison Result

```json
{
  "status": "success",
  "source": "job_database",  // or "benchmark" if no match found
  "job_title": "Senior React Developer",
  "benchmark": {
    "met_skills": [
      {
        "skill_name": "React",
        "user_proficiency_numeric": 4,
        "recommended_proficiency": "advanced"
      }
    ],
    "missing_skills": [
      {
        "skill_name": "Docker",
        "user_proficiency_numeric": 0,
        "requirement_level": "required"
      }
    ],
    "proficiency_gaps": [
      {
        "skill_name": "TypeScript",
        "user_proficiency_numeric": 2,
        "gap_level": 1  // Need to go up 1 level
      }
    ],
    "emerging_skills": [
      {
        "skill_name": "GraphQL",
        "requirement_level": "preferred"
      }
    ],
    "met_count": 5,
    "gap_count": 3,
    "missing_count": 2
  }
}
```

---

## 🔌 API Endpoints

### GET /skill-gap-analysis/

**Method**: GET  
**Authentication**: Required (@login_required)  
**Parameters**: None

**Returns**: HTML page with user's skills injected as JSON

```html
<script>
  const userSkillsData = [{...}, {...}, ...];
  const categoriesData = [{...}, {...}, ...];
</script>
```

---

### POST /api/get-role-requirements/

**Method**: POST  
**Authentication**: Required (@login_required)  
**Content-Type**: application/json

**Request Body**:

```json
{
  "role_title": "Senior React Developer",
  "experience_level": "Senior",
  "industry": "Technology/Software",
  "career_path": "Frontend Dev → Senior → Lead"
}
```

**Response**:

```json
{
  "status": "success",
  "source": "job_database",
  "job_title": "Senior React Developer at Company X",
  "benchmark": {
    "required_skills": [...],
    "preferred_skills": [...],
    "met_skills": [...],
    "missing_skills": [...],
    "proficiency_gaps": [...],
    "emerging_skills": [...],
    "met_count": 5,
    "gap_count": 3,
    "missing_count": 2
  }
}
```

---

## 💾 Database Models Used

### Skills App Models

```
SkillCategory
├── name: CharField
└── skills: ForeignKey

Skill
├── name: CharField
├── category: ForeignKey → SkillCategory
├── skill_type: Choice (technical, soft, domain, language)
└── description: TextField

UserSkill
├── user: ForeignKey → User
├── skill: ForeignKey → Skill
├── proficiency_level: Choices (beginner, intermediate, advanced, expert)
├── years_experience: DecimalField
└── is_verified: BooleanField
```

### Jobs App Models

```
Job
├── title: CharField
├── company: ForeignKey → Company
├── experience_level: Choices (entry, mid, senior, lead, manager)
├── job_type: Choices (full_time, part_time, internship, contract, remote)
├── skills_required: ManyToMany → Skill
├── skills_preferred: ManyToMany → Skill
└── description: TextField
```

---

## 🛠️ Implementation Details

### 1. View: skill_gap_analysis() in apps/core/views.py

**What it does**:
- Fetches user's skills from UserSkill table
- Converts skills to JSON format
- Gets skill categories
- Passes data to template

**Key Code**:
```python
@login_required
def skill_gap_analysis(request):
    user = request.user
    user_skills = UserSkill.objects.filter(user=user).select_related('skill', 'skill__category')
    
    user_skills_data = []
    for us in user_skills:
        user_skills_data.append({
            'skill_name': us.skill.name,
            'category': us.skill.category.name,
            'proficiency_level': us.proficiency_level,
            'proficiency_numeric': _get_proficiency_numeric(us.proficiency_level),
            'years_experience': str(us.years_experience),
            'is_verified': us.is_verified
        })
    
    context = {
        'user_skills_json': json.dumps(user_skills_data),
        'categories_json': json.dumps(categories_data),
    }
    return render(request, 'core/skillgap.html', context)
```

### 2. API Endpoint: get_role_requirements() in apps/core/views.py

**What it does**:
- Receives role title, experience level, industry
- Searches Job database for matching jobs
- Gets required & preferred skills
- Compares with user's skills
- Categorizes skills into: met, missing, gaps, emerging
- Returns JSON response

**Key Logic**:
```python
@login_required
@require_http_methods(["POST"])
def get_role_requirements(request):
    data = json.loads(request.body)
    role_title = data.get('role_title')
    
    # Search jobs database
    jobs_query = Job.objects.filter(is_active=True, title__icontains=role_title)
    job = jobs_query.first()
    
    # Compare user skills with job requirements
    for skill in job.skills_required.all():
        if skill.id in user_skills_dict:
            # User has this skill
            if user_proficiency >= recommended:
                # Add to met_skills
            else:
                # Add to proficiency_gaps
        else:
            # Add to missing_skills
    
    return JsonResponse({
        'benchmark': {
            'met_skills': [...],
            'missing_skills': [...],
            'proficiency_gaps': [...],
            'emerging_skills': [...]
        }
    })
```

### 3. Template: skillgap.html

**What it does**:
- Receives user skills from server
- Displays user's skills on page load
- Sends role request to API when user submits form
- Updates all sections with real data

**Key JavaScript**:
```javascript
// Data from server
const userSkillsData = {{ user_skills_json|safe }};

// On button click
function generateAnalysis() {
    // Fetch role requirements from API
    fetch('/api/get-role-requirements/', {
        method: 'POST',
        body: JSON.stringify({
            role_title: targetRole,
            experience_level: expLevel
        })
    })
    .then(response => response.json())
    .then(data => {
        // Update all sections with real data
        updateBenchmarkCard(data.benchmark);
        updateSkillGapAnalysis(data.benchmark);
        updatePriorityMatrix(data.benchmark);
        renderCharts(data.benchmark);
    });
}
```

---

## 🎯 How Gaps Are Calculated

### 1. Met Skills ✅

**Criteria**: User's proficiency >= Recommended proficiency

```python
if user_proficiency_numeric >= 3 and skill.requirement_level == 'required':
    # Add to met_skills
```

### 2. Missing Skills ❌

**Criteria**: User has no proficiency in this skill

```python
if skill.id not in user_skills_dict:
    # Add to missing_skills
```

### 3. Proficiency Gaps ⬆️

**Criteria**: User has skill but below recommended level

```python
if skill.id in user_skills_dict:
    if user_proficiency_numeric < recommended:
        gap_level = recommended - user_proficiency_numeric
        # Add to proficiency_gaps
```

### 4. Emerging Skills 💡

**Criteria**: Preferred skills (not required but important)

```python
if skill in job.skills_preferred.all():
    # Add to emerging_skills
```

---

## 📈 Comparison Calculation

### Compatibility Score

```python
compatibility = (met_skills / total_required_skills) * 100
```

### Example

User has:
- React: Advanced (meets requirement)
- JavaScript: Intermediate (meets requirement)
- HTML/CSS: Advanced (meets requirement)

Job requires:
- React: Advanced ✅
- JavaScript: Intermediate ✅
- HTML/CSS: Intermediate ✅
- TypeScript: Advanced ❌
- Docker: Intermediate ❌

**Compatibility**: 3/5 = **60%**

---

## 🔄 Fallback Mechanism

If no job matches the search criteria, the system uses **generic benchmarks** based on role title:

```python
def _get_generic_benchmark(role_title, experience_level):
    # Map role titles to typical skills
    if 'react' in role_title.lower():
        required_skills = ['React', 'JavaScript', 'HTML/CSS', 'Git']
        preferred_skills = ['TypeScript', 'Node.js', 'REST API', 'Testing']
    
    # Return benchmark data
```

This ensures users always get analysis even if no exact job match is found.

---

## 🧪 Testing Real Data

### 1. Add Test Skills to User

```python
# In Django shell
from apps.skills.models import Skill, UserSkill
from apps.accounts.models import User

user = User.objects.get(email='test@example.com')
react = Skill.objects.get(name='React')
UserSkill.objects.create(user=user, skill=react, proficiency_level='advanced')
```

### 2. Add Test Jobs

```python
from apps.jobs.models import Job, Company

company = Company.objects.first()
job = Job.objects.create(
    title='Senior React Developer',
    company=company,
    experience_level='senior',
    description='...',
    requirements='...'
)
job.skills_required.add(react)  # Add required skills
job.skills_preferred.add(typescript)  # Add preferred skills
```

### 3. Test the Endpoint

```python
import requests
import json

response = requests.post('http://localhost:8000/api/get-role-requirements/', {
    'role_title': 'Senior React Developer'
}, headers={'X-CSRFToken': csrf_token})

print(response.json())
```

---

## 📋 Troubleshooting

### Issue: "Skills not loading"

**Solution**: Check that user has skills in UserSkill table

```python
from apps.skills.models import UserSkill
UserSkill.objects.filter(user=request.user).count()
```

### Issue: "No job matches found"

**Solution**: Check job database - ensure jobs are created with proper titles

```python
from apps.jobs.models import Job
Job.objects.filter(is_active=True).values_list('title')
```

### Issue: "API returning error"

**Solution**: Check browser console for error details

```javascript
console.log(response.json());  // In JavaScript
```

### Issue: "Charts not rendering"

**Solution**: Ensure Chart.js is loaded and benchmark data is valid

```javascript
console.log(benchmark);  // Check data structure
```

---

## 🚀 Future Enhancements

### Phase 2: Advanced Features

1. **AI-Powered Job Matching**
   - Use ML to find best matching jobs
   - Suggest roles based on user's skills

2. **Resume Parsing**
   - Extract skills from user's resume
   - Auto-populate UserSkill table

3. **Real-Time Market Data**
   - Integrate with job APIs (LinkedIn, Indeed, Glassdoor)
   - Get live role requirements
   - Track market demand trends

4. **Peer Benchmarking**
   - Compare with similar users
   - Show percentile rankings
   - Industry salary insights

5. **Weight & Scoring**
   - Custom weight for skills
   - Industry-specific scoring
   - Goal-aligned prioritization

---

## 📊 Database Queries Reference

### Get User Skills

```python
from apps.skills.models import UserSkill

user_skills = UserSkill.objects.filter(
    user=request.user
).select_related('skill', 'skill__category')

for user_skill in user_skills:
    print(f"{user_skill.skill.name}: {user_skill.proficiency_level}")
```

### Get Job Requirements

```python
from apps.jobs.models import Job

job = Job.objects.get(title__icontains='React Developer')
required_skills = job.skills_required.all()
preferred_skills = job.skills_preferred.all()
```

### Create/Update User Skills

```python
user_skill, created = UserSkill.objects.update_or_create(
    user=user,
    skill=skill,
    defaults={
        'proficiency_level': 'advanced',
        'years_experience': 3.5,
        'is_verified': True
    }
)
```

---

## ✅ Checklist for Usage

- [x] User has skills in UserSkill table (from profile page)
- [x] Jobs exist in Job table with required skills
- [x] User logged in to access skill gap analysis
- [x] API endpoint (/api/get-role-requirements/) accessible
- [x] Chart.js library loaded
- [x] CSRF token properly handled
- [x] Real data displayed in comparisons
- [x] Gaps calculated correctly
- [x] Progress tracked accurately

---

**Version**: 1.0  
**Date**: February 22, 2026  
**Status**: ✅ Complete with Real Data Integration
