# Generated by Django 4.2.11 on 2024-04-30 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('line_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('user_icon', models.CharField(blank=True, max_length=100, null=True)),
                ('invitation', models.BooleanField(default=False)),
                ('request', models.BooleanField(default=False)),
                ('have_list', models.BooleanField(default=False)),
                ('default_list', models.BooleanField(default=True)),
                ('remind', models.BooleanField(default=True)),
                ('remind_timing', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True)),
                ('remind_time', models.TimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('list_id', models.AutoField(primary_key=True, serialize=False)),
                ('list_name', models.CharField(max_length=50)),
                ('shopping_cycle', models.IntegerField(choices=[(0, '毎月'), (1, '隔週'), (2, '毎週')], default=0)),
                ('shopping_day', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30)], null=True)),
                ('day_of_week', models.IntegerField(blank=True, choices=[(0, '月'), (1, '火'), (2, '水'), (3, '木'), (4, '金'), (5, '土'), (6, '日')], null=True)),
                ('owner_id', models.ForeignKey(db_column='owner_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'lists',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('member_id', models.AutoField(primary_key=True, serialize=False)),
                ('authority', models.BooleanField(default=False)),
                ('invitee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shared_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.list')),
            ],
            options={
                'db_table': 'members',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=50)),
                ('color', models.IntegerField(blank=True, choices=[(0, '赤'), (1, '青'), (2, '緑')], null=True)),
                ('consume_cycle', models.IntegerField(default=30)),
                ('last_purchase_at', models.DateField(blank=True, null=True)),
                ('last_open_at', models.DateField(blank=True, null=True)),
                ('link', models.CharField(blank=True, max_length=255, null=True)),
                ('to_list', models.BooleanField(blank=True, default=False, null=True)),
                ('remind_by_item', models.BooleanField(default=True)),
                ('manage_target', models.BooleanField(default=True)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.list')),
            ],
            options={
                'db_table': 'items',
            },
        ),
    ]
