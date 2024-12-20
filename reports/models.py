from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Report(models.Model):
    REPORT_TYPES = [
        ('inventory', 'تقرير المخزون'),
        ('invoices', 'تقرير الفواتير'),
        ('suppliers', 'تقرير الموردين'),
        ('projects', 'تقرير المشاريع'),
        ('finance', 'تقرير المالية'),
    ]

    title = models.CharField('عنوان التقرير', max_length=200)
    report_type = models.CharField('نوع التقرير', max_length=20, choices=REPORT_TYPES)
    date_from = models.DateField('من تاريخ')
    date_to = models.DateField('إلى تاريخ')
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='تم الإنشاء بواسطة')
    
    class Meta:
        verbose_name = 'تقرير'
        verbose_name_plural = 'التقارير'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.title}"
