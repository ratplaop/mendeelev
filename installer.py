import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

class ProjectInstaller:
    def __init__(self):
        self.project_name = 'myproject'
        self.base_dir = Path.cwd()
        self.apps_dir = self.base_dir / 'apps'
        self.templates_dir = self.base_dir / 'templates'
        self.config_dir = self.base_dir / 'config'
        self.static_dir = self.base_dir / 'static'
        self.media_dir = self.base_dir / 'media'
        
    def run(self):
        try:
            print("🚀 Начинаем установку проекта...")
            self.check_prerequisites()
            self.create_project_structure()
            self.create_virtual_environment()
            self.install_requirements()
            self.create_apps()
            self.setup_settings()
            self.create_manage_py()
            self.create_env_file()
            self.setup_telegram_bot()
            self.setup_payment_system()
            self.setup_control_panel()
            print("✅ Установка успешно завершена!")
        except Exception as e:
            print(f"❌ Ошибка при установке: {str(e)}")
            sys.exit(1)

    def check_prerequisites(self):
        print("🔍 Проверка необходимых компонентов...")
        try:
            import django
        except ImportError:
            print("Django не установлен. Установка...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "django"])

    def create_project_structure(self):
        print("📁 Создание структуры проекта...")
        
        # Создаем основные директории
        directories = [
            self.apps_dir,
            self.templates_dir,
            self.static_dir,
            self.media_dir,
            self.base_dir / 'backups',
            self.config_dir,
            self.templates_dir / 'includes',
            self.static_dir / 'css',
            self.static_dir / 'js',
            self.static_dir / 'img',
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Создана директория: {directory}")
            
        # Создаем __init__.py файлы
        init_files = [
            self.config_dir / '__init__.py',
            self.apps_dir / '__init__.py'
        ]
        
        for init_file in init_files:
            init_file.touch()

    def create_virtual_environment(self):
        print("🔧 Создание виртуального окружения...")
        if not (self.base_dir / 'venv').exists():
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
            print("  ✓ Виртуальное окружение создано")

    def install_requirements(self):
        print("📦 Установка зависимостей...")
        requirements = [
            'Django>=4.2,<5.0',
            'Pillow>=10.0.0',
            'python-telegram-bot>=20.0',
            'yookassa>=2.3.0',
            'django-crispy-forms>=2.0',
            'django-allauth>=0.54.0',
            'django-ckeditor>=6.5.1',
            'django-debug-toolbar>=4.0.0',
            'django-environ>=0.10.0',
            'psycopg2-binary>=2.9.6',
            'gunicorn>=21.2.0',
            'whitenoise>=6.5.0',
        ]
        
        with open(self.base_dir / 'requirements.txt', 'w') as f:
            f.write('\n'.join(requirements))
        
        pip_path = str(self.base_dir / 'venv' / 'bin' / 'pip')
        if os.name == 'nt':  # Windows
            pip_path = str(self.base_dir / 'venv' / 'Scripts' / 'pip')
            
        subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
        print("  ✓ Зависимости установлены")

    def create_apps(self):
        print("📱 Создание приложений...")
        
        apps = [
            'main',
            'news',
            'events',
            'regions',
            'actual',
            'control_panel',
            'membership',
            'library',
            'telegram_bot'
        ]
        
        for app in apps:
            app_path = self.apps_dir / app
            app_path.mkdir(exist_ok=True)
            
            # Создаем структуру приложения
            (app_path / 'migrations').mkdir(exist_ok=True)
            (app_path / '__pycache__').mkdir(exist_ok=True)
            (app_path / 'templates' / app).mkdir(parents=True, exist_ok=True)
            (app_path / 'static' / app).mkdir(parents=True, exist_ok=True)
            
            # Создаем базовые файлы приложения
            self.create_app_files(app, app_path)
            
            # Создаем базовые модели и представления
            self.create_models(app, app_path)
            self.create_views(app, app_path)
            
            print(f"  ✓ Создано приложение: {app}")

    def create_app_files(self, app_name, app_path):
        """Создание базовых файлов для приложения"""
        
        # __init__.py
        (app_path / '__init__.py').touch()
        
        # apps.py
        apps_content = f'''from django.apps import AppConfig

class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
    verbose_name = '{app_name.capitalize()}'
'''
        self.write_file(app_path / 'apps.py', apps_content)
        
        # admin.py
        admin_content = '''from django.contrib import admin
# Register your models here.
'''
        self.write_file(app_path / 'admin.py', admin_content)
        
        # urls.py
        urls_content = f'''from django.urls import path
from . import views

app_name = '{app_name}'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
'''
        self.write_file(app_path / 'urls.py', urls_content)
        
        # views.py
        views_content = f'''from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

class IndexView(ListView):
    template_name = '{app_name}/index.html'
    context_object_name = 'objects'
    
    def get_queryset(self):
        return []
'''
        self.write_file(app_path / 'views.py', views_content)
        
        # models.py
        models_content = '''from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
'''
        self.write_file(app_path / 'models.py', models_content)
        
        # forms.py
        forms_content = '''from django import forms
from .models import *

# Create your forms here.
'''
        self.write_file(app_path / 'forms.py', forms_content)
        
        # services.py
        services_content = '''# Business logic and services
'''
        self.write_file(app_path / 'services.py', services_content)
        
        # signals.py
        signals_content = '''from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *

# Create your signals here.
'''
        self.write_file(app_path / 'signals.py', signals_content)

    def create_manage_py(self):
        print("📝 Создание manage.py...")
        manage_content = '''#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
'''
        self.write_file(self.base_dir / 'manage.py', manage_content)
        # Делаем файл исполняемым на Unix-системах
        if os.name != 'nt':
            os.chmod(self.base_dir / 'manage.py', 0o755)

    def setup_telegram_bot(self):
        print("🤖 Настройка Telegram бота...")
        
        bot_settings = '''
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

def start_bot():
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Добавляем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    
    # Запускаем бота
    updater.start_polling()
    updater.idle()

def start(update, context):
    update.message.reply_text('Добро пожаловать!')

def help(update, context):
    update.message.reply_text('Справка по использованию бота')
'''
        self.write_file(self.apps_dir / 'telegram_bot' / 'bot.py', bot_settings)

    def setup_payment_system(self):
        print("💳 Настройка платежной системы...")
        
        payment_settings = '''
from yookassa import Configuration, Payment
import uuid

class PaymentService:
    @staticmethod
    def init_payment(amount, description):
        Configuration.account_id = os.getenv('YOOKASSA_SHOP_ID')
        Configuration.secret_key = os.getenv('YOOKASSA_SECRET_KEY')

        payment = Payment.create({
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://www.example.com/return_url"
            },
            "capture": True,
            "description": description,
            "metadata": {
                "order_id": str(uuid.uuid4())
            }
        })
        
        return payment.confirmation.confirmation_url
'''
        self.write_file(self.apps_dir / 'membership' / 'payment.py', payment_settings)

    def create_env_file(self):
        print("🔒 Создание .env файла...")
        
        env_content = '''
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Telegram
TELEGRAM_BOT_TOKEN=your-bot-token-here

# YooKassa
YOOKASSA_SHOP_ID=your-shop-id-here
YOOKASSA_SECRET_KEY=your-secret-key-here

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
'''
        self.write_file(self.base_dir / '.env', env_content)

    def setup_control_panel(self):
        print("🎛️ Настройка контрольной панели...")
        
        panel_settings = '''
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
import os
import json

class ControlPanelView(UserPassesTestMixin, TemplateView):
    template_name = 'control_panel/index.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apps'] = self.get_installed_apps()
        context['templates'] = self.get_templates()
        return context
    
    def get_installed_apps(self):
        from django.conf import settings
        return [app for app in settings.INSTALLED_APPS if app.startswith('apps.')]
    
    def get_templates(self):
        template_dir = settings.TEMPLATES[0]['DIRS'][0]
        templates = []
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file.endswith('.html'):
                    templates.append(os.path.join(root, file))
        return templates
'''
        self.write_file(self.apps_dir / 'control_panel' / 'views.py', panel_settings)

    def create_models(self, app_name, app_path):
        """Создание базовых моделей для приложения"""
        models_content = f'''from django.db import models
from django.contrib.auth.models import User

class {app_name.capitalize()}Model(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
'''
        self.write_file(app_path / 'models.py', models_content)

    def create_views(self, app_name, app_path):
        """Создание базовых представлений для приложения"""
        views_content = f'''from django.views.generic import ListView
from .models import {app_name.capitalize()}Model

class {app_name.capitalize()}ListView(ListView):
    model = {app_name.capitalize()}Model
    template_name = '{app_name}/list.html'
    context_object_name = 'objects'
'''
        self.write_file(app_path / 'views.py', views_content)

    def create_urls(self):
        print("🔗 Создание URL маршрутов...")
        
        # Основной urls.py
        main_urls = '''
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls')),
    path('news/', include('apps.news.urls')),
    path('events/', include('apps.events.urls')),
    path('regions/', include('apps.regions.urls')),
    path('actual/', include('apps.actual.urls')),
    path('control/', include('apps.control_panel.urls')),
    path('membership/', include('apps.membership.urls')),
    path('library/', include('apps.library.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
'''
        self.write_file(self.config_dir / 'urls.py', main_urls)

    def create_templates(self):
        print("🎨 Создание шаблонов...")
        
        # Базовый шаблон
        base_template = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Сайт{% endblock %}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <!-- Навигация -->
    </nav>
    
    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>
    
    <footer class="footer mt-auto py-3 bg-light">
        <div class="container">
            <span class="text-muted">© {% now "Y" %} Все права защищены</span>
        </div>
    </footer>
    
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
'''
        self.write_file(self.templates_dir / 'base.html', base_template)

    def create_static_files(self):
        print("📁 Создание статических файлов...")
        
        # CSS
        main_css = '''
/* Основные стили */
body {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

main {
    flex: 1;
}
'''
        self.write_file(self.static_dir / 'css' / 'main.css', main_css)
        
        # JavaScript
        main_js = '''
// Основные скрипты
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация
});
'''
        self.write_file(self.static_dir / 'js' / 'main.js', main_js)

    def write_file(self, file_path, content):
        with open(file_path, 'w') as f:
            f.write(content)

    def setup_settings(self):
        print("⚙️ Настройка конфигурации проекта...")
        
        settings_content = '''import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'crispy_forms',
    'ckeditor',
    'debug_toolbar',
    'allauth',
    'allauth.account',
    
    # Local apps
    'apps.main',
    'apps.news',
    'apps.events',
    'apps.regions',
    'apps.actual',
    'apps.control_panel',
    'apps.membership',
    'apps.library',
    'apps.telegram_bot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# CKEditor
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'

# Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# Authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = 'main:home'
LOGOUT_REDIRECT_URL = 'main:home'

# AllAuth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# YooKassa
YOOKASSA_SHOP_ID = os.getenv('YOOKASSA_SHOP_ID', '')
YOOKASSA_SECRET_KEY = os.getenv('YOOKASSA_SECRET_KEY', '')
'''
        
        # Создаем файл settings.py
        self.write_file(self.config_dir / 'settings.py', settings_content)
        
        # Создаем wsgi.py
        wsgi_content = '''import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
'''
        self.write_file(self.config_dir / 'wsgi.py', wsgi_content)
        
        # Создаем asgi.py
        asgi_content = '''import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_asgi_application()
'''
        self.write_file(self.config_dir / 'asgi.py', asgi_content)
        
        print("  ✓ Настройки проекта созданы")

if __name__ == "__main__":
    try:
        installer = ProjectInstaller()
        installer.run()
    except KeyboardInterrupt:
        print("\n⚠️ Установка прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {str(e)}")
        sys.exit(1)

        
