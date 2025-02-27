import os

# Список приложений
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

# Содержимое базового шаблона
template_content = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - Главная</title>
</head>
<body>
    <h1>Добро пожаловать в приложение {app_name}!</h1>
    <p>Это базовый шаблон для приложения {app_name}.</p>
</body>
</html>
'''

# Путь к директории проекта
base_dir = os.path.join(os.getcwd(), 'apps')

# Создание шаблонов
for app in apps:
    # Путь к директории шаблонов приложения
    templates_dir = os.path.join(base_dir, app, 'templates', app)
    
    # Создаем директорию, если она не существует
    os.makedirs(templates_dir, exist_ok=True)
    
    # Путь к файлу шаблона
    template_file_path = os.path.join(templates_dir, 'index.html')
    
    # Запись содержимого в файл шаблона
    with open(template_file_path, 'w', encoding='utf-8') as f:
        f.write(template_content.format(app_name=app))
    
    print(f'Создан шаблон: {template_file_path}')