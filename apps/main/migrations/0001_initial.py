# Generated by Django 4.2.19 on 2025-02-19 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('date', models.DateTimeField(verbose_name='Дата проведения')),
                ('image', models.ImageField(upload_to='events/', verbose_name='Изображение')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно')),
            ],
            options={
                'verbose_name': 'Мероприятие',
                'verbose_name_plural': 'Мероприятия',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MainNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='news_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('author', models.CharField(default='Неизвестный автор', max_length=100)),
                ('content', models.TextField(verbose_name='Содержание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='news/', verbose_name='Изображение')),
                ('published_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('slug', models.SlugField(unique=True)),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['-published_date'],
            },
        ),
    ]
