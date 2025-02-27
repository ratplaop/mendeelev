from django.contrib import admin
# Register your models here.
from .models import Main, Event, News  # Измените на новое имя класса, импортируйте новые модели

admin.site.register(Main)
admin.site.register(Event)  # Регистрация модели Event
admin.site.register(News)   # Регистрация модели News
