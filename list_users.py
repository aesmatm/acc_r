import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construction_accounting.settings')
django.setup()

from accounts.models import User

print("\nAll Users List:")
print("-" * 50)

users = User.objects.all()
for user in users:
    print(f"Username: {user.username}")
    print(f"Full Name: {user.get_full_name()}")
    print(f"Email: {user.email}")
    print(f"Role: {user.role}")
    print(f"Is Staff: {user.is_staff}")
    print(f"Is Superuser: {user.is_superuser}")
    print("-" * 30)
