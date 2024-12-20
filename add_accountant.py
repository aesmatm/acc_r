import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construction_accounting.settings')
django.setup()

from accounts.models import User

# Create a new accountant
User.objects.create_user(
    username='accountant1',
    password='accountant123',
    email='accountant1@example.com',
    first_name='Mohammed',
    last_name='Ahmed',
    role='accountant',
    is_staff=True
)

print("New accountant added successfully")
