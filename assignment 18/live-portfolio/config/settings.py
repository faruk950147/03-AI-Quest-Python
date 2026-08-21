import os
from pathlib import Path
from dotenv import load_dotenv
from celery.schedules import crontab
from datetime import timedelta
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

# ========================
# Base directory
# ========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# Load environment variables from .env file
# ========================
load_dotenv(BASE_DIR / ".env")


# ========================
# Security settings
# ========================
SECRET_KEY = os.environ.get("SECRET_KEY")

# ========================
# Debug and allowed hosts
# ========================
DEBUG = os.environ.get("DEBUG", "False") == "True"

# ========================
# Allowed hosts and base URL
# ========================
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")
BASE_URL = os.environ.get("BASE_URL", default="http://127.0.0.1:8000")


# =========================
# Application definition
# =========================
INSTALLED_APPS = [
    'unfold',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'ckeditor',
    'rest_framework',  # DRF
    'corsheaders',  # CORS
    'rest_framework_simplejwt',  # JWT auth
    'rest_framework_simplejwt.token_blacklist',  # JWT token blacklist
    # Local apps
    'account.apps.AccountConfig',
    'settings.apps.SettingsConfig',
    'home.apps.HomeConfig',
    'about.apps.AboutConfig',
    'resume.apps.ResumeConfig',
    'service.apps.ServiceConfig',
    'portfolio.apps.PortfolioConfig',
    'contact.apps.ContactConfig',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'settings.context_processors.settings_context'
            ],
        },
    },
]


# WSGI_APPLICATION is for HTTP
# WSGI_APPLICATION = 'config.wsgi.application'


# =========================
# ASGI_APPLICATION is for WebSocket
# ========================
ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/0"],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "live_portfolio",
        "TIMEOUT": 300,  # Cache timeout in seconds (5 minutes)
    }
}

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = "Asia/Dhaka"
CELERY_ENABLE_UTC = False

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300
CELERY_TASK_SOFT_TIME_LIMIT = 240


# ========================
# Database
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

# =========================
# Password validation
# =========================

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


# =========================
# Internationalization
# =========================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# =========================
# Default primary key field type
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ========================
# Authentication settings       
# Custom user model
# ========================
AUTH_USER_MODEL = 'account.User'


# =========================
# Static files 
# =========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# =========================
# Email configuration
# =========================
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))

EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() == "true"

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")


# =========================
# Django REST Framework
# =========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # JWT Authentication this is used for API authentication
        'rest_framework_simplejwt.authentication.JWTAuthentication', 
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # Default permission for API views 
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# =========================
# Simple JWT
# =========================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",

    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
}


# =========================
# Logging
# =========================
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {'standard': {'format': '[{levelname}] {asctime} {name} - {message}', 'style': '{'}},
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'level': 'INFO', 'formatter': 'standard'},
        'debug_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
            'maxBytes': 5*1024*1024,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 5*1024*1024,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {'handlers': ['console', 'error_file'], 'level': 'INFO', 'propagate': False},
        'project': {'handlers': ['console', 'debug_file', 'error_file'], 'level': 'DEBUG', 'propagate': False},
    },
}

# =========================
# Security headers
# =========================
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'


# =========================
# CKEditor Configuration
# =========================
CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono-lisa",
        "toolbar": "full",
        "height": 400,
        "width": "100%",
        "resize_enabled": True,
    },
}


# ==========================
# Unfold Configuration
# ==========================
UNFOLD = {
    "SITE_TITLE": "Omar Faruk",
    "SITE_HEADER": "Dashboard",
    "SITE_SUBHEADER": "Admin",
    "SITE_SYMBOL": "account_circle",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "Development",
    "SITE_URL": "/",
    "SITE_DROPDOWN": [{
            "icon": "diamond",
            "title": _("Site Visit"),
            "link": BASE_URL,
        }],
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("assets/img/favicon.svg"),
        },
    ],

}