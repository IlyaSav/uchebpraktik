# Generated by Django 5.1.1 on 2025-05-06 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='price',
        ),
        migrations.AddField(
            model_name='service',
            name='price_max',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Максимальная цена'),
        ),
        migrations.AddField(
            model_name='service',
            name='price_min',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Минимальная цена'),
        ),
    ]
