# Telegram бот

## Описание

Проект представляет собой telegram бота для планирования встреч.

### В основной функционал входит

- Регистрация пользователя (заполнение графика свободного времени)
- Просмотр собственного расписания и других пользователей
- Нахождение пересечний по времени в расписаниях групп людей для определения премерных окон для встречи

## Технологии

- Фреймворк: aiogram
- Базы данных: mongodb (Motor), redis (redis)
- Тестирование: pytest, pytest-asyncio, testcontainers

## Запуск приложения

- вставить собственный токен в timetable_bot/src/.env.local
- убрать .local у .env файлов:
    - mongo_credentials.env.local
    - mongo_express_credentials.env.local
    - redis_credentials.env.local
    - timetable_bot/src/.env.local
- запустить docker
- собрать docer-compose файл:
    ```
    docker compose -f 'docker-compose.yml' up -d --build 
    ```
- запустить main

## Тестирование

### Тестирование основного функционала:
- Конструирование расписания из регистрационной информации в /tests/timetable_service_test/test_timetable_construction.py
- Поиск пересечений в расписаниях пользователей в /tests/timetable_service_test/test_timetable_intersection.py

### Тестирование подключения к базе данных и выполнения запросов:
- Проверка основных возможностей в /tests/test_client.py
