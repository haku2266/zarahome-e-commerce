# Generated by Django 5.0 on 2024-01-08 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_orderitemmodel_code_orderitemmodel_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitemmodel',
            name='code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitemmodel',
            name='size',
            field=models.CharField(max_length=100),
        ),
    ]
