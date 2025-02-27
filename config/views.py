# views.py
from django.shortcuts import render
from django.template import TemplateDoesNotExist
import os
from django.conf import settings

def include_view(request, template_name):
    # Путь к папке с шаблонами
    template_path = os.path.join('includes', template_name)

    # Проверка, существует ли шаблон
    try:
        return render(request, template_path)
    except TemplateDoesNotExist:
        return render(request, '404.html', status=404)  # Отображение страницы 404, если шаблон не найден