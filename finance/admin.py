from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import AccountTree, Transaction, TransactionLine

@admin.register(AccountTree)
class AccountTreeAdmin(MPTTModelAdmin):
    list_display = ('code', 'name', 'account_type', 'parent')
    list_filter = ('account_type',)
    search_fields = ('code', 'name')
    mptt_level_indent = 20

class TransactionLineInline(admin.TabularInline):
    model = TransactionLine
    extra = 1
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'date', 'type', 'project', 'created_by')
    list_filter = ('type', 'project', 'created_by')
    search_fields = ('reference_number', 'description')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'created_by')
    inlines = [TransactionLineInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # إذا كان إنشاء جديد
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
