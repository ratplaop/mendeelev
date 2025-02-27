from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import include_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls')),  # Основное приложение
    path('news/', include('apps.news.urls')),  # Приложение новостей
    path('events/', include('apps.events.urls')),  # Приложение событий
    path('regions/', include('apps.regions.urls')),  # Приложение регионов
    path('actual/', include('apps.actual.urls')),  # Приложение актуальных материалов
    path('control/', include('apps.control_panel.urls')),  # Контрольная панель
    path('membership/', include('apps.membership.urls')),  # Приложение членства
    path('telegram/', include('apps.telegram_bot.urls')),
    path('bookmagazine/', include('apps.bookmagazine.urls')), 
    path('includes/<str:template_name>/', include_view, name='include_view'),
    path('tinymce/', include('tinymce.urls')),
]

# Если у вас есть статические файлы, добавьте их
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

