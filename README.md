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

Приложение читает настройки из переменных окружения. Файл `.env` автоматически не загружается.

- `DJANGO_SECRET_KEY` — обязателен, если режим отладки выключен
- `DJANGO_DEBUG` — `1` для локальной разработки, по умолчанию выключен
- `DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost`
- `CSRF_TRUSTED_ORIGINS=https://your-domain.tld` — схема обязательна.
  Подробнее в доке: https://docs.djangoproject.com/en/stable/ref/settings/#csrf-trusted-origins
- `DJANGO_CLIENT_IP_HEADER=HTTP_X_REAL_IP` — обязателен за обратным прокси. Укажите заголовок, который прокси выставляет сам, иначе все посетители будут считаться одним голосующим

## Локальная разработка

Включите режим отладки:

- Windows (PowerShell): `$env:DJANGO_DEBUG="1"`
- macOS/Linux: `export DJANGO_DEBUG=1`

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Откройте:
- `http://127.0.0.1:8000/` — главная (случайная цитата по весу)
- `http://127.0.0.1:8000/add/` — добавить цитату
- `http://127.0.0.1:8000/top/` — топ-подборки
- `http://127.0.0.1:8000/admin/` — админка

## Деплой (в т.ч. PythonAnywhere)

1) Задайте переменные окружения:

```bash
DJANGO_SECRET_KEY=<новый случайный ключ>
DJANGO_ALLOWED_HOSTS=your-domain.tld
CSRF_TRUSTED_ORIGINS=https://your-domain.tld
DJANGO_CLIENT_IP_HEADER=HTTP_X_REAL_IP
```

Сгенерировать ключ:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```
