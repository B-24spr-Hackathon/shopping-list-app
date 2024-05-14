'''
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
'''

from pathlib import Path
from datetime import timedelta


"""
デプロイ時に変更する項目（始点）
"""
BACKEND_URL = "https://127.0.0.1:8000"
FRONTEND_URL = "http://127.0.0.1:5173"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "django-db",
        "USER": "django",
        "PASSWORD": "django",
        "HOST": "db",
        "PORT": "3306",
    }
}

CORS_ALLOWED_ORIGINS = [f"{FRONTEND_URL}", "http://localhost:5173"]

"""
デプロイ時に変更する項目（終点）
"""


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i3n5v%kp87j+-e(qouya93ir71tj47no^r%-m*b*t$+z*n%^y9'

# JWT用の署名鍵
JWT_KEY = 'eaef77e7815fe048132cb830be2641c966306d78aa27dbad1cfe24a28300e3f5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    # 'django.contrib.sessions',
    # 'django.contrib.staticfiles',
    'rest_framework',
    'shop',
    'corsheaders',
    
    # デプロイ時に削除
    'sslserver'
]

# AbstractUserを使うため追記
AUTH_USER_MODEL = 'shop.User'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# デフォルトでViewに適用する認証クラス
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'shop.authentication.CustomJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# JWTの設定
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': JWT_KEY,
    'ISSUER': 'Kaimotto',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'user_id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'shop.authentication.user_authentication_rule',
    'COOKIE_NAME': 'jwt_token'
}

# LINEログインの設定
LINE_CHANNEL_ID = '2004751038'
LINE_CHANNEL_SECRET = 'b2b453579e5786b991a979e0c555f1a0'
REDIRECT_URL = f'{BACKEND_URL}/api/callback/'
STATE = 'shopping-list12345'

# LINEログインでのフロントエンドリダイレクトURL
FRONT_REDIRECT_URL = f'{FRONTEND_URL}/'
FRONT_ERROR_URL = f"{FRONTEND_URL}/lineloginerror"

# LINE連携後のフロントエンドリダイレクトURL
LINK_REDIRECT_URL = f"{FRONTEND_URL}/"

# 買い物リストのURL
SHOPPING_LIST_URL = f"{FRONTEND_URL}/shoppinglist"

# LINE公式チャンネルの設定
CHANNEL_URL = 'https://lin.ee/Ekblccd'
REPLY_URL = 'https://api.line.me/v2/bot/message/reply'
PUSH_URL = 'https://api.line.me/v2/bot/message/push'

# チャンネルアクセストークン
CHANNEL_ACCESS_TOKEN = '3XxTjzUjmAoJC2uybNTaRAis+pRQtbfsr/Lf48T7VHPxvrchvxqkwCHL8W2WOaw8AZRPwzFFStB25Hi50j/0Rn2lg/i9q2+uxRxF+iOoNwgUMpGdF2YEElhVrPXnD6g1Gj/6y2gYwlZT5lQ+wu2Y4AdB04t89/1O/w1cDnyilFU='

# Celery設定
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_TIMEZONE = 'Asia/Tokyo'

# Celery Beatの呼出し時間
BATCH_HOUR = 3
BATCH_MINUTE = 0
