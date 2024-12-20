from django.db import models
from django.conf import settings
from django.urls import reverse
from suppliers.models import Supplier
from decimal import Decimal
from inventory.models import Item, StockMovement
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Invoice(models.Model):
    TAX_STATUS_CHOICES = [
        ('taxable', 'خاضع للضريبة'),
        ('exempt', 'معفى من الضريبة'),
        ('zero_rated', 'نسبة صفرية'),
    ]

    number = models.CharField(max_length=50, unique=True, verbose_name='رقم الفاتورة', blank=True)
    date = models.DateField(verbose_name='تاريخ الفاتورة')
    supplier = models.ForeignKey(
        Supplier, 
        on_delete=models.PROTECT, 
        related_name='supplier_invoices',
        verbose_name='المورد'
    )
    tax_status = models.CharField(
        max_length=20,
        choices=TAX_STATUS_CHOICES,
        default='taxable',
        verbose_name='حالة الضريبة'
    )
    tax_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('15.00'), 
        verbose_name='نسبة الضريبة %'
    )
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='created_invoices',
        verbose_name='تم الإنشاء بواسطة'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'فاتورة'
        verbose_name_plural = 'الفواتير'
        ordering = ['-date', '-number']

    def __str__(self):
        return f"فاتورة رقم {self.number}"

    def get_absolute_url(self):
        return reverse('invoices:invoice_detail', args=[str(self.id)])

    @property
    def subtotal(self):
        return sum(item.total for item in self.items.all())

    @property
    def total_amount(self):
        """حساب إجمالي قيمة الفاتورة"""
        total = sum(item.quantity * item.price for item in self.items.all())
        return total

    @property
    def tax_amount(self):
        """حساب قيمة الضريبة"""
        if self.tax_status == 'taxable':
            return self.total_amount * (self.tax_rate / Decimal('100.0'))
        return Decimal('0.00')

    @property
    def total_with_tax(self):
        """حساب الإجمالي شامل الضريبة"""
        return self.total_amount + self.tax_amount

    @property
    def tax_amount_original(self):
        if self.tax_status == 'exempt' or self.tax_status == 'zero_rated':
            return Decimal('0.00')
        return (self.subtotal * self.tax_rate / Decimal('100')).quantize(Decimal('0.01'))

    @property
    def total_original(self):
        return self.subtotal + self.tax_amount_original

    def save(self, *args, **kwargs):
        if not self.number:
            # Get the last invoice number
            last_invoice = Invoice.objects.order_by('-number').first()
            if last_invoice and last_invoice.number.isdigit():
                self.number = str(int(last_invoice.number) + 1).zfill(4)
            else:
                self.number = '0001'  # Start with 0001 if no previous invoices
        super().save(*args, **kwargs)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items', verbose_name='الفاتورة')
    item = models.ForeignKey(
        Item, 
        on_delete=models.PROTECT, 
        related_name='invoice_items', 
        verbose_name='الصنف',
        null=True,  # Allow null temporarily for migration
        blank=True
    )
    description = models.CharField(max_length=255, verbose_name='الوصف')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='الكمية')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='السعر')

    class Meta:
        verbose_name = 'بند الفاتورة'
        verbose_name_plural = 'بنود الفاتورة'

    def __str__(self):
        return f"{self.item.name} - {self.invoice.number}"

    @property
    def total(self):
        if self.quantity is None or self.price is None:
            return Decimal('0.00')
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Create stock movement for new items
            StockMovement.objects.create(
                item=self.item,
                movement_type='in',
                quantity=self.quantity,
                date=self.invoice.date,
                notes=f'وارد من فاتورة رقم {self.invoice.number}',
                created_by=self.invoice.created_by
            )

@receiver(post_delete, sender=InvoiceItem)
def handle_deleted_invoice_item(sender, instance, **kwargs):
    # Create reverse stock movement when item is deleted
    StockMovement.objects.create(
        item=instance.item,
        movement_type='out',
        quantity=instance.quantity,
        date=instance.invoice.date,
        notes=f'إلغاء وارد من فاتورة رقم {instance.invoice.number}',
        created_by=instance.invoice.created_by
    )
