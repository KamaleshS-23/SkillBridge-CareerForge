import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('📊 TECHNICAL TEST DATABASE OVERVIEW')
print('=' * 60)

# Check if TechnicalTestResult table exists
cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="skills_technicaltestresult"')
table_exists = cursor.fetchone()

if table_exists:
    print('✅ TechnicalTestResult table exists')
    
    # Get total records
    cursor.execute('SELECT COUNT(*) FROM skills_technicaltestresult')
    total_records = cursor.fetchone()[0]
    print(f'📈 Total test records: {total_records:,}')
    
    if total_records > 0:
        # Get unique users
        cursor.execute('SELECT COUNT(DISTINCT user_id) FROM skills_technicaltestresult')
        unique_users = cursor.fetchone()[0]
        print(f'👥 Unique users who took tests: {unique_users:,}')
        
        # Get subject breakdown
        cursor.execute('SELECT subject, COUNT(*) as count FROM skills_technicaltestresult GROUP BY subject ORDER BY count DESC')
        subjects = cursor.fetchall()
        print('\n📚 Tests by Subject:')
        for subject, count in subjects:
            print(f'   • {subject:<25} {count:>6:,} tests')
        
        # Get difficulty breakdown
        cursor.execute('SELECT difficulty, COUNT(*) as count FROM skills_technicaltestresult GROUP BY difficulty ORDER BY count DESC')
        difficulties = cursor.fetchall()
        print('\n🎯 Tests by Difficulty:')
        for difficulty, count in difficulties:
            print(f'   • {difficulty:<15} {count:>6:,} tests')
        
        # Get average scores
        cursor.execute('SELECT AVG(percentage) as avg_score FROM skills_technicaltestresult')
        avg_score = cursor.fetchone()[0]
        if avg_score:
            print(f'\n📊 Average score across all tests: {avg_score:.1f}%')
        
        # Get recent tests
        cursor.execute('SELECT subject, difficulty, score, total_questions, percentage, test_date FROM skills_technicaltestresult ORDER BY test_date DESC LIMIT 5')
        recent_tests = cursor.fetchall()
        print('\n🕐 Recent Test Results:')
        for i, (subject, difficulty, score, total, percentage, date) in enumerate(recent_tests, 1):
            print(f'   {i}. {subject} ({difficulty}) - {score}/{total} ({percentage:.1f}%) - {date}')
    else:
        print('📝 No test records found yet')
else:
    print('❌ TechnicalTestResult table does not exist')

print('=' * 60)

# Also check all tables
print('\n🔍 ALL DATABASE TABLES')
print('=' * 40)
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()

total_records = 0
for table_name, in tables:
    cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
    count = cursor.fetchone()[0]
    if count > 0:
        print(f'📋 {table_name:<35} {count:>6} records')
        total_records += count

print('=' * 40)
print(f'📊 TOTAL RECORDS: {total_records:,}')

conn.close()
