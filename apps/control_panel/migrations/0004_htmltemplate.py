# Generated by Django 4.2.19 on 2025-02-23 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_panel', '0003_alter_controlpanel_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='HtmlTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('content', models.TextField()),
            ],
        ),
    ]
