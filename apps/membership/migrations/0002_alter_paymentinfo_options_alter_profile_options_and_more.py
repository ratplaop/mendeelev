# Generated by Django 4.2.19 on 2025-02-23 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentinfo',
            options={'verbose_name': 'Информация оп платежах', 'verbose_name_plural': 'Информация оп платежах'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AddField(
            model_name='profile',
            name='education',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Образование'),
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон'),
        ),
    ]
