# Generated by Django 5.0.6 on 2025-01-21 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_todoo_unique_id_alter_todoo_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todoo',
            old_name='unique_id',
            new_name='id',
        ),
    ]
