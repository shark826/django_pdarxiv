# Generated by Django 3.2.3 on 2021-05-19 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdarxiv', '0004_alter_pd_nom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pd',
            name='drr',
            field=models.DateField(blank=True, null=True, verbose_name='Дата ревизии'),
        ),
        migrations.AlterField(
            model_name='pd',
            name='ds',
            field=models.DateField(blank=True, null=True, verbose_name='Дата смерти'),
        ),
        migrations.AlterField(
            model_name='pd',
            name='fname',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Отчество'),
        ),
    ]