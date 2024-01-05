# Generated by Django 5.0 on 2024-01-05 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_typemodel_name_alter_typemodel_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='short_description',
            field=models.CharField(blank=True, help_text='short description of category', max_length=100, verbose_name='short description'),
        ),
    ]