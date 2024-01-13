# Generated by Django 5.0 on 2024-01-12 13:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_ordermodel_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='discount',
            field=models.PositiveIntegerField(blank=True, help_text='discount issued by the promo code', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='discount'),
        ),
    ]