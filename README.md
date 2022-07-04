Клонировать репозиторий
git clone https://github.com/ravimb06/api_yamdb.git

cd api_yamdb

Cоздать и активировать виртуальное окружение:
python -m venv venv

source venv/scripts/activate

python -m pip install --upgrade pip

Установить зависимости из файла requirements.txt:
pip install -r requirements.txt

Выполнить миграции:
python manage.py migrate

Запустить проект:
python manage.py runserver

В проекте доступны следующие эндпоинты:
http://127.0.0.1:8000/api/v1/auth/signup/  - Получение кода подверждения на email

{
"email": "string",
"username": "string"
}

http://127.0.0.1:8000/api/v1/auth/token/ - Получение токена для авторизации

{
"username": "string",
"confirmation_code": "string"
}

http://127.0.0.1:8000/api/v1/categories/ - Работа с категориями, доступны запросы Get, Post и Del

http://127.0.0.1:8000/api/v1/genres/ - Работа с жанрами, доступны запросы Get, Post и Del

http://127.0.0.1:8000/api/v1/titles/ - Работа со статьями , доступны запросы Get, Post, Patch и Del

http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/  - Работа с отзывами , доступны запросы Get, Post, Patch и Del

http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Работа с комментариями , доступны запросы Get, Post, Patch и Del

http://127.0.0.1:8000/api/v1/users/ - Создание пользователя и получение информации о всех пользователях. Доступны запросы Get, Post

http://127.0.0.1:8000/api/v1/users/{username}/ - Получение информации о конкретном пользователе и редактирование информации о нем. Доступны доступны запросы Get, Postm Del

http://127.0.0.1:8000/api/v1/users/me/ - Получение и изменение своих данных, доступны запросы Get, Patch

Клонирование базы

перейти в Python Shell командой

python manage.py shell

импорт необходимых модулей

import os
