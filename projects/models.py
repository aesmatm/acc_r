from django.db import models
from django.conf import settings
from django.utils import timezone

class Project(models.Model):
    STATUS_CHOICES = (
        ('planning', 'تخطيط'),
        ('in_progress', 'قيد التنفيذ'),
        ('completed', 'مكتمل'),
        ('on_hold', 'متوقف'),
        ('cancelled', 'ملغي'),
    )
    
    name = models.CharField(max_length=200, verbose_name='اسم المشروع')
    code = models.CharField(max_length=50, unique=True, verbose_name='رمز المشروع')
    description = models.TextField(blank=True, null=True, verbose_name='وصف المشروع')
    client_name = models.CharField(max_length=200, verbose_name='اسم العميل')
    client_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='هاتف العميل')
    client_email = models.EmailField(blank=True, null=True, verbose_name='بريد العميل')
    
    start_date = models.DateField(verbose_name='تاريخ البدء')
    expected_end_date = models.DateField(verbose_name='تاريخ الانتهاء المتوقع')
    actual_end_date = models.DateField(null=True, blank=True, verbose_name='تاريخ الانتهاء الفعلي')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning', verbose_name='حالة المشروع')
    total_budget = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='الميزانية الكلية')
    
    accountant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'accountant'},
        related_name='assigned_projects',
        verbose_name='المحاسب المسؤول'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    
    class Meta:
        verbose_name = 'مشروع'
        verbose_name_plural = 'المشاريع'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expenses.all())
    
    def get_total_revenues(self):
        return sum(revenue.amount for revenue in self.revenues.all())
    
    def get_profit_loss(self):
        return self.get_total_revenues() - self.get_total_expenses()
    
    def get_budget_usage_percentage(self):
        total_expenses = self.get_total_expenses()
        if self.total_budget:
            return (total_expenses / self.total_budget) * 100
        return 0
    
    def is_over_budget(self):
        return self.get_budget_usage_percentage() > 100
