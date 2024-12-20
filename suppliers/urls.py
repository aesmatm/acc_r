from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    # Supplier URLs
    path('', views.supplier_list, name='supplier_list'),
    path('<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('<int:pk>/invoices/', views.supplier_invoices, name='supplier_invoices'),
    
    # Invoice URLs
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:pk>/print/', views.invoice_print, name='invoice_print'),
]
