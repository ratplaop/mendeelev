from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Main(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Региональные Новости'
        verbose_name_plural = 'Региональные Новости'

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    author = models.CharField(max_length=100, default="Неизвестный автор")
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='Изображение')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.SlugField(unique=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_date']

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    date = models.DateTimeField(verbose_name='Дата проведения')
    image = models.ImageField(upload_to='events/', verbose_name='Изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['date']

    def __str__(self):
        return self.title

class MainNews(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
