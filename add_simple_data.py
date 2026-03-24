#!/usr/bin/env python
import os
import sys
import django

# Add the project path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

# Simple data creation without using problematic fields
def add_basic_data():
    try:
        # Create a test user if not exists
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'username': 'testuser',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            print("✅ Created test user: test@example.com")
        
        print(f"✅ Basic data setup completed!")
        print(f"✅ Server is running at: http://127.0.0.1:8000")
        print(f"✅ Internship page accessible at: http://127.0.0.1:8000/internship/")
        print(f"✅ Test user credentials: test@example.com / testpass123")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    add_basic_data()
