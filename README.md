# Random Quotes (Django)
## Установка
python -m venv .venv && .\.venv\Scripts\activate
pip install -r requirements.txt
## Настройки
set DJANGO_SECRET_KEY=... & set DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
## Миграции и старт
python manage.py migrate
python manage.py runserver
## API
GET /api/quote/random/
POST /api/quote/<id>/vote/ {"value":"like"|"dislike"}
