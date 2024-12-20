import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construction_accounting.settings')
django.setup()

from accounts.models import User

# Create new superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        role='admin',
        first_name='Admin',
        last_name='System'
    )
    print('Superuser created successfully')
