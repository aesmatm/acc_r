from django.contrib import admin
from .models import Item, StockMovement

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'unit', 'price', 'current_stock', 'created_by', 'created_at']
    list_filter = ['unit', 'created_by']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['current_stock', 'created_by', 'created_at', 'updated_at']
    fieldsets = (
        ('معلومات الصنف', {
            'fields': ('name', 'code', 'unit', 'price', 'description')
        }),
        ('معلومات المخزون', {
            'fields': ('current_stock',)
        }),
        ('معلومات النظام', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by when creating a new item
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['item', 'movement_type', 'quantity', 'date', 'created_by']
    list_filter = ['movement_type', 'date', 'created_by']
    search_fields = ['item__name', 'item__code', 'notes']
    readonly_fields = ['created_by', 'created_at']
    date_hierarchy = 'date'
    fieldsets = (
        ('معلومات الحركة', {
            'fields': ('item', 'movement_type', 'quantity', 'date')
        }),
        ('معلومات إضافية', {
            'fields': ('notes',)
        }),
        ('معلومات النظام', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by when creating a new movement
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
