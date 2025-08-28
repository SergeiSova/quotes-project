from pathlib import Path
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def env(name, default=None):
    return os.getenv(name, default)

SECRET_KEY = env("DJANGO_SECRET_KEY", "8qi#)&vd5%)4zqj7v4(c_sxzcc_07l+eitxh_4ql^-qd+-9c_)")
DEBUG = env("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles" 
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

CSRF_TRUSTED_ORIGINS = [f"http://{h}" for h in ALLOWED_HOSTS if h not in ("127.0.0.1","localhost")] + \
                       [f"https://{h}" for h in ALLOWED_HOSTS if h not in ("127.0.0.1","localhost")]

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'change-me'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'quotes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
