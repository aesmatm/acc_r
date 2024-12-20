from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum, Count
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from inventory.models import Item
from invoices.models import Invoice
from suppliers.models import Supplier
from projects.models import Project
from finance.models import Transaction
from .models import Report
from django.db import models
import os
from django.conf import settings
import base64

def get_report_data(report_type, date_from=None, date_to=None):
    """استرجاع بيانات التقرير حسب نوعه"""
    if report_type == 'inventory':
        items = Item.objects.all()
        headers = ['#', 'اسم الصنف', 'الكمية', 'سعر الوحدة', 'القيمة الإجمالية']
        data = [
            [str(i+1), item.name, str(item.current_stock), str(item.price), str(item.current_stock * item.price)]
            for i, item in enumerate(items)
        ]
        total_value = sum(item.current_stock * item.price for item in items)
        summary = [
            f'إجمالي عدد الأصناف: {items.count()}',
            f'إجمالي قيمة المخزون: {total_value} ج.م'
        ]
        title = 'تقرير المخزون'
        
    elif report_type == 'invoices':
        invoices = Invoice.objects.filter(date__range=[date_from, date_to])
        headers = ['#', 'رقم الفاتورة', 'التاريخ', 'المورد', 'المبلغ قبل الضريبة', 'الضريبة', 'الإجمالي']
        data = [
            [str(i+1), invoice.number, invoice.date.strftime('%Y-%m-%d'), 
             invoice.supplier.name, str(invoice.total_amount), 
             str(invoice.tax_amount), str(invoice.total_with_tax)]
            for i, invoice in enumerate(invoices)
        ]
        total_amount = sum(invoice.total_with_tax for invoice in invoices)
        summary = [
            f'إجمالي عدد الفواتير: {invoices.count()}',
            f'إجمالي المبلغ: {total_amount} ج.م'
        ]
        title = 'تقرير الفواتير'
        
    elif report_type == 'suppliers':
        suppliers = Supplier.objects.all()
        headers = ['#', 'اسم المورد', 'رمز المورد', 'الرقم الضريبي', 'العنوان']
        data = [
            [str(i+1), supplier.name, supplier.code, supplier.tax_number or '-', supplier.address or '-']
            for i, supplier in enumerate(suppliers)
        ]
        summary = [
            f'إجمالي عدد الموردين: {suppliers.count()}'
        ]
        title = 'تقرير الموردين'
        
    elif report_type == 'projects':
        projects = Project.objects.filter(start_date__range=[date_from, date_to])
        headers = ['#', 'اسم المشروع', 'تاريخ البدء', 'تاريخ الانتهاء', 'المبلغ']
        data = [
            [str(i+1), project.name, project.start_date.strftime('%Y-%m-%d'), project.end_date.strftime('%Y-%m-%d'), str(project.amount)]
            for i, project in enumerate(projects)
        ]
        summary = [
            f'إجمالي عدد المشاريع: {projects.count()}'
        ]
        title = 'تقرير المشاريع'
        
    elif report_type in ['finance', 'financial']:
        transactions = Transaction.objects.filter(date__range=[date_from, date_to])
        headers = ['#', 'نوع المعاملة', 'التاريخ', 'رقم المرجع', 'المشروع', 'مدين', 'دائن']
        data = []
        total_debit = 0
        total_credit = 0
        
        for i, transaction in enumerate(transactions):
            debit_sum = transaction.lines.aggregate(total=models.Sum('debit'))['total'] or 0
            credit_sum = transaction.lines.aggregate(total=models.Sum('credit'))['total'] or 0
            total_debit += debit_sum
            total_credit += credit_sum
            
            data.append([
                str(i+1),
                transaction.get_type_display(),
                transaction.date.strftime('%Y-%m-%d'),
                transaction.reference_number,
                transaction.project.name,
                str(debit_sum),
                str(credit_sum)
            ])
        
        summary = [
            f'إجمالي عدد المعاملات: {transactions.count()}',
            f'إجمالي المدين: {total_debit} ج.م',
            f'إجمالي الدائن: {total_credit} ج.م',
            f'الرصيد: {total_debit - total_credit} ج.م'
        ]
        title = 'التقرير المالي'
    else:
        raise ValueError(f'نوع التقرير غير معروف: {report_type}')
    
    return {
        'title': title,
        'headers': headers,
        'data': data,
        'summary': summary
    }

def create_pdf_report(response, title, headers, data, summary):
    # إنشاء مستند PDF
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    # تحضير العناصر
    elements = []
    
    # إضافة العنوان
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        alignment=1,  # وسط
        fontSize=24,
        spaceAfter=30
    )
    elements.append(Paragraph(title, title_style))
    
    # إضافة الجدول
    table_data = [headers] + data
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    
    # إضافة الملخص
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=30
    )
    for line in summary:
        elements.append(Paragraph(line, summary_style))
    
    # بناء المستند
    doc.build(elements)

@login_required
def report_form(request):
    """عرض نموذج إنشاء تقرير جديد"""
    return render(request, 'reports/report_form.html')

@login_required
def generate_report(request, report_type):
    """إنشاء تقرير جديد أو عرض تقرير موجود"""
    # التحقق من وجود معرف التقرير في الطلب
    report_id = request.GET.get('id')
    if report_id:
        report = get_object_or_404(Report, id=report_id)
        return view_report(request, report_type, report)
    
    if request.method != 'POST':
        return render(request, 'reports/report_form.html', {
            'report_type': report_type,
        })
    
    # إنشاء تقرير جديد
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    
    report_data = get_report_data(report_type, date_from, date_to)
    
    report = Report.objects.create(
        title=report_data['title'],
        report_type=report_type,
        date_from=date_from,
        date_to=date_to,
        created_by=request.user
    )
    
    return view_report(request, report_type, report)

@login_required
def view_report(request, report_type, report=None):
    if not report:
        report_id = request.GET.get('id')
        report = get_object_or_404(Report, id=report_id)
    
    report_data = get_report_data(report_type, report.date_from, report.date_to)
    context = {
        'report': report,
        'title': report_data['title'],
        'headers': report_data['headers'],
        'data': report_data['data'],
        'summary': report_data['summary']
    }
    
    return render(request, 'reports/view_report.html', context)

@login_required
def print_report(request, report_type):
    """عرض التقرير للطباعة"""
    report_id = request.GET.get('id')
    if not report_id:
        raise Http404("لم يتم تحديد التقرير")
    
    report = get_object_or_404(Report, id=report_id)
    report_data = get_report_data(report.report_type, report.date_from, report.date_to)
    
    # إضافة مسار الشعار
    logo_path = os.path.join(settings.STATIC_ROOT, 'images', 'logo.png')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_data = base64.b64encode(f.read()).decode('utf-8')
            logo_url = f'data:image/png;base64,{logo_data}'
    else:
        logo_url = ''
    
    context = {
        'title': report_data['title'],
        'headers': report_data['headers'],
        'data': report_data['data'],
        'summary': report_data['summary'],
        'report': report,
        'logo_url': logo_url,
    }
    
    return render(request, 'reports/print_report.html', context)

@login_required
def export_pdf(request, report_type):
    report_id = request.GET.get('id')
    report = get_object_or_404(Report, id=report_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    report_data = get_report_data(report_type, report.date_from, report.date_to)
    create_pdf_report(
        response,
        report_data['title'],
        report_data['headers'],
        report_data['data'],
        report_data['summary']
    )
    
    return response

@login_required
def report_list(request):
    reports = Report.objects.filter(created_by=request.user)
    return render(request, 'reports/report_list.html', {
        'reports': reports,
    })
