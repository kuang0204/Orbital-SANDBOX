import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Auto-load a local .env file (gitignored) in development. In production the
# platform (Render/Vercel) injects these as real environment variables, so the
# absence of a .env file is expected and harmless.
load_dotenv(BASE_DIR / '.env')


def _env_bool(name, default):
    return os.environ.get(name, str(default)).strip().lower() in ('1', 'true', 'yes', 'on')


# SECURITY WARNING: keep the secret key used in production secret!
# The hardcoded fallback below is ONLY for local development convenience.
# Production MUST provide SECRET_KEY via the environment — never deploy relying
# on this fallback value.
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-!f6c8^j6($-9&6vy0bzqit4juth4ryw5x06fpl*t@&fd^-0gj7',
)

# Defaults to True for local dev; production MUST set DEBUG=False explicitly.
DEBUG = _env_bool('DEBUG', True)

# Comma-separated list via env, e.g. "myapp.onrender.com,localhost".
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    if h.strip()
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# In development, allow any origin for convenience. In production, lock CORS
# down to an explicit allow-list supplied via the CORS_ALLOWED_ORIGINS env var
# (comma-separated, e.g. "https://myapp.vercel.app").
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        o.strip()
        for o in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
        if o.strip()
    ]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Default to local SQLite. If DATABASE_URL is set (production / Supabase /
# Postgres), parse it and use that instead — local dev without a .env keeps
# working unchanged.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.parse(
        os.environ['DATABASE_URL'],
        conn_max_age=600,
        ssl_require=not DEBUG,
    )

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
