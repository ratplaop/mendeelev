from django.urls import path
from .views import (
    control_panel_list,
    control_panel_create,
    control_panel_edit,
    dashboard,
    create_app,
    check_routes,
    create_template,
    check_structure,
    run_checks,
    check_settings,
    configure_new_app,
    analyze_models,
    create_backup,
    
)

app_name = 'control_panel'

urlpatterns = [
    path('', control_panel_list, name='control_panel_list'),  # Список контрольных панелей
    path('create/', control_panel_create, name='control_panel_create'),  # Создание новой панели
    path('edit/<int:panel_id>/', control_panel_edit, name='control_panel_edit'),  # Редактирование панели
    path('dashboard/', dashboard, name='dashboard'),  # Главная панель
    path('create_app/', create_app, name='create_app'),  # Создание приложения
    path('check_routes/', check_routes, name='check_routes'),  # Проверка маршрутов
    path('create_template/', create_template, name='create_template'),  # Создание шаблона
    path('check_structure/', check_structure, name='check_structure'),  # Проверка структуры
    path('run_checks/', run_checks, name='run_checks'),  # Запуск проверок
    path('check_settings/', check_settings, name='check_settings'),  # Проверка настроек
    path('configure_new_app/', configure_new_app, name='configure_new_app'),  # Конфигурация нового приложения
    path('analyze_models/', analyze_models, name='analyze_models'),  # Анализ моделей
    path('create_backup/', create_backup, name='create_backup'),  # Создание резервной копии
    
]
