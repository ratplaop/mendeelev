from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
import os
from django.conf import settings
from .models import ControlPanel, HtmlTemplate
from .forms import ControlPanelForm
from django.shortcuts import render, redirect, get_object_or_404
import subprocess
import shutil
import importlib
import sys
from django.db import models
import datetime
from .models import HtmlTemplate

class ControlPanelView(UserPassesTestMixin, ListView):
    model = ControlPanel
    template_name = 'control_panel/index.html'
    context_object_name = 'objects'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apps'] = self.get_installed_apps()
        context['templates'] = self.get_templates()
        return context
    
    def get_installed_apps(self):
        return [app for app in settings.INSTALLED_APPS if app.startswith('apps.')]
    
    def get_templates(self):
        template_dir = settings.TEMPLATES[0]['DIRS'][0]
        templates = []
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file.endswith('.html'):
                    templates.append(os.path.join(root, file))
        return templates
    
    def get_queryset(self):
        return ControlPanel.objects.all()

class IndexView(ListView):
    model = ControlPanel
    template_name = 'control_panel/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return ControlPanel.objects.all()

def control_panel_list(request):
    panels = ControlPanel.objects.all()
    return render(request, 'control_panel/control_panel_list.html', {'panels': panels})

def control_panel_create(request):
    if request.method == 'POST':
        form = ControlPanelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('control_panel:control_panel_list')
    else:
        form = ControlPanelForm()
    return render(request, 'control_panel/control_panel_form.html', {'form': form})

def control_panel_edit(request, panel_id):
    panel = get_object_or_404(ControlPanel, id=panel_id)
    if request.method == 'POST':
        form = ControlPanelForm(request.POST, instance=panel)
        if form.is_valid():
            form.save()
            return redirect('control_panel:control_panel_list')
    else:
        form = ControlPanelForm(instance=panel)
    return render(request, 'control_panel/control_panel_form.html', {'form': form})

def dashboard(request):
    return render(request, 'control_panel/dashboard.html')

def create_app(request):
    message = ""
    if request.method == "POST":
        app_name = request.POST.get("app_name")
        app_directory = request.POST.get("app_directory", "apps")
        add_to_installed_apps = request.POST.get("add_to_installed_apps") is not None

        if app_name:
            try:
                # Создаем приложение в указанной директории
                subprocess.check_call(["python", "manage.py", "startapp", app_name, os.path.join(settings.BASE_DIR, app_directory)])
                message = f"Приложение '{app_name}' успешно создано в '{app_directory}'."

                # Если нужно, добавляем приложение в INSTALLED_APPS
                if add_to_installed_apps:
                    settings_path = os.path.join(settings.BASE_DIR, "myproject", "settings.py")
                    with open(settings_path, 'a') as f:
                        f.write(f"\nINSTALLED_APPS.append('{app_name}')\n")
                    message += f" Приложение '{app_name}' добавлено в INSTALLED_APPS."
            except subprocess.CalledProcessError as e:
                message = f"Ошибка при создании приложения: {e}"
    return render(request, 'control_panel/create_app.html', {"message": message})

