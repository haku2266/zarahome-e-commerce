# Generated by Django 5.0 on 2024-01-02 14:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        ('shop', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.clientdetails', verbose_name='client'),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='items',
            field=models.ManyToManyField(help_text='Items related to the order', related_name='orders', to='shop.cartitemmodel', verbose_name='items'),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='promo_code',
            field=models.ForeignKey(blank=True, help_text='promo code that would give discount for an order', null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.promocodemodel', verbose_name='promo code'),
        ),
    ]
