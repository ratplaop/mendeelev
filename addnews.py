#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Скрипт скачивания новостей
# Скрипт скачивания новостей
# Скрипт скачивания новостей


import requests
from bs4 import BeautifulSoup
import os
import re

# Базовые настройки
BASE_URL = "https://mendeleevfest.com"
NEWS_URL = f"{BASE_URL}/news/"
OUTPUT_DIR = os.path.join("media", "add")  # Папка для хранения текстов новостей и изображений

# Создаём каталог, если его не существует
os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_filename(name):
    """
    Функция удаляет недопустимые символы для имени файла, заменяет пробелы на нижнее подчеркивание
    и приводит результат к нижнему регистру.
    Например, "Продлеваем подачу заявок" преобразуется в "продлеваем_подачу_заявок".
    """
    # Заменяем пробелы на '_'
    name = name.replace(" ", "_")
    # Удаляем символы, недопустимые в именах файлов
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    # Приводим к нижнему регистру
    return name.lower()


def get_extension(_):
    """
    Функция возвращает расширение .jpg независимо от MIME-типа,
    что гарантирует сохранение изображения в формате jpg.
    """
    return ".jpg"


def scrape_news():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(NEWS_URL, headers=headers)

    if response.status_code != 200:
        print("Не удалось подключиться к странице новостей.")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")

    if not articles:
        print("Не найдено ни одной новости.")
        return

    for article in articles:
        # Извлекаем ссылку на детальную страницу новости
        a_tag = article.find("a", href=True)
        if not a_tag:
            continue
        news_link = a_tag["href"]
        if not news_link.startswith("http"):
            news_link = BASE_URL + news_link

        # Заголовок новости для формирования имени файла
        title = a_tag.get_text(strip=True)
        if not title:
            title_tag = article.find(["h1", "h2", "h3"])
            title = title_tag.get_text(strip=True) if title_tag else "news"
        filename = clean_filename(title)

        # Извлекаем URL изображения из блока с классом "wpr-grid-image-wrap"
        image_wrap = article.find("div", class_="wpr-grid-image-wrap")
        if image_wrap and image_wrap.has_attr("data-src"):
            img_url = image_wrap["data-src"]
        else:
            # Альтернативно, пробуем найти тег img с data-src или src
            img_tag = article.find("img")
            img_url = (img_tag.get("data-src") if img_tag and img_tag.has_attr("data-src")
                       else (img_tag.get("src") if img_tag else None))

        # Переходим на страницу детали новости для получения её полного текста
        news_response = requests.get(news_link, headers=headers)
        if news_response.status_code != 200:
            print(f"Ошибка при загрузке новости: {news_link}")
            continue

        news_soup = BeautifulSoup(news_response.text, "html.parser")
        # Пытаемся найти контейнер с текстом новости
        content_container = news_soup.find("div", class_="entry-content")
        if content_container is None:
            content_container = news_soup.find("div", class_="post-content")
        if content_container:
            news_text = content_container.get_text(separator="\n", strip=True)
        else:
            news_text = news_soup.get_text(separator="\n", strip=True)

        # Сохраняем текст новости
        text_file_path = os.path.join(OUTPUT_DIR, filename + ".txt")
        with open(text_file_path, "w", encoding="utf-8") as file:
            file.write(news_text)
        print(f"Новость сохранена в: {text_file_path}")

        # Если URL изображения найден, скачиваем и сохраняем его
        if img_url:
            if not img_url.startswith("http"):
                img_url = BASE_URL + img_url
            img_resp = requests.get(img_url, headers=headers)
            if img_resp.status_code == 200 and img_resp.content:
                ext = get_extension(img_resp.headers.get("Content-Type"))
                photo_file_path = os.path.join(OUTPUT_DIR, filename + ext)
                with open(photo_file_path, "wb") as img_file:
                    img_file.write(img_resp.content)
                print(f"Изображение сохранено в: {photo_file_path}")
            else:
                print(f"Не удалось загрузить изображение по адресу: {img_url}")
        else:
            print("URL изображения не найден для данной новости.")


if __name__ == "__main__":
    scrape_news()
    print("Скрипт завершил копирование новостей.")