# YaMDb API
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Django](https://img.shields.io/badge/django-3.2-green.svg)

## Описание проекта

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

### Возможности проекта
- Создание и управление отзывами на произведения
- Комментирование отзывов
- Оценка произведений по шкале от 1 до 10
- Категоризация произведений (фильмы, книги, музыка и т.д.)
- Жанровая классификация произведений
- Система ролей пользователей с разными уровнями доступа

### Технологии
- Python 3.7+
- Django 3.2
- Django REST framework
- Simple JWT
- SQLite3

## Установка и запуск проекта

### Требования
- Python 3.7+
- pip

### Установка
1. Клонируйте репозиторий:
```bash
git clone git@github.com:username/api_yamdb.git
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
source venv/Scripts/activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Выполните миграции:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

### Запуск проекта
```bash
python manage.py runserver
```

## Работа с API

### Регистрация пользователей
1. Отправьте POST-запрос с `email` и `username` на эндпоинт `/api/v1/auth/signup/`
2. YaMDB отправит код подтверждения на указанный email
3. Получите JWT-токен, отправив POST-запрос с `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`

### Аутентификация
Для доступа к API необходимо передавать токен в заголовке каждого запроса:
```
Authorization: Bearer <ваш_токен>
```

### Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии
- **Пользователь** — может публиковать отзывы, ставить оценки произведениям, комментировать отзывы
- **Модератор** — те же права, что и у пользователя, плюс право удалять и редактировать любые отзывы и комментарии
- **Администратор** — полные права на управление контентом проекта

### Основные эндпоинты API
- `/api/v1/auth/signup/` (POST): Регистрация пользователя
- `/api/v1/auth/token/` (POST): Получение JWT-токена
- `/api/v1/users/` (GET, POST): Пользователи
- `/api/v1/users/me/` (GET, PATCH): Профиль пользователя
- `/api/v1/categories/` (GET, POST): Категории произведений
- `/api/v1/genres/` (GET, POST): Жанры произведений
- `/api/v1/titles/` (GET, POST): Произведения
- `/api/v1/titles/{title_id}/reviews/` (GET, POST): Отзывы
- `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` (GET, POST): Комментарии

Полная документация доступна по адресу `/redoc/` после запуска проекта.

## Работа с базой данных

### Импорт тестовых данных
В проекте есть готовый набор данных для тестирования в формате CSV:
- категории (category.csv)
- жанры (genre.csv)
- произведения (titles.csv)
- отзывы (review.csv)
- комментарии (comments.csv)
- пользователи (users.csv)

Чтобы загрузить данные, выполните команду:
```bash
python manage.py import_csv
```

## Тестирование

### Запуск тестов
```bash
python manage.py test
```

### Проверка работы API
После запуска проекта, документация API доступна по адресу:
```
http://127.0.0.1:8000/redoc/
```

## Примеры запросов

### Регистрация нового пользователя
```bash
POST /api/v1/auth/signup/
{
    "email": "user@example.com",
    "username": "string"
}
```

### Получение JWT-токена
```bash
POST /api/v1/auth/token/
{
    "username": "string",
    "confirmation_code": "string"
}
```

### Получение списка всех произведений
```bash
GET /api/v1/titles/
```

### Добавление отзыва
```bash
POST /api/v1/titles/{title_id}/reviews/
{
    "text": "string",
    "score": 1
}
```

### Добавление комментария к отзыву
```bash
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
{
    "text": "string"
}
```

### Получение категорий
```bash
GET /api/v1/categories/
```

### Фильтрация произведений
```bash
GET /api/v1/titles/?category=movies&genre=fiction&year=2024
```

## Возможные ответы API

### Успешные ответы
- 200: Запрос выполнен успешно
- 201: Ресурс успешно создан
- 204: Ресурс успешно удален

### Ошибки
- 400: Ошибка в запросе
- 401: Требуется авторизация
- 403: Недостаточно прав
- 404: Ресурс не найден