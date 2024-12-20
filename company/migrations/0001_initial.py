# Generated by Django 4.2 on 2024-12-20 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='اسم الشركة')),
                ('address', models.TextField(verbose_name='العنوان')),
                ('phone', models.CharField(max_length=50, verbose_name='رقم الهاتف')),
                ('mobile', models.CharField(blank=True, max_length=50, null=True, verbose_name='رقم الجوال')),
                ('email', models.EmailField(max_length=254, verbose_name='البريد الإلكتروني')),
                ('website', models.URLField(blank=True, null=True, verbose_name='الموقع الإلكتروني')),
                ('tax_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='الرقم الضريبي')),
                ('commercial_record', models.CharField(blank=True, max_length=50, null=True, verbose_name='السجل التجاري')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company/', verbose_name='شعار الشركة')),
            ],
            options={
                'verbose_name': 'معلومات الشركة',
                'verbose_name_plural': 'معلومات الشركة',
            },
        ),
    ]
