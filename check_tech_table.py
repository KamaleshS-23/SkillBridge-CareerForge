import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check specifically for TechnicalTestResult table
cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="skills_technicaltestresult"')
table_exists = cursor.fetchone()

if table_exists:
    print('✅ skills_technicaltestresult table exists')
    cursor.execute('SELECT COUNT(*) FROM skills_technicaltestresult')
    count = cursor.fetchone()[0]
    print(f'📈 Records: {count}')
    
    # Get table schema
    cursor.execute('PRAGMA table_info(skills_technicaltestresult)')
    columns = cursor.fetchall()
    print('\n📋 Table Structure:')
    for col in columns:
        print(f'   • {col[1]} ({col[2]})')
else:
    print('❌ skills_technicaltestresult table does NOT exist')

conn.close()
