import os

# Параметры вашего проекта
project_name = 'apps/library2'  # Замените на имя вашего проекта
app_name = 'library2'

# Создание приложения
os.system(f'python manage.py startapp {app_name}')

# Создание моделей
models_code = """
from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    access_level = models.CharField(max_length=50)  # Например, 'basic', 'premium'

    def __str__(self):
        return f"{self.user.username} - {self.access_level}"
"""

with open(f'{app_name}/models.py', 'w') as f:
    f.write(models_code)

# Создание представлений
views_code = """
from django.shortcuts import render, get_object_or_404
from .models import Category, Book
from django.http import HttpResponse

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'library/category_list.html', {'categories': categories})

def book_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(category=category)
    return render(request, 'library/book_list.html', {'category': category, 'books': books})

def download_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    response = HttpResponse(book.file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
    return response
"""

with open(f'{app_name}/views.py', 'w') as f:
    f.write(views_code)

# Создание URL-ов
urls_code = """
from django.urls import path
from .views import category_list, book_list, download_book

urlpatterns = [
    path('categories/', category_list, name='category_list'),
    path('categories/<int:category_id>/', book_list, name='book_list'),
    path('download/<int:book_id>/', download_book, name='download_book'),
]
"""

with open(f'{app_name}/urls.py', 'w') as f:
    f.write(urls_code)

# Создание шаблонов
os.makedirs(f'{app_name}/templates/library', exist_ok=True)

category_list_template = """
{% extends 'base.html' %}

{% block content %}
<h1>Категории</h1>
<ul>
    {% for category in categories %}
        <li><a href="{% url 'book_list' category.id %}">{{ category.name }}</a></li>
    {% empty %}
        <li>Нет доступных категорий.</li>
    {% endfor %}
</ul>
{% endblock %}
"""

with open(f'{app_name}/templates/library/category_list.html', 'w') as f:
    f.write(category_list_template)

book_list_template = """
{% extends 'base.html' %}

{% block content %}
<h1>{{ category.name }}</h1>
<ul>
    {% for book in books %}
        <li>
            {{ book.title }} by {{ book.author }} - 
            <a href="{% url 'download_book' book.id %}">Скачать</a>
        </li>
    {% empty %}
        <li>Нет доступных книг в этой категории.</li>
    {% endfor %}
</ul>
{% endblock %}
"""

with open(f'{app_name}/templates/library/book_list.html', 'w') as f:
    f.write(book_list_template)

# Создание админского интерфейса
admin_code = """
from django.contrib import admin
from .models import Category, Book, Subscription

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Subscription)
"""

with open(f'{app_name}/admin.py', 'w') as f:
    f.write(admin_code)

# Обновление главного urls.py
main_urls_path = os.path.join(project_name, 'urls.py')
with open(main_urls_path, 'r') as f:
    main_urls = f.readlines()

main_urls.append(f"\npath('library/', include('{app_name}.urls')),\n")

with open(main_urls_path, 'w') as f:
    f.writelines(main_urls)

print(f"Приложение '{app_name}' успешно создано!")