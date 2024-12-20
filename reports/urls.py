from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('generate/<str:report_type>/', views.generate_report, name='generate_report'),
    path('view/<str:report_type>/', views.view_report, name='view_report'),
    path('print/<str:report_type>/', views.print_report, name='print_report'),
    path('export-pdf/<str:report_type>/', views.export_pdf, name='export_pdf'),
    path('list/', views.report_list, name='report_list'),
    path('generate/', views.report_form, name='report_form'),  # صفحة إنشاء تقرير جديد
]
