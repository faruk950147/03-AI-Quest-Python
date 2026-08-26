import os
from pathlib import Path
from dotenv import load_dotenv
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

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
    # Local apps
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
WSGI_APPLICATION = 'config.wsgi.application'


# ========================
# Database
# =========================
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME'),
        # 'USER': os.environ.get('DB_USER', 'root'),
        # 'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        # 'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        # 'PORT': os.environ.get('DB_PORT', '3306'),
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


# =========================
# Static files 
# =========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

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