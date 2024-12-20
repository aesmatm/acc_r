from django.contrib import admin
from django.contrib.admin.apps import AdminConfig

# تنظيم التطبيقات في مجموعات
class CustomAdminSite(admin.AdminSite):
    site_header = 'نظام إدارة المقاولات'
    site_title = 'نظام إدارة المقاولات'
    index_title = 'لوحة التحكم'

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        app_dict = {}
        
        # تجميع التطبيقات في مجموعات
        groups = {
            'إدارة الشركة': {
                'icon': 'fas fa-building',
                'apps': ['company'],
                'order': 1,
            },
            'المعاملات المالية': {
                'icon': 'fas fa-money-bill',
                'apps': ['finance', 'suppliers', 'invoices'],
                'order': 2,
            },
            'إدارة المخزون': {
                'icon': 'fas fa-warehouse',
                'apps': ['inventory'],
                'order': 3,
            },
            'إدارة المشاريع': {
                'icon': 'fas fa-project-diagram',
                'apps': ['projects'],
                'order': 4,
            },
            'التقارير والإحصائيات': {
                'icon': 'fas fa-chart-bar',
                'apps': ['reports'],
                'order': 5,
            },
            'إدارة النظام': {
                'icon': 'fas fa-cogs',
                'apps': ['accounts', 'auth', 'sites'],
                'order': 6,
            },
        }

        # تنظيم التطبيقات حسب المجموعات
        for app in app_list:
            app_name = app['app_label']
            for group_name, group_info in groups.items():
                if app_name in group_info['apps']:
                    if group_name not in app_dict:
                        app_dict[group_name] = {
                            'name': group_name,
                            'icon': group_info['icon'],
                            'order': group_info['order'],
                            'models': [],
                        }
                    app_dict[group_name]['models'].extend(app['models'])

        # ترتيب المجموعات
        sorted_app_list = [
            {'name': name, 'icon': data['icon'], 'models': data['models']}
            for name, data in sorted(app_dict.items(), key=lambda x: x[1]['order'])
        ]

        return sorted_app_list

# تكوين لوحة التحكم المخصصة
class CustomAdminConfig(AdminConfig):
    default_site = 'construction_accounting.admin.CustomAdminSite'
