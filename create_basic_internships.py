#!/usr/bin/env python
import os
import sys
import django

# Add the project path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

def create_basic_internships():
    """Create basic internship data using direct SQL to avoid model field issues"""
    
    try:
        from django.db import connection
        
        # Create basic internships using raw SQL to avoid model field issues
        internships_data = [
            (1, 'Frontend Developer Intern', 'TechCorp Solutions', 'Join our team to build modern web applications using React and TypeScript. Work on real projects and learn from experienced developers.', 'Remote', '3 months', '$500/month', 'Basic knowledge of HTML, CSS, JavaScript. Experience with React is a plus.', 'React, JavaScript, TypeScript, HTML, CSS', 'https://techcorp.com/careers/frontend-intern', 'Company Website', 1),
            (2, 'Full Stack Developer Intern', 'StartupHub', 'Work on both frontend and backend development. Build features from database to user interface.', 'Hybrid', '6 months', '$800/month', 'Knowledge of Python, JavaScript, databases. Full stack experience preferred.', 'Python, Django, React, PostgreSQL, Git', 'https://startuphub.io/jobs/fullstack-intern', 'LinkedIn', 1),
            (3, 'React Developer Intern', 'Innovation Labs', 'Focus on React development for cutting-edge web applications. Work with modern tools and frameworks.', 'Remote', '3 months', '$700/month', 'Strong JavaScript skills, React experience, understanding of state management.', 'React, Redux, JavaScript ES6+, CSS, Git', 'https://innovationlabs.tech/careers/react-intern', 'AngelList', 1),
            (4, 'Backend Developer Intern', 'DataFlow Systems', 'Build robust backend services and APIs. Learn modern backend technologies and best practices.', 'Remote', '4 months', '$600/month', 'Knowledge of Python, databases, REST APIs. Experience with cloud platforms preferred.', 'Python, Django, PostgreSQL, REST APIs, Docker', 'https://dataflow.com/careers/backend-intern', 'Company Website', 0),
            (5, 'UI/UX Design Intern', 'Creative Studios', 'Design beautiful user interfaces and experiences. Work with modern design tools and collaborate with development teams.', 'Hybrid', '3 months', '$400/month', 'Knowledge of design tools, user research, prototyping. Portfolio required.', 'Figma, Adobe Creative Suite, HTML, CSS, User Research', 'https://creativestudios.com/careers/ux-intern', 'Company Website', 1),
        ]
        
        with connection.cursor() as cursor:
            # Check if core_internship table exists and has the right structure
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_internship'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                # Check table structure
                cursor.execute("PRAGMA table_info(core_internship)")
                columns = [row[1] for row in cursor.fetchall()]
                
                print(f"Table columns found: {columns}")
                
                # Insert data based on available columns
                for internship in internships_data:
                    id_, title, company, description, location, duration, stipend, requirements, skills_required, application_url, source, is_featured = internship
                    
                    # Try to insert with basic columns first
                    try:
                        cursor.execute("""
                            INSERT INTO core_internship (title, company, description, location, duration, stipend, requirements, skills_required, application_url, source, is_featured, posted_date, status, created_at, updated_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), 'active', datetime('now'), datetime('now'))
                        """, (title, company, description, location, duration, stipend, requirements, skills_required, application_url, source, is_featured))
                        print(f"✅ Created internship: {title}")
                    except Exception as e:
                        print(f"❌ Error inserting {title}: {str(e)}")
                        # Try with fewer columns if some don't exist
                        try:
                            cursor.execute("""
                                INSERT INTO core_internship (title, company, description, location, duration, stipend, requirements, skills_required, application_url, source, posted_date, status, created_at, updated_at)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), 'active', datetime('now'), datetime('now'))
                            """, (title, company, description, location, duration, stipend, requirements, skills_required, application_url, source))
                            print(f"✅ Created internship (basic columns): {title}")
                        except Exception as e2:
                            print(f"❌ Error with basic columns: {str(e2)}")
            else:
                print("❌ core_internship table does not exist")
        
        connection.commit()
        print(f"\n✅ Internship data creation completed!")
        
        # Display summary
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM core_internship")
            total_count = cursor.fetchone()[0]
            print(f"Total internships in database: {total_count}")
            
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_basic_internships()