def check_routes(request):
    errors = []
    recommendations = []

    # Проходим по всем приложениям, указанным в INSTALLED_APPS, исключая системные (django.*)
    for app in settings.INSTALLED_APPS:
        if app.startswith("django."):
            continue
        try:
            module = importlib.import_module(app)
            app_path = os.path.dirname(module.__file__)
        except Exception as e:
            errors.append(f"Не удалось импортировать приложение '{app}': {e}")
            continue

        # Проверка наличия urls.py
        urls_file = os.path.join(app_path, "urls.py")
        if not os.path.exists(urls_file):
            errors.append(f"Приложении '{app}' отсутствует файл urls.py.")
            recommendations.append(
                f"Создайте файл '{urls_file}' и определите необходимые маршруты для приложения '{app}'.")
        else:
            with open(urls_file, 'r') as f:
                urls_lines = f.readlines()
            # Проверка наличия маршрутов
            if not any("path(" in line for line in urls_lines):
                errors.append(f"В файле '{urls_file}' отсутствуют маршруты.")
                recommendations.append(f"Добавьте маршруты в файл '{urls_file}'.")

        # Проверка наличия views.py
        views_file = os.path.join(app_path, "views.py")
        if not os.path.exists(views_file):
            errors.append(f"Приложении '{app}' отсутствует файл views.py.")
            recommendations.append(f"Создайте файл '{views_file}' с функциями обработки маршрутов для '{app}'.")

        # Проверка наличия models.py
        models_file = os.path.join(app_path, "models.py")
        if not os.path.exists(models_file):
            errors.append(f"Приложении '{app}' отсутствует файл models.py.")
            recommendations.append(f"Создайте файл '{models_file}' для определения моделей приложения '{app}'.")

        # Проверка наличия шаблонов
        template_dir = os.path.join(settings.BASE_DIR, "templates", app)
        if not os.path.exists(template_dir):
            errors.append(f"Отсутствует каталог шаблонов для приложения '{app}' (ожидался путь: '{template_dir}').")
            recommendations.append(f"Создайте каталог '{template_dir}' и поместите туда шаблоны приложения '{app}'.")

    result = "Проверка маршрутов завершена.\n\n"
    if errors:
        result += "Обнаружены следующие проблемы:\n" + "\n".join(errors) + "\n\n"
    if recommendations:
        result += "Рекомендации по исправлению:\n" + "\n".join(recommendations)
    if not errors and not recommendations:
        result += "Все маршруты и файлы находятся на своих местах."

    return render(request, "control_panel/check_routes.html", {"content": result})

def create_template(request):
    message = ""
    if request.method == "POST":
        template_name = request.POST.get("template_name")
        content = request.POST.get("content", "")
        if template_name:
            dir_path = os.path.join(settings.BASE_DIR, "templates")
            os.makedirs(dir_path, exist_ok=True)
            file_path = os.path.join(dir_path, template_name)
            try:
                with open(file_path, "w") as f:
                    f.write(content)
                message = f"Шаблон '{template_name}' создан успешно."
            except Exception as e:
                message = f"Ошибка создания шаблона: {e}"
    return render(request, 'control_panel/create_template.html', {"message": message})

def check_structure(request):
    structure = []

    def build_tree(path, prefix="", depth=0):
        if depth > 5:  # Ограничиваем глубину до 5
            return
        items = os.listdir(path)
        for i, item in enumerate(items):
            item_path = os.path.join(path, item)
            is_last = i == len(items) - 1
            if item == 'venv':  # Игнорируем папку venv
                continue
            if os.path.isdir(item_path):
                structure.append(f"{prefix}{item}/")  # Добавляем папку
                build_tree(item_path, prefix + item + " > ", depth + 1)  # Увеличиваем глубину
            else:
                structure.append(f"{prefix}{item}")  # Добавляем файл

    build_tree(settings.BASE_DIR)
    return render(request, 'control_panel/check_structure.html', {"structure": structure})

def run_checks(request):
    message = ""
    try:
        output = subprocess.check_output([sys.executable, "manage.py", "check"], universal_newlines=True)
        message = output if output.strip() else "Проверки пройдены успешно."
    except subprocess.CalledProcessError as e:
        message = f"Ошибка при запуске проверок: {e.output}"
    return render(request, 'control_panel/run_checks.html', {"message": message})

