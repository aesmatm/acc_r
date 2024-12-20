from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Invoice, Supplier

# Create your views here.

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    for supplier in suppliers:
        supplier.total_invoices = supplier.invoices.count()
        supplier.total_amount = supplier.invoices.aggregate(total=Sum('total_amount'))['total'] or 0
    
    context = {
        'suppliers': suppliers,
    }
    return render(request, 'suppliers/supplier_list.html', context)

@login_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    total_amount = supplier.invoices.aggregate(total=Sum('total_amount'))['total'] or 0
    
    context = {
        'supplier': supplier,
        'total_amount': total_amount,
    }
    return render(request, 'suppliers/supplier_detail.html', context)

@login_required
def supplier_invoices(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    invoices = supplier.invoices.all().order_by('-invoice_date')
    total_amount = invoices.aggregate(total=Sum('total_amount'))['total'] or 0
    
    context = {
        'supplier': supplier,
        'invoices': invoices,
        'total_amount': total_amount,
    }
    return render(request, 'suppliers/supplier_invoices.html', context)

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    context = {
        'invoice': invoice,
        'company_address': 'عنوان الشركة هنا',
        'company_phone': 'رقم الهاتف هنا',
        'company_email': 'البريد الإلكتروني هنا',
    }
    return render(request, 'suppliers/invoice_detail.html', context)

@login_required
def invoice_print(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    context = {
        'invoice': invoice,
        'company_address': 'عنوان الشركة هنا',
        'company_phone': 'رقم الهاتف هنا',
        'company_email': 'البريد الإلكتروني هنا',
    }
    return render(request, 'suppliers/invoice_print.html', context)
