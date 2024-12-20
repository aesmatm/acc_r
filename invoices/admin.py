from django.contrib import admin
from django.db import models
from .models import Invoice, InvoiceItem
from django.forms import TextInput, NumberInput

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ['item', 'description', 'quantity', 'price', 'get_total']
    readonly_fields = ['get_total']
    autocomplete_fields = ['item']
    formfield_overrides = {
        models.DecimalField: {'widget': NumberInput(attrs={'class': 'calc-trigger'})},
    }

    def get_total(self, obj):
        if obj.quantity and obj.price:
            return obj.quantity * obj.price
        return 0
    get_total.short_description = 'الإجمالي'

    class Media:
        js = ('js/invoice_calculations.js',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['number', 'date', 'supplier', 'get_total_amount', 'get_tax_amount', 'get_total_with_tax', 'created_by', 'created_at']
    list_filter = ['date', 'supplier', 'created_by']
    search_fields = ['number', 'supplier__name', 'notes']
    date_hierarchy = 'date'
    inlines = [InvoiceItemInline]
    readonly_fields = ['created_by', 'created_at', 'updated_at', 'get_total_amount', 'get_tax_amount', 'get_total_with_tax']
    
    fieldsets = (
        ('معلومات الفاتورة', {
            'fields': ('number', 'date', 'supplier', 'tax_status', 'tax_rate')
        }),
        ('المبالغ', {
            'fields': ('get_total_amount', 'get_tax_amount', 'get_total_with_tax')
        }),
        ('معلومات إضافية', {
            'fields': ('notes',)
        }),
        ('معلومات النظام', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_total_amount(self, obj):
        return obj.total_amount
    get_total_amount.short_description = 'المبلغ قبل الضريبة'

    def get_tax_amount(self, obj):
        return obj.tax_amount
    get_tax_amount.short_description = 'مبلغ الضريبة'

    def get_total_with_tax(self, obj):
        return obj.total_with_tax
    get_total_with_tax.short_description = 'الإجمالي شامل الضريبة'

    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by when creating a new invoice
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.description:  # Auto-fill description from item if empty
                instance.description = instance.item.name
            instance.save()
        formset.save_m2m()

    class Media:
        js = ('js/invoice_calculations.js',)
