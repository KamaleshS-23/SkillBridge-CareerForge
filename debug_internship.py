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
from django.template import loader, Context

def debug_internship_page():
    """Debug the internship page by checking template rendering"""
    client = Client()
    
    try:
        # Test the internship page
        response = client.get('/internship/')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Internship page loads successfully!")
            
            # Try to render the template directly
            template = loader.get_template('core/internship.html')
            context = {
                'page_title': 'Internship Finder',
                'page_description': 'Search internships across top companies worldwide',
            }
            
            # Render template to check for errors
            try:
                rendered = template.render(context)
                print("✅ Template renders successfully!")
                print(f"Template length: {len(rendered)} characters")
                
                # Check if key sections are present
                if 'My Internship Journey' in rendered:
                    print("✅ My Internship Journey section found")
                if 'Internship Statistics' in rendered:
                    print("✅ Internship Statistics section found")
                if 'Available Internships' in rendered:
                    print("✅ Available Internships section found")
                    
            except Exception as e:
                print(f"❌ Template rendering error: {str(e)}")
                
        else:
            print(f"❌ Error loading page. Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_internship_page()
