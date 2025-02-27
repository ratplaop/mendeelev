from django.contrib import admin
# Register your models here.
from .models import Events  # Измените на новое имя класса

admin.site.register(Events)
