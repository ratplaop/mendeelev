
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='books/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Цена за доступ
    date_added = models.DateTimeField(default=timezone.now)  # Дата добавления книги

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    access_level = models.CharField(max_length=50)  # Например, 'basic', 'premium'

    def __str__(self):
        return f"{self.user.username} - {self.access_level}"
