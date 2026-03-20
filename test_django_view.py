from django.test import RequestFactory
from django.contrib.auth import get_user_model
from apps.core.views import get_role_requirements
import json

User = get_user_model()
user = User.objects.first()

if not user:
    print("No user found.")
else:
    factory = RequestFactory()
    data = {
        "role_title": "Senior React Developer",
        "experience_level": "Senior",
        "industry": "",
        "career_path": ""
    }
    request = factory.post('/api/get-role-requirements/', data=json.dumps(data), content_type='application/json')
    request.user = user

    try:
        response = get_role_requirements(request)
        print("Status Code:", response.status_code)
        print("Response:", response.content.decode('utf-8'))
    except Exception as e:
        print("View Error:", str(e))
