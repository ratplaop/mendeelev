# Generated by Django 4.2.19 on 2025-02-23 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0002_alter_paymentinfo_options_alter_profile_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='price',
            new_name='amount',
        ),
    ]
