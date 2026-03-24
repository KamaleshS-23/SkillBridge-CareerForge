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

def test_urls():
    """Test both internship URLs"""
    client = Client()
    
    print("=== Testing Internship URLs ===")
    
    # Test /internship/
    response1 = client.get('/internship/')
    print(f"✅ /internship/ - Status: {response1.status_code}")
    
    # Test /internship-finder/
    response2 = client.get('/internship-finder/')
    print(f"✅ /internship-finder/ - Status: {response2.status_code}")
    
    if response1.status_code == 200 and response2.status_code == 200:
        print("\n🎉 SUCCESS: Both URLs are working!")
        print("\n📱 Browser Access URLs:")
        print("   - http://127.0.0.1:8000/internship/")
        print("   - http://127.0.0.1:8000/internship-finder/")
        print("\n💡 If still getting 404 in browser:")
        print("   1. Refresh the page (Ctrl+F5)")
        print("   2. Clear browser cache")
        print("   3. Try the other URL")
    else:
        print(f"\n❌ ERROR: URLs not working properly")

if __name__ == '__main__':
    test_urls()
