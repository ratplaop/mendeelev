from calendar import Day
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe

class Actual(models.Model):
    title = models.CharField(max_length=200)  # Заголовок
    content = RichTextField()  # Основное содержание
    image = models.ImageField(upload_to='actual_images/', null=True, blank=True)  # Изображение
    date = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор записи

    class Meta:
        verbose_name = "Актуальная информация"
        verbose_name_plural = "Актуальная информация"

    def __str__(self):
        return self.title
    

    def display_my_safefield(self): 
        return mark_safe(self.my_textfield)
