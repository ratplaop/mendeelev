from django.contrib import admin
# Register your models here.
from .models import Regions  # Измените на новое имя класса

admin.site.register(Regions)
