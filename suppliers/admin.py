from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Supplier, Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'phone', 'email', 'tax_number')
    search_fields = ('name', 'code', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('معلومات المورد', {
            'fields': ('name', 'code', 'contact_person')
        }),
        ('معلومات الاتصال', {
            'fields': ('phone', 'email', 'address')
        }),
        ('معلومات ضريبية', {
            'fields': ('tax_number',)
        }),
        ('معلومات النظام', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'supplier', 'project', 'invoice_date', 'total_amount', 'status', 'print_button')
    list_filter = ('status', 'supplier', 'project')
    search_fields = ('invoice_number', 'supplier__name', 'description')
    date_hierarchy = 'invoice_date'
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    inlines = [InvoiceItemInline]
    
    fieldsets = (
        ('معلومات الفاتورة', {
            'fields': ('invoice_number', 'supplier', 'project')
        }),
        ('التواريخ', {
            'fields': ('invoice_date', 'due_date')
        }),
        ('المبالغ', {
            'fields': ('total_amount', 'tax_amount')
        }),
        ('معلومات إضافية', {
            'fields': ('status', 'description', 'notes')
        }),
        ('معلومات النظام', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def print_button(self, obj):
        url = reverse('suppliers:invoice_print', kwargs={'pk': obj.pk})
        return format_html(
            '<a href="{}" target="_blank" class="button" style="background-color: #027448;">'
            '<i class="fas fa-print"></i> طباعة</a>',
            url
        )
    print_button.short_description = 'طباعة'
    
    def save_model(self, request, obj, form, change):
        if not change:  # إذا كان إنشاء جديد
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',)
        }
