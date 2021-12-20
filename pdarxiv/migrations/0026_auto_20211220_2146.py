# Generated by Django 3.2.3 on 2021-12-20 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdarxiv', '0025_alter_pd_user_create'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pd',
            name='user_create',
        ),
        migrations.RemoveField(
            model_name='pd',
            name='user_update',
        ),
        migrations.AlterField(
            model_name='pd',
            name='date_create',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='pd',
            name='date_update',
            field=models.DateField(auto_now=True),
        ),
    ]
