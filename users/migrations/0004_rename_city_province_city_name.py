# Generated by Django 4.2 on 2025-01-01 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='province',
            old_name='city',
            new_name='city_name',
        ),
    ]
