from django.contrib import admin
from .models import Project

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'client_name', 'status', 'start_date', 'accountant')
    list_filter = ('status', 'accountant')
    search_fields = ('name', 'code', 'client_name')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('معلومات المشروع', {
            'fields': ('name', 'code', 'description', 'status')
        }),
        ('معلومات العميل', {
            'fields': ('client_name', 'client_phone', 'client_email')
        }),
        ('التواريخ', {
            'fields': ('start_date', 'expected_end_date', 'actual_end_date')
        }),
        ('المالية', {
            'fields': ('total_budget', 'accountant')
        }),
        ('معلومات النظام', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
