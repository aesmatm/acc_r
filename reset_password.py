import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'construction_accounting.settings')
django.setup()

from accounts.models import User

# Get the user
user = User.objects.get(username='admin')

# Set new password
new_password = 'admin123'
user.set_password(new_password)
user.save()

print(f"Password has been reset for user: {user.username}")
print(f"New login credentials:")
print(f"Username: {user.username}")
print(f"Password: {new_password}")
