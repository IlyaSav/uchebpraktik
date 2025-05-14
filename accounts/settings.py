import os

# Определение базового каталога проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Секретный ключ для вашего приложения
SECRET_KEY = 'ваш_секретный_ключ'  # Замените на ваш реальный секретный ключ

# Режим отладки
DEBUG = False  # На продакшене всегда False!

# Разрешенные хосты
ALLOWED_HOSTS = ['doghap23.pythonanywhere.com']

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',  # Ваше приложение здесь
]

# Промежуточное ПО
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Корневой URL конфигурации
ROOT_URLCONF = 'uchebpraktik.urls'  # Замените на имя вашего проекта

# WSGI приложение
WSGI_APPLICATION = 'uchebpraktik.wsgi.application'  # Замените на имя вашего проекта

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Настройки статических файлов
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Изменено на 'staticfiles' для лучшей практики

# Дополнительные настройки (например, для статических файлов в продакшене)
if not DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
