# Generated by Django 4.2 on 2024-12-20 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='اسم القالب')),
                ('report_type', models.CharField(choices=[('financial', 'تقرير مالي'), ('inventory', 'تقرير المخزون'), ('projects', 'تقرير المشاريع'), ('invoices', 'تقرير الفواتير'), ('suppliers', 'تقرير الموردين')], max_length=20, verbose_name='نوع التقرير')),
                ('template_file', models.FileField(upload_to='report_templates/', verbose_name='ملف القالب')),
                ('description', models.TextField(blank=True, verbose_name='وصف القالب')),
                ('is_active', models.BooleanField(default=True, verbose_name='نشط')),
            ],
            options={
                'verbose_name': 'قالب تقرير',
                'verbose_name_plural': 'قوالب التقارير',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان التقرير')),
                ('report_type', models.CharField(choices=[('financial', 'تقرير مالي'), ('inventory', 'تقرير المخزون'), ('projects', 'تقرير المشاريع'), ('invoices', 'تقرير الفواتير'), ('suppliers', 'تقرير الموردين')], max_length=20, verbose_name='نوع التقرير')),
                ('date_from', models.DateField(verbose_name='من تاريخ')),
                ('date_to', models.DateField(verbose_name='إلى تاريخ')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاريخ الإنشاء')),
                ('notes', models.TextField(blank=True, verbose_name='ملاحظات')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='تم الإنشاء بواسطة')),
            ],
            options={
                'verbose_name': 'تقرير',
                'verbose_name_plural': 'التقارير',
                'ordering': ['-created_at'],
            },
        ),
    ]
