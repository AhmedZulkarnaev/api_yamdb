# Проект YaMDb собирает отзывы пользователей на произведения. 

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

## Установка

1. Сначала склонируйте репозиторий:

    ```bash
    git clone git@github.com:AhmedZulkarnaev/api_yamdb.git
    cd ваш-репозиторий
    ```

2. Создайте виртуальное окружение и установите зависимости:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux/Mac
    pip install -r requirements.txt
    ```

## Использование

1. Запуск:

    ```bash
    python manage.py runserver
    ```

## Замечание

Убедитесь, что у вас есть актуальный токен пользователя.