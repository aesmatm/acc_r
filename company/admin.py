from django.contrib import admin
from django.utils.html import format_html
from .models import CompanyInfo

# Register your models here.

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'tax_number', 'show_logo']
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('name', 'logo', 'address'),
            'classes': ('wide',)
        }),
        ('معلومات الاتصال', {
            'fields': ('phone', 'mobile', 'email', 'website'),
            'classes': ('wide',)
        }),
        ('معلومات قانونية', {
            'fields': ('tax_number', 'commercial_record'),
            'classes': ('wide',)
        }),
    )

    def show_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        return "لا يوجد شعار"
    show_logo.short_description = 'الشعار'

    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not CompanyInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False

# تخصيص لوحة الإدارة
admin.site.site_header = 'نظام إدارة المقاولات'
admin.site.site_title = 'نظام إدارة المقاولات'
admin.site.index_title = 'لوحة التحكم'

# تنظيم التطبيقات في لوحة الإدارة
class CompanyAdminArea(admin.AdminSite):
    site_header = 'نظام إدارة المقاولات'
    site_title = 'نظام إدارة المقاولات'
    index_title = 'لوحة التحكم'

# إعادة تنظيم التطبيقات في مجموعات
admin.site.index_template = 'admin/custom_index.html'
