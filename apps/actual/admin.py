from django.contrib import admin
# Register your models here.
from .models import Actual  # Измените на новое имя класса

class ActualAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Укажите, какие поля отображать в списке
    search_fields = ('title',)  # Поиск по заголовку

admin.site.register(Actual, ActualAdmin)
