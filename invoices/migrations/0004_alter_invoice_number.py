# Generated by Django 4.2 on 2024-12-20 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_invoiceitem_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='number',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='رقم الفاتورة'),
        ),
    ]
