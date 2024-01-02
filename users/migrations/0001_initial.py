# Generated by Django 5.0 on 2024-01-02 14:16

import django.contrib.auth.password_validation
import django.db.models.deletion
import django.utils.timezone
import users.models
import users.validators
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUserModel',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email already exists'}, help_text='Required. Your gmail address.', max_length=254, unique=True, validators=[users.validators.validate_email], verbose_name='email address')),
                ('phone_number', models.CharField(blank=True, error_messages={'invalid': 'Please enter a valid phone', 'unique': 'A user with that phone number already exists'}, help_text='Enter phone number e.g: +998123456789', max_length=15, null=True, unique=True, validators=[users.validators.PhoneValidator()], verbose_name='phone number')),
                ('site_ranking', models.PositiveSmallIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('password', models.CharField(max_length=100, validators=[django.contrib.auth.password_validation.validate_password])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'users',
            },
            managers=[
                ('objects', users.models.BaseUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ClientDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='your first name', max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(help_text='your last name', max_length=100, verbose_name='last name')),
                ('region', models.CharField(help_text='region', max_length=100, verbose_name='region')),
                ('city', models.CharField(help_text='city', max_length=100, verbose_name='city')),
                ('street', models.TextField(help_text='street', verbose_name='street')),
                ('flat_number', models.IntegerField(blank=True, help_text='flat number', null=True, verbose_name='flat number')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_details', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'client detail',
                'verbose_name_plural': 'client details',
                'db_table': 'client_details',
            },
        ),
    ]