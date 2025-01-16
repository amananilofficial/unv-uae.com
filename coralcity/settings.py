from django.contrib.messages import constants as messages
import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
# Replace with a secure, randomly generated key
SECRET_KEY = "%07dn)!zj+*7))o7ra2#t^i+p5i59qr1q^d@fm81d_dio%p2d$"
DEBUG = True  # Set to True for development, False for production
ALLOWED_HOSTS = ['unv-uae.com', 'www.unv-uae.com', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'jazzmin',  # Admin customization
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages.apps.PagesConfig',
    'products.apps.ProductsConfig',
    'contacts.apps.ContactsConfig',
    'django.contrib.humanize',
    'graphene_django',
    'django.contrib.sitemaps',  # Added for sitemap generation
    'django.contrib.sites',  # For site-based settings
    'robots',
    'import_export',
    'phonenumber_field',
    'django_redis',
    'django_extensions',
    'django_htmx',
    'django_browser_reload',
    'meta',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'coralcity.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'coralcity.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),  # Convert Path to string
    }
}

# Only use dj_database_url in production
if not DEBUG and 'DATABASE_URL' in os.environ:
    db_from_env = dj_database_url.config(conn_max_age=600)
    DATABASES['default'].update(db_from_env)

# Caching configuration (using Redis)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # Update with your Redis server details
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Adjust this path as necessary
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise configuration for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Cache and session settings
CACHE_TTL = 60 * 15  # 15 minutes
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Authentication password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Security headers
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
X_CONTENT_TYPE_OPTIONS = 'nosniff'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Cron job settings
CRONJOBS = [
    ('0 0 * * *', 'contacts.cron.ExportToGoogleSheetsCronJob'),
    ('0 0 * * *', 'products.cron.ExportToGoogleSheetsCronJob'),
]

# Sitemap settings
SITE_ID = 1
SITEMAP_LIMIT = 50000

# Robots.txt settings
ROBOTS_USE_HOST = False
ROBOTS_USE_SITEMAP = True

# SEO metadata
META_SITE_PROTOCOL = 'https'
META_SITE_DOMAIN = 'unv-uae.com'
META_DEFAULT_KEYWORDS = ['your', 'default', 'keywords']
META_INCLUDE_KEYWORDS = True
META_DEFAULT_DESCRIPTION = 'Explore the vibrant city of Coral City, where the ocean meets the sky and the beauty of nature is intertwined with the charm of urban life.'
META_IMAGE_URL = f"{META_SITE_PROTOCOL}://{META_SITE_DOMAIN}/static/images/logo/logo.png"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Temporarily disable security settings for development
if DEBUG:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

# Add message tags for proper styling
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
