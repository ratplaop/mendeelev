import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils.text import slugify
from unidecode import unidecode # type: ignore
from apps.main.models import News as MainNews
from django.utils import timezone
from django.db import IntegrityError

# Задайте поддержку допустимых расширений для фотографий
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']

class Command(BaseCommand):
    help = ("Импорт новостей из папки. Каждая новость представлена текстовым файлом (с расширением .txt) и изображением с таким же названием. "
            "При добавлении изображений имя файла преобразуется: кириллица транслитерируется в латиницу и имя сокращается до 15 символов.")

    def add_arguments(self, parser):
        parser.add_argument(
            'folder',
            type=str,
            help="Путь к папке с файлами новостей"
        )

    def handle(self, *args, **options):
        folder = options['folder']
        if not os.path.isdir(folder):
            self.stdout.write(self.style.ERROR(f"Папка '{folder}' не найдена."))
            return

        imported_count = 0

        # Получаем список всех файлов в папке
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) and filename.lower().endswith('.txt'):
                # Заменяем нижние подчеркивания на пробелы и делаем первую букву заглавной.
                base_name = os.path.splitext(filename)[0]
                title = base_name.replace('_', ' ')
                if title:
                    title = title[0].upper() + title[1:]
                # Читаем контент из текстового файла
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                # Ищем файл изображения с таким же базовым именем и одним из допустимых расширений:
                image_path = None
                for ext in IMAGE_EXTENSIONS:
                    candidate = os.path.join(folder, base_name + ext)
                    if os.path.isfile(candidate):
                        image_path = candidate
                        break

                # Создаем объект новости (если новость с таким названием ещё не существует)
                news_data = {
                    'title': title,
                    'author': 'Автор новости',
                    'content': content,
                    'slug': slugify(title)
                }
                
                # Проверяем уникальность slug
                original_slug = news_data['slug']
                unique_slug = original_slug
                counter = 1
                while MainNews.objects.filter(slug=unique_slug).exists():
                    unique_slug = f"{original_slug}-{counter}"
                    counter += 1
                
                news_data['slug'] = unique_slug

                try:
                    news_obj, created = MainNews.objects.update_or_create(
                        slug=news_data['slug'],
                        defaults={
                            'title': news_data['title'],
                            'author': news_data['author'],
                            'content': news_data['content'],
                        }
                    )
                    if created:
                        # Если найдено изображение, прикрепляем его с изменением имени файла
                        if image_path:
                            original_name = os.path.basename(image_path)
                            name_part, ext = os.path.splitext(original_name)
                            # Транслитерируем имя и преобразуем в slug, затем сокращаем до 15 символов
                            slug_name = slugify(unidecode(name_part))
                            short_slug = slug_name[:15] if len(slug_name) > 15 else slug_name
                            short_name = short_slug + ext
                            with open(image_path, 'rb') as img_file:
                                news_obj.image.save(short_name, File(img_file), save=True)
                        imported_count += 1
                        self.stdout.write(self.style.SUCCESS(f"Импортирована новость: '{title}'"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Новость с заголовком '{title}' уже существует."))
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f'Ошибка при добавлении новости: {e}'))
        self.stdout.write(self.style.SUCCESS(f"\nИмпорт завершен. Добавлено новостей: {imported_count}.")) 