# Generated by Django 3.2.3 on 2021-11-02 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdarxiv', '0018_vocnsp_voculc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pd',
            name='gor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pdarxiv.vocnsp', verbose_name='Населенный пункт'),
        ),
    ]
