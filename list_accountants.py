import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construction_accounting.settings')
django.setup()

from accounts.models import User

print("\nRegistered Accountants List:")
print("-" * 50)

accountants = User.objects.filter(role='accountant')
if accountants:
    for accountant in accountants:
        print(f"Name: {accountant.get_full_name() or accountant.username}")
        print(f"Email: {accountant.email}")
        print(f"Active: {'Yes' if accountant.is_active else 'No'}")
        print("-" * 30)
else:
    print("No accountants registered yet")

print("\nTotal accountants:", accountants.count())
