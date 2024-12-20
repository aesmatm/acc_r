from django.db import models
from django.conf import settings

class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name='اسم المورد')
    code = models.CharField(max_length=50, unique=True, verbose_name='رمز المورد')
    contact_person = models.CharField(max_length=200, blank=True, null=True, verbose_name='الشخص المسؤول')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
    email = models.EmailField(blank=True, null=True, verbose_name='البريد الإلكتروني')
    address = models.TextField(blank=True, null=True, verbose_name='العنوان')
    tax_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='الرقم الضريبي')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    
    class Meta:
        verbose_name = 'مورد'
        verbose_name_plural = 'الموردين'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_total_invoices(self):
        return self.invoices.count()
    
    def get_total_amount(self):
        return sum(invoice.total_amount for invoice in self.invoices.all())

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('draft', 'مسودة'),
        ('approved', 'معتمد'),
        ('paid', 'مدفوع'),
        ('cancelled', 'ملغي'),
    )
    
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='invoices', verbose_name='المورد')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='supplier_invoices', verbose_name='المشروع')
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name='رقم الفاتورة')
    invoice_date = models.DateField(verbose_name='تاريخ الفاتورة')
    due_date = models.DateField(verbose_name='تاريخ الاستحقاق')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='الحالة')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='المبلغ الإجمالي')
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='مبلغ الضريبة')
    
    description = models.TextField(blank=True, null=True, verbose_name='الوصف')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='تم الإنشاء بواسطة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    
    class Meta:
        verbose_name = 'فاتورة مورد'
        verbose_name_plural = 'فواتير الموردين'
        ordering = ['-invoice_date', '-created_at']
    
    def __str__(self):
        return f"فاتورة {self.invoice_number} - {self.supplier.name}"
    
    def get_total_with_tax(self):
        return self.total_amount + self.tax_amount

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items', verbose_name='الفاتورة')
    description = models.CharField(max_length=200, verbose_name='الوصف')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='الكمية')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='سعر الوحدة')
    
    class Meta:
        verbose_name = 'بند الفاتورة'
        verbose_name_plural = 'بنود الفاتورة'
    
    def __str__(self):
        return f"{self.description} ({self.quantity} × {self.unit_price})"
    
    def get_total(self):
        return self.quantity * self.unit_price
