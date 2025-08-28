# Random Quotes (Django)

Страница со случайной цитатой (весовая выдача), лайки/дизлайки, добавление из формы, ТОП.

## Требования
- Python 3.10+
- Django 5.x

## Установка

### Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt

### macOS/Linux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Настройки окружения

Создайте `.env` или экспортируйте переменные:

- `DJANGO_SECRET_KEY=...`
- `DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost` 
- `DJANGO_DEBUG=True`
- Для продакшена обязательно:
  - `CSRF_TRUSTED_ORIGINS=https://your-domain.tld`  ← схема обязательна.  
    Подробнее в доке: https://docs.djangoproject.com/en/stable/ref/settings/#csrf-trusted-origins

## Локальная разработка

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Откройте:
- `http://127.0.0.1:8000/` — главная (случайная цитата по весу)
- `http://127.0.0.1:8000/add/` — добавить цитату
- `http://127.0.0.1:8000/top/` — топ-подборки
- `http://127.0.0.1:8000/admin/` — админка

## Деплой (в т.ч. PythonAnywhere)

1) В `settings.py` пропишите:

```python
ALLOWED_HOSTS = ["your-domain.tld"]
CSRF_TRUSTED_ORIGINS = ["https://your-domain.tld"]
STATIC_ROOT = BASE_DIR / "staticfiles"

