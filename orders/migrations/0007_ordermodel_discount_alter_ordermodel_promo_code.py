# Generated by Django 5.0 on 2024-01-12 12:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_promocodemodel_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='discount',
            field=models.PositiveSmallIntegerField(blank=True, default=0, help_text='discount issued by the promo code', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='discount'),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='promo_code',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='promo code'),
        ),
    ]
