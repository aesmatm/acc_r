from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Report

# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'date_from', 'date_to', 'created_at', 'created_by', 'view_report_button']
    list_filter = ['report_type', 'created_at', 'created_by']
    search_fields = ['title', 'report_type']
    readonly_fields = ['created_at', 'created_by']
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # إذا كان التقرير جديداً
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def view_report_button(self, obj):
        url = reverse('reports:generate_report', kwargs={'report_type': obj.report_type})
        return format_html(
            '<a class="button" href="{}?id={}" target="_blank">'
            '<i class="fas fa-print"></i> عرض وطباعة التقرير</a>',
            url, obj.id
        )
    view_report_button.short_description = 'عرض/طباعة'
