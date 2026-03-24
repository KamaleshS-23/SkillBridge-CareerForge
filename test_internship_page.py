#!/usr/bin/env python
import os
import sys
import django

# Add the project path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

from django.test import Client

def test_internship_page():
    """Test if internship page loads and shows content"""
    client = Client()
    
    try:
        # Test the internship page
        response = client.get('/internship/')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Internship page loads successfully!")
            content = response.content.decode('utf-8')
            
            # Check if key content is present
            if 'Internship Finder' in content:
                print("✅ Page title found in content")
            else:
                print("❌ Page title not found in content")
                
            if 'My Internship Journey' in content:
                print("✅ My Internships section found")
            else:
                print("❌ My Internships section not found")
                
            # Show first 500 characters of content
            print(f"First 500 chars of content:\n{content[:500]}")
            
        else:
            print(f"❌ Error loading page. Status: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"Error content: {response.content.decode('utf-8')[:200]}")
                
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_internship_page()
