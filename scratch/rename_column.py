import os
import sys
import django
from django.db import connection

# Add the project root to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ivhemms_project.settings')
django.setup()

with connection.cursor() as cursor:
    print("Renaming StartTime to date_time in appointment table...")
    try:
        cursor.execute("ALTER TABLE appointment CHANGE StartTime date_time DATETIME")
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")
