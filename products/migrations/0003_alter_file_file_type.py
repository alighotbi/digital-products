# Generated by Django 4.2 on 2024-12-24 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_file_file_type_alter_file_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_type',
            field=models.SmallIntegerField(choices=[(1, 'audio'), ('video', 'video'), (3, 'pdf')], verbose_name='file_type'),
        ),
    ]
