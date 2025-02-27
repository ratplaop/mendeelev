from django.contrib import admin
# Register your models here.
from .models import News  # Измените на новое имя класса

admin.site.register(News)
