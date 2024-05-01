# Generated by Django 4.2.11 on 2024-05-01 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_rename_owner_id_list_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='invitee',
            new_name='invitee_id',
        ),
        migrations.RemoveField(
            model_name='list',
            name='owner',
        ),
        migrations.AddField(
            model_name='list',
            name='owner_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