def check_settings(request):
    try:
        output = subprocess.check_output([sys.executable, "manage.py", "diffsettings"], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        output = f"Ошибка при проверке настроек: {e.output}"
    return render(request, 'control_panel/check_settings.html', {"output": output})

def configure_new_app(request):
    message = ""
    if request.method == "POST":
        new_app_name = request.POST.get("new_app_name", "").strip()
        if not new_app_name:
            message = "Имя приложения не может быть пустым."
        else:
            project_root = settings.BASE_DIR
            settings_path = os.path.join(project_root, "myproject", "settings.py")
            urls_path = os.path.join(project_root, "myproject", "urls.py")

            # 1. Редактируем settings.py для добавления приложения в INSTALLED_APPS.
            try:
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings_content = f.read()
                if new_app_name in settings_content:
                    message += f"Приложение '{new_app_name}' уже присутствует в INSTALLED_APPS.\n"
                else:
                    marker = "INSTALLED_APPS = ["
                    pos = settings_content.find(marker)
                    if pos == -1:
                        message += "Не удалось найти переменную INSTALLED_APPS в settings.py.\n"
                    else:
                        pos_end = settings_content.find("]", pos)
                        new_line = f"    '{new_app_name}',\n"
                        settings_content = settings_content[:pos_end] + new_line + settings_content[pos_end:]
                        with open(settings_path, 'w', encoding='utf-8') as f:
                            f.write(settings_content)
                        message += f"Приложение '{new_app_name}' успешно добавлено в INSTALLED_APPS.\n"
            except Exception as e:
                message += f"Ошибка при редактировании settings.py: {e}\n"

            # 2. Редактируем urls.py для добавления маршрута к новому приложению.
            try:
                with open(urls_path, 'r', encoding='utf-8') as f:
                    urls_lines = f.readlines()
                new_route = f"    path('{new_app_name}/', include('{new_app_name}.urls')),\n"
                inserted = False
                for i, line in enumerate(urls_lines):
                    if line.strip().startswith("urlpatterns") and line.strip().endswith("["):
                        j = i + 1
                        while j < len(urls_lines):
                            if urls_lines[j].strip().startswith("]"):
                                urls_lines.insert(j, new_route)
                                inserted = True
                                message += f"Маршрут для приложения '{new_app_name}' успешно добавлен.\n"
                                break
                            j += 1
                        break
                if inserted:
                    with open(urls_path, 'w', encoding='utf-8') as f:
                        f.write("".join(urls_lines))
                else:
                    message += "Не удалось добавить маршрут в urls.py.\n"
            except Exception as e:
                message += f"Ошибка при редактировании urls.py: {e}\n"
    return render(request, "control_panel/configure_new_app.html", {"message": message})

def analyze_models(request):
    model_info = []
    selected_apps = request.POST.getlist('selected_apps') if request.method == "POST" else []
    app_path = request.POST.get("app_path", "").strip()  # Получаем путь к приложению

    # Устанавливаем корневую директорию проекта
    project_root = settings.BASE_DIR

    if app_path:
        # Проверяем, существует ли указанный путь
        full_app_path = os.path.join(project_root, app_path)
        if not os.path.exists(full_app_path):
            return render(request, 'control_panel/analyze_models.html', {"error": "Указанный путь не существует."})

        # Получаем список моделей из указанного приложения
        try:
            module = importlib.import_module(app_path.replace('/', '.').replace('\\', '.'))  # Импортируем модуль
            app_models = [
                {
                    "name": model.__name__,
                    "fields": [
                        (field.name, field.get_internal_type())
                        for field in model._meta.get_fields()
                    ]
                }
                for model in module.__dict__.values()
                if isinstance(model, type) and issubclass(model, models.Model)
            ]
            model_info.append({"app": app_path, "models": app_models})
        except Exception as e:
            return render(request, 'control_panel/analyze_models.html', {"error": str(e)})

    return render(request, 'control_panel/analyze_models.html', {'model_info': model_info, 'selected_apps': selected_apps})

def create_backup(request):
    message = ""
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    os.makedirs(backup_dir, exist_ok=True)

    # Получаем список существующих резервных копий
    existing_backups = [f for f in os.listdir(backup_dir) if f.endswith('.zip')]

    if request.method == "POST":
        backup_name = request.POST.get("backup_name", "").strip()
        if not backup_name:
            message = "Имя резервной копии не может быть пустым."
        else:
            # Создаем имя файла резервной копии
            backup_file = os.path.join(backup_dir, f"{backup_name}.zip")

            # Создаем резервную копию проекта
            shutil.make_archive(backup_file[:-4], 'zip', settings.BASE_DIR)

            message = f"Резервная копия успешно создана: {backup_file}"

    return render(request, 'control_panel/create_backup.html', {"message": message, "existing_backups": existing_backups})

def include_view(request, template_name):
    try:
        template = HtmlTemplate.objects.get(name=template_name)
        return render(request, 'includes/base_template.html', {
            'content': template.content,
            'title': template.name,
        })
    except HtmlTemplate.DoesNotExist:
        return render(request, '404.html', status=404)  # Отображение страницы 404, если шаблон не найден
