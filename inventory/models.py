from django.db import models
from django.conf import settings
from decimal import Decimal

class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name='اسم الصنف')
    code = models.CharField(max_length=50, unique=True, verbose_name='كود الصنف')
    unit = models.CharField(max_length=50, verbose_name='وحدة القياس')
    description = models.TextField(blank=True, null=True, verbose_name='الوصف')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='سعر الوحدة')
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='الرصيد الحالي')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_items',
        verbose_name='تم الإنشاء بواسطة'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'صنف'
        verbose_name_plural = 'الأصناف'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'وارد'),
        ('out', 'منصرف'),
    ]

    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='movements', verbose_name='الصنف')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES, verbose_name='نوع الحركة')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='الكمية')
    date = models.DateField(verbose_name='التاريخ')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_movements',
        verbose_name='تم الإنشاء بواسطة'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'حركة مخزنية'
        verbose_name_plural = 'حركات المخزن'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.item.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        if self.movement_type == 'in':
            self.item.current_stock += self.quantity
        else:
            self.item.current_stock -= self.quantity
        self.item.save()
        super().save(*args, **kwargs)
