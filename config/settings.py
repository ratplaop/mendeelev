import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['195.2.74.203']
CSRF_COOKIE_SECURE = False  # Убедитесь, что это значение соответствует вашему окружению
CSRF_TRUSTED_ORIGINS = ['http://195.2.74.203:8000']  # Добавьте ваш домен, если необходимо

# Application definition
INSTALLED_APPS = [
    'apps.bookmagazine',  # Добавлено приложение bookmagazine
    'jazzmin',
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
    'apps.telegram_bot',
    'tinymce',
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
    'allauth.account.middleware.AccountMiddleware', 
]

ROOT_URLCONF = 'config.urls'


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',  # Используем полную панель инструментов
        'height': 400,
        'width': '100%',
        'plugins': 'advlist autolink lists link image charmap print preview anchor help',
        'toolbar_Custom': [
            ['undo', 'redo', 'styles', 'formatselect', 'bold', 'italic', 'underline', 'strikethrough'],
            ['forecolor', 'backcolor', 'removeformat', 'blockquote'],
            ['alignleft', 'aligncenter', 'alignright', 'alignjustify'],
            ['outdent', 'indent', 'bullist', 'numlist', 'table'],
            ['link', 'image', 'charmap', 'hr', 'pagebreak'],
            ['preview', 'print', 'fullscreen', 'help'],
        ],
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

STATIC_URL = '/static/'
STATICFILES_DIRS = [
       os.path.join(BASE_DIR, 'static'),  # Укажите путь к статическим файлам в корневой папке
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

LOGIN_REDIRECT_URL = 'membership:home'
LOGOUT_REDIRECT_URL = 'main:home'

# AllAuth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# YooKassa
YOOKASSA_SETTINGS = {
    'SHOP_ID': '1031484',
    'SECRET_KEY': 'test_vtqzw1vJa14mDgYc5gypRJvXhTOFGXvcMoqbHsKfH34',
}