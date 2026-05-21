import os
import sys
import django
from django.db import connection

# Add the project root to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ivhemms_project.settings')
django.setup()

with connection.cursor() as cursor:
    print("Columns for 'appointment' table:")
    cursor.execute("DESCRIBE appointment")
    columns = cursor.fetchall()
    for col in columns:
        print(f"{col[0]}: {col[1]}")
