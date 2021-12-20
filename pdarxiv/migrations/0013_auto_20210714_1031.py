# Generated by Django 3.2.3 on 2021-07-14 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdarxiv', '0012_auto_20210714_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pd',
            name='link1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='catp1', to='pdarxiv.catpens', verbose_name='Категория1 умершего'),
        ),
        migrations.AlterField(
            model_name='pd',
            name='link2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='catp2', to='pdarxiv.catpens', verbose_name='Категория2 умершего'),
        ),
        migrations.AlterField(
            model_name='pd',
            name='link3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='catp3', to='pdarxiv.catpens', verbose_name='Категория3 умершего'),
        ),
    ]