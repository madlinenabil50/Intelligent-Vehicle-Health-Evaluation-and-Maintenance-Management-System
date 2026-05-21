import os
import sys
import django
from django.db import connection

# Add the project root to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ivhemms_project.settings')
django.setup()

with connection.cursor() as cursor:
    print("Removing 'notes' from appointment table...")
    try:
        cursor.execute("ALTER TABLE appointment DROP COLUMN notes")
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

    print("Removing 'CustomerCategory' from client table...")
    try:
        cursor.execute("ALTER TABLE client DROP COLUMN CustomerCategory")
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")
