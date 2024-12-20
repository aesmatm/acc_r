from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from .models import Invoice
from .forms import InvoiceForm, InvoiceItemFormSet
from company.models import CompanyInfo

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-invoice_date')
    total_amount = invoices.aggregate(total=Sum('total_amount'))['total'] or 0
    
    context = {
        'invoices': invoices,
        'total_amount': total_amount,
    }
    return render(request, 'invoices/invoice_list.html', context)

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    company = CompanyInfo.objects.first()
    context = {
        'invoice': invoice,
        'company': company,
    }
    return render(request, 'invoices/invoice_detail.html', context)

@login_required
def invoice_print(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    context = {
        'invoice': invoice,
        'company_address': 'عنوان الشركة هنا',
        'company_phone': 'رقم الهاتف هنا',
        'company_email': 'البريد الإلكتروني هنا',
    }
    return render(request, 'invoices/invoice_print.html', context)

@login_required
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            
            formset = InvoiceItemFormSet(request.POST, instance=invoice)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'تم إنشاء الفاتورة بنجاح')
                return redirect('invoices:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'إنشاء فاتورة جديدة'
    }
    return render(request, 'invoices/invoice_form.html', context)

@login_required
def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save()
            
            formset = InvoiceItemFormSet(request.POST, instance=invoice)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'تم تحديث الفاتورة بنجاح')
                return redirect('invoices:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice)
    
    context = {
        'form': form,
        'formset': formset,
        'invoice': invoice,
        'title': 'تعديل الفاتورة'
    }
    return render(request, 'invoices/invoice_form.html', context)
