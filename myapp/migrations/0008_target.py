# Generated by Django 4.2.2 on 2023-07-23 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_report_price_alter_report_total_sales'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=100)),
                ('total_targets', models.PositiveIntegerField()),
                ('account_manager', models.CharField(max_length=100)),
                ('sales_month', models.CharField(max_length=20)),
            ],
        ),
    ]
