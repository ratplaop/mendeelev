# Generated by Django 4.2.19 on 2025-02-18 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0002_rename_name_regionsmodel_region_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RegionsModel',
            new_name='Regions',
        ),
    ]
