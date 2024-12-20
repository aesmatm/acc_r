from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'مدير'),
        ('accountant', 'محاسب'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='accountant', verbose_name='الدور')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='رقم الهاتف')
    address = models.TextField(blank=True, null=True, verbose_name='العنوان')
    
    class Meta:
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمين'
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
