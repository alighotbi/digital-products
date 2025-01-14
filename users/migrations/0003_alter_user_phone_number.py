# Generated by Django 4.2 on 2025-01-01 10:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.BigIntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be in international format (e.g., +123456789).', regex='^\\+?[1-9]\\d{1,14}$')], verbose_name='mobile number'),
        ),
    ]
