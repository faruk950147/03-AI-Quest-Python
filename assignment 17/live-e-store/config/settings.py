from pathlib import Path
import os
import dotenv
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from celery.schedules import crontab

dotenv.load_dotenv()

# =========================
# Base directory
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:8000"
)

# =========================
# Installed Applications
# =========================
INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',  # DRF
    # 'rest_framework.authtoken',  # Token auth
    'corsheaders',  # CORS
    'rest_framework_simplejwt',  # JWT auth
    'rest_framework_simplejwt.token_blacklist',  # JWT token blacklist

    # Local apps
    'account.apps.AccountConfig',
    'store.apps.StoreConfig',
    'cart.apps.CartConfig',
    'checkout.apps.CheckoutConfig'
]

# =========================
# Middleware
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Enable CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
    # Custom middleware can be added here
]

ROOT_URLCONF = 'config.urls'

# =========================
# Templates
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Custom context processors 
                'store.context_processors.store_context',  
                'cart.context_processors.cart_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# =========================
# Database
# =========================
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        # 'USER': os.getenv('DB_USER'),
        # 'PASSWORD': os.getenv('DB_PASSWORD'),
        # 'HOST': os.getenv('DB_HOST'),
        # 'PORT': os.getenv('DB_PORT'),
    }
}
# =========================
# Password validation
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# Internationalization
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

# =========================
# Static & Media files
# =========================
STATIC_URL = 'static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Development static files

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Production collectstatic

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# =========================
# Authentication & JWT
# =========================
AUTH_USER_MODEL = "account.User"
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default
    'account.backends.AuthBackend',  # Email/Phone login
]


LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'

# =========================
# Email configuration
# =========================
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'

EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')

EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# =========================
# Default primary key
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# Celery configuration
# =========================
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = "Asia/Dhaka"
CELERY_ENABLE_UTC = False

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300
CELERY_TASK_SOFT_TIME_LIMIT = 240

# settings.py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}



# =========================
# Django REST Framework
# =========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # Token Authentication by default drf 
        # 'rest_framework.authentication.TokenAuthentication',
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

# ==========================
# Unfold Configuration
# ==========================

UNFOLD = {
    "SITE_TITLE": "EStore",
    "SITE_HEADER": "Dashboard",
    "SITE_SUBHEADER": "Admin",
    "SITE_SYMBOL": "account_circle",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "Development",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("img/logo.png"),
        "dark": lambda request: static("img/logo.png"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("img/logo.png"),
        "dark": lambda request: static("img/logo.png"),
    },
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
            "href": lambda request: static("img/logo.png"),
        },
    ],

}