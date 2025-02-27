from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
from ckeditor.fields import RichTextField
from tinymce.models import HTMLField  # Импортируйте HTMLField из tinymce

class ControlPanel(models.Model):
    name = models.CharField(max_length=100)  # Название приложения
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    description = models.TextField(blank=True, null=True)  # Описание приложения

    class Meta:
        verbose_name = "Панель управления"
        verbose_name_plural = "Панель управления"

    def __str__(self):
        return self.name

class HtmlTemplate(models.Model):
    name = models.CharField(max_length=200, unique=True)  # Имя шаблона
    content = HTMLField()  # Используем HTMLField от TinyMCE
    template_name = models.CharField(max_length=200, default='base_template')  # Имя базового шаблона с значением по умолчанию

    def save(self, *args, **kwargs):
        # Сначала сохраняем объект в базе данных
        super().save(*args, **kwargs)

        # Затем сохраняем содержимое в файл, используя базовый шаблон
        file_path = os.path.join(settings.BASE_DIR, 'templates', 'includes', f'{self.name}.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.get_full_template())

    def get_full_template(self):
        # Возвращаем полный HTML, включая базовый шаблон
        return f"""<!doctype html>
        <html lang="ru">
        <head>
        {{% include 'main/header.html' %}}
            <title>{self.name}</title>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <link rel="stylesheet" type="text/css" href="/static/main/css/style.css">
        </head>
        <body>
            <div class="container">
                {self.content}  <!-- Вставляем контент -->
            </div>
            {{% include 'main/events.html' %}}
            {{% include 'main/footer.html' %}}

                    <style>
                .container {{
    width: 90%; /* Ширина контейнера 90% */
    margin: 20px auto; /* Центрирование контейнера с отступами сверху и снизу */
    padding: 20px; /* Внутренние отступы */
    background-color: #f9f9f9; /* Цвет фона */
    border-radius: 8px; /* Закругленные углы */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Тень для эффекта глубины */
    transition: transform 0.3s ease, box-shadow 0.3s ease; /* Анимация при наведении */
}}

.container:hover {{
    transform: translateY(-5px); /* Подъем контейнера при наведении */
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Увеличение тени при наведении */
                }}
            </style>
        </body>
        </html>"""
    
    def __str__(self):
        return self.name
