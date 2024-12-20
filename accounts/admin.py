from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render, redirect
from django.contrib.admin.options import IS_POPUP_VAR
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'password_change_link')
    list_filter = ('is_staff', 'is_superuser', 'role')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('المعلومات الشخصية', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address')}),
        ('الصلاحيات', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تواريخ مهمة', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'email', 'first_name', 'last_name'),
        }),
    )
    
    def password_change_link(self, obj):
        change_password_url = reverse('admin:auth_user_password_change', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="background-color: #2a8241; color: white; '
            'padding: 5px 10px; border-radius: 4px; text-decoration: none;">'
            'تغيير كلمة المرور</a>',
            change_password_url
        )
    password_change_link.short_description = 'تغيير كلمة المرور'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<id>/password/',
                self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change',
            ),
        ]
        return custom_urls + urls
    
    def user_change_password(self, request, id, form_url=''):
        user = self.get_object(request, id)
        if not user:
            return self._get_obj_does_not_exist_redirect(request, self.model._meta, id)
            
        if request.method == 'POST':
            form = AdminPasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                self.message_user(request, 'تم تغيير كلمة المرور بنجاح.')
                return redirect('admin:accounts_user_change', id)
        else:
            form = AdminPasswordChangeForm(user)
            
        fieldsets = [(None, {'fields': list(form.base_fields)})]
        admin_form = admin.helpers.AdminForm(form, fieldsets, {})
        
        context = {
            'title': f'تغيير كلمة المرور: {user.username}',
            'adminForm': admin_form,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            **self.admin_site.each_context(request),
        }
        
        request.current_app = self.admin_site.name
        
        return render(request, 'admin/auth/user/change_password.html', context)
