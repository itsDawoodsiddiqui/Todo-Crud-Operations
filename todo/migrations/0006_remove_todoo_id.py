# Generated by Django 5.0.6 on 2025-01-21 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_rename_unique_id_todoo_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todoo',
            name='id',
        ),
    ]
