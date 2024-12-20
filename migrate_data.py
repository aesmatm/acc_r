import os
import django
from django.core.management import call_command
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construction_accounting.settings')
django.setup()

def transfer_data():
    # Create tables in MySQL if they don't exist
    call_command('migrate')
    
    # Copy data from each model
    apps = [
        'accounts',
        'finance',
        'invoices',
        'projects',
        'suppliers',
        'auth'
    ]
    
    for app in apps:
        try:
            # Load data from SQLite
            print(f"Copying data from {app}...")
            call_command('inspectdb', app)
            call_command('loaddata', f'{app}_data.json')
        except Exception as e:
            print(f"Error copying {app}: {str(e)}")

if __name__ == '__main__':
    transfer_data()
