import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print('DATABASE TABLES AND RECORDS')
print('=' * 50)

cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()

total_records = 0
for table_name, in tables:
    cursor.execute('SELECT COUNT(*) FROM ' + table_name)
    count = cursor.fetchone()[0]
    if count > 0:
        print(f'{table_name}: {count} records')
        total_records += count

print('=' * 50)
print(f'TOTAL RECORDS: {total_records}')

conn.close()
