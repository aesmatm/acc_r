from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey

class AccountTree(MPTTModel):
    ACCOUNT_TYPES = (
        ('asset', 'أصول'),
        ('liability', 'خصوم'),
        ('equity', 'حقوق ملكية'),
        ('revenue', 'إيرادات'),
        ('expense', 'مصروفات'),
    )
    
    code = models.CharField(max_length=20, unique=True, verbose_name='رمز الحساب')
    name = models.CharField(max_length=200, verbose_name='اسم الحساب')
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, verbose_name='نوع الحساب')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='الحساب الأب')
    description = models.TextField(blank=True, null=True, verbose_name='الوصف')
    
    class Meta:
        verbose_name = 'حساب'
        verbose_name_plural = 'شجرة الحسابات'
        
    class MPTTMeta:
        order_insertion_by = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('expense', 'مصروف'),
        ('revenue', 'إيراد'),
        ('journal', 'قيد يومية'),
    )
    
    date = models.DateField(verbose_name='التاريخ')
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name='نوع المعاملة')
    description = models.TextField(verbose_name='الوصف')
    reference_number = models.CharField(max_length=50, unique=True, verbose_name='رقم المرجع')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='transactions', verbose_name='المشروع')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='تم الإنشاء بواسطة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    
    class Meta:
        verbose_name = 'معاملة مالية'
        verbose_name_plural = 'المعاملات المالية'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.reference_number}"

class TransactionLine(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='lines', verbose_name='المعاملة')
    account = models.ForeignKey(AccountTree, on_delete=models.PROTECT, verbose_name='الحساب')
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='مدين')
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='دائن')
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name='الوصف')
    
    class Meta:
        verbose_name = 'بند معاملة'
        verbose_name_plural = 'بنود المعاملات'
    
    def __str__(self):
        return f"{self.account.name} ({self.debit or self.credit})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.debit and self.credit:
            raise ValidationError('لا يمكن أن يكون الحساب مدين ودائن في نفس الوقت')
        if not self.debit and not self.credit:
            raise ValidationError('يجب تحديد قيمة مدينة أو دائنة')
