# Generated by Django 4.2.11 on 2024-05-01 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='owner_id',
            new_name='owner',
        ),
    ]
