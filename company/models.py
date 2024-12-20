from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class CompanyInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name='اسم الشركة')
    address = models.TextField(verbose_name='العنوان')
    phone = models.CharField(max_length=50, verbose_name='رقم الهاتف')
    mobile = models.CharField(max_length=50, blank=True, null=True, verbose_name='رقم الجوال')
    email = models.EmailField(verbose_name='البريد الإلكتروني')
    website = models.URLField(blank=True, null=True, verbose_name='الموقع الإلكتروني')
    tax_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='الرقم الضريبي')
    commercial_record = models.CharField(max_length=50, blank=True, null=True, verbose_name='السجل التجاري')
    logo = models.ImageField(upload_to='company/', blank=True, null=True, verbose_name='شعار الشركة')

    def clean(self):
        # Ensure only one instance exists
        if not self.pk and CompanyInfo.objects.exists():
            raise ValidationError('لا يمكن إضافة أكثر من معلومات شركة واحدة')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'معلومات الشركة'
        verbose_name_plural = 'معلومات الشركة'

    def __str__(self):
        return self.name
