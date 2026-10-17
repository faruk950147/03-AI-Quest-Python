# Django + Docker + PostgreSQL + Redis + Celery — Complete Notes

## Table of Contents

1. Beginner Level
2. Intermediate Level
3. Advanced Level
4. Project Structure
5. Dockerfile
6. Docker Compose
7. Environment Variables
8. Django Settings
9. PostgreSQL
10. Redis
11. Celery
12. Database Migration
13. Docker Commands
14. Production Deployment
15. Security Best Practices
16. Troubleshooting
17. Quick Reference

---

# 1. Beginner Level

## 1.1 What is Django?

Django is a Python web framework used to build web applications, backend systems, and REST APIs.

Common use cases:

- Blog applications
- E-commerce websites
- Authentication systems
- REST APIs
- SaaS applications
- Admin dashboards

## 1.2 What is Docker?

Docker packages an application and its dependencies into containers.

Benefits:

- Consistent development environment
- Easy deployment
- Isolated services
- Reproducible builds
- Easier scaling

## 1.3 What is PostgreSQL?

PostgreSQL is a relational database management system.

Django uses it to store:

- Users
- Products
- Orders
- Payments
- Application data

## 1.4 What is Redis?

Redis is an in-memory data store.

Common uses:

- Caching
- Celery message broker
- Temporary data storage
- Rate limiting

## 1.5 What is Celery?

Celery executes background tasks outside the normal HTTP request-response cycle.

Examples:

- Sending emails
- Generating reports
- Processing uploaded files
- Scheduled jobs
- Notifications

## 1.6 How the Services Work Together

```text
Client
  |
  v
Django Application
  |
  +------ PostgreSQL
  |
  +------ Redis
             |
             v
          Celery Worker
```

Django handles HTTP requests. PostgreSQL stores persistent data. Redis can queue background tasks. Celery workers execute those tasks.

---

# 2. Intermediate Level

## 2.1 Recommended Project Structure

```text
django-docker-project/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── migrations/
│
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .env
└── manage.py
```

Create the project:

```bash
mkdir django-docker-project
cd django-docker-project

python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

Activate on Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install django djangorestframework psycopg[binary] redis celery
```

Create the Django project:

```bash
django-admin startproject config .
python manage.py startapp core
```

Save dependencies:

```bash
pip freeze > requirements.txt
```

For production, use a reviewed and pinned dependency list rather than blindly relying on an uncontrolled environment.

---

# 3. Requirements File

Example `requirements.txt`:

```text
Django
djangorestframework
psycopg[binary]
redis
celery
gunicorn
```

For a real deployment, pin tested package versions and update them deliberately.

---

# 4. Dockerfile

Create a file named `Dockerfile`:

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Explanation

- `FROM`: Selects the base image.
- `WORKDIR`: Sets the working directory.
- `ENV`: Configures Python behavior.
- `COPY`: Copies files into the image.
- `RUN`: Executes build-time commands.
- `EXPOSE`: Documents the intended application port.
- `CMD`: Starts the Django application using Gunicorn.

The build tools are included here for packages that may require compilation. Remove unnecessary packages when your dependencies do not need them.

---

# 5. Docker Ignore File

Create `.dockerignore`:

```text
venv/
.venv/
__pycache__/
*.py[cod]
.git/
.env
.pytest_cache/
.coverage
staticfiles/
media/
```

This prevents unnecessary files and secrets from entering the Docker build context.

---

# 6. Environment Variables

Create `.env`:

```dotenv
DEBUG=True
SECRET_KEY=replace-this-with-a-long-random-secret
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=replace-with-a-local-development-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
```

Important:

- Do not commit `.env` to Git.
- Use a unique, randomly generated secret key.
- Never reuse the example passwords in production.
- Production secrets should be injected through your deployment platform or a secret manager.

---

# 7. Django Settings

Update `config/settings.py`.

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "unsafe-development-key-change-me",
)

DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS",
        "localhost",
    ).split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "django_db"),
        "USER": os.environ.get("POSTGRES_USER", "django_user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REDIS_URL = os.environ.get(
    "REDIS_URL",
    "redis://localhost:6379/0",
)

CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER_URL",
    "redis://localhost:6379/1",
)

CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND",
    "redis://localhost:6379/2",
)
```

The fallback secret key is for local development only. Production startup should fail if a real secret key is missing.

---

# 8. Docker Compose

Create `compose.yaml`:

```yaml
services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 10

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 10

  celery:
    build: .
    command: celery -A config worker --loglevel=info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  postgres_data:
  redis_data:
```

This Compose configuration is intended for local development. The Django development server and bind-mounted source code should be replaced with a production-ready setup for deployment.

## Start the Services

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up --build -d
```

Check service status:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f web
docker compose logs -f db
docker compose logs -f redis
docker compose logs -f celery
```

Stop services:

```bash
docker compose down
```

Stop services and delete database/cache volumes:

```bash
docker compose down -v
```

Warning: `docker compose down -v` deletes the named volumes and their stored data. Do not use it when you need to preserve your database.

---

# 9. PostgreSQL

## 9.1 Database Connection

Inside Docker Compose, Django connects to:

```text
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

The hostname `db` is the Compose service name.

From a program running directly on your computer, the hostname is typically `localhost` if PostgreSQL has been published to a host port. The example Compose file does not publish the database port.

## 9.2 Run Migrations

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

## 9.3 Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

Open the admin panel:

```text
http://localhost:8000/admin/
```

## 9.4 Open PostgreSQL Shell

```bash
docker compose exec db psql \
  -U django_user \
  -d django_db
```

Useful SQL:

```sql
\l
\dt
SELECT * FROM django_migrations;
\q
```

Use the actual username and database configured in `.env`.

---

# 10. Redis

Redis is commonly used as a cache and Celery broker.

## 10.1 Redis CLI

```bash
docker compose exec redis redis-cli
```

Test Redis:

```text
PING
```

Expected result:

```text
PONG
```

Check server information:

```text
INFO
```

Exit:

```text
EXIT
```

## 10.2 Django Cache Example

Add to `config/settings.py`:

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 300,
    }
}
```

Example usage:

```python
from django.core.cache import cache

cache.set("welcome_message", "Hello Django", timeout=300)

message = cache.get("welcome_message")
print(message)
```

Redis cache data is temporary. Do not use it as the only storage for critical business records.

---

# 11. Celery Setup

## 11.1 Create `config/celery.py`

```python
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

## 11.2 Update `config/__init__.py`

```python
from .celery import app as celery_app

__all__ = ("celery_app",)
```

## 11.3 Create a Task

Create `core/tasks.py`:

```python
from celery import shared_task


@shared_task
def add_numbers(a, b):
    return a + b
```

## 11.4 Run a Task

Open a Django shell:

```bash
docker compose exec web python manage.py shell
```

Run:

```python
from core.tasks import add_numbers

result = add_numbers.delay(10, 20)
print(result.id)
```

The worker should process the task.

If you need to inspect the returned value, configure result storage and check the task state after completion:

```python
print(result.get(timeout=10))
```

Do not call `.get()` inside a web request if doing so would block the request unnecessarily.

## 11.5 Run Celery Worker Manually

```bash
docker compose exec web celery -A config worker --loglevel=info
```

Normally, the dedicated `celery` service in Compose runs this worker for you.

---

# 12. Intermediate Django API Example

Create a simple model in `core/models.py`:

```python
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

Create and apply migrations:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

Create `core/serializers.py`:

```python
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "created_at"]
```

Create `core/views.py`:

```python
from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

Create `core/urls.py`:

```python
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")

urlpatterns = router.urls
```

Update `config/urls.py`:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
]
```

Test the API:

```text
http://localhost:8000/api/products/
```

Important: Before using this API in production, configure authentication, permissions, validation, pagination, and appropriate access controls.

---

# 13. Advanced Level

## 13.1 Production Architecture

```text
Internet
   |
   v
Reverse Proxy / Load Balancer
   |
   v
Django + Gunicorn
   |
   +------ PostgreSQL
   |
   +------ Redis
              |
              v
          Celery Workers
```

A production deployment may also need:

- HTTPS/TLS
- Static and media file storage
- Database backups
- Monitoring and centralized logging
- Error tracking
- Health checks
- Resource limits
- Automated deployment
- Database connection management
- Separate worker scaling

## 13.2 Production Checklist

- Set `DEBUG=False`.
- Set `ALLOWED_HOSTS` correctly.
- Use a strong, private `SECRET_KEY`.
- Configure HTTPS and secure cookies.
- Configure trusted origins for CSRF where needed.
- Do not expose PostgreSQL or Redis publicly.
- Use non-root containers where practical.
- Keep images and Python packages updated.
- Back up PostgreSQL and test restoration.
- Use persistent storage where required.
- Configure logging and monitoring.
- Run `python manage.py check --deploy`.
- Run migrations as a controlled deployment step.
- Serve static files using a suitable production strategy.
- Use proper authentication and authorization.
- Add request timeouts, rate limits, and resource limits.

## 13.3 Example Production Environment

```dotenv
DEBUG=False
SECRET_KEY=inject-a-real-secret-through-your-secret-manager
ALLOWED_HOSTS=api.example.com

POSTGRES_DB=production_db
POSTGRES_USER=production_user
POSTGRES_PASSWORD=inject-a-strong-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
```

This is an example of variable names and configuration, not a complete production deployment. Use secret management, network restrictions, TLS where appropriate, and secure Redis/PostgreSQL configuration.

## 13.4 Gunicorn

A common Django production command is:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

Worker counts and timeouts should be tuned to the application's workload and available resources.

## 13.5 Celery Reliability

For reliable background processing:

- Make tasks idempotent when possible.
- Configure retries for transient failures.
- Set sensible task time limits.
- Monitor failed and stuck tasks.
- Keep tasks small and focused.
- Avoid passing large objects as task arguments.
- Pass database identifiers instead of full model objects.
- Consider broker persistence and result expiration.
- Plan how duplicate task execution will be handled.

Example:

```python
from celery import shared_task


@shared_task(
    bind=True,
    autoretry_for=(ConnectionError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_notification(self, user_id):
    # Load the user from the database.
    # Send the notification through your chosen provider.
    return {"user_id": user_id, "status": "processed"}
```

The task needs real application logic before it can send notifications. Retrying is suitable only when the operation and failure mode make retries safe.

## 13.6 Database Performance

Useful practices:

- Add indexes for frequently filtered columns.
- Use `select_related()` for foreign-key relationships.
- Use `prefetch_related()` for many-to-many and reverse relationships.
- Avoid N+1 query patterns.
- Paginate large querysets.
- Profile queries before optimizing.
- Use transactions for related writes.
- Monitor database connections and query latency.

Example:

```python
products = Product.objects.all().order_by("-created_at")
```

For larger datasets, add pagination at the API layer rather than returning every row at once.

---

# 14. Useful Docker Commands

Build images:

```bash
docker compose build
```

Start services:

```bash
docker compose up -d
```

Rebuild and start:

```bash
docker compose up --build -d
```

View running containers:

```bash
docker compose ps
```

Follow logs:

```bash
docker compose logs -f
```

Execute a command in Django:

```bash
docker compose exec web python manage.py check
```

Open a shell:

```bash
docker compose exec web bash
```

If Bash is not installed:

```bash
docker compose exec web sh
```

Stop services:

```bash
docker compose stop
```

Stop and remove containers and network:

```bash
docker compose down
```

Rebuild a service:

```bash
docker compose build web
```

Restart a service:

```bash
docker compose restart web
```

---

# 15. Troubleshooting

## Problem 1: Database Connection Refused

Possible causes:

- PostgreSQL is not ready.
- The hostname is incorrect.
- Credentials do not match.
- The database container failed.

Check:

```bash
docker compose ps
docker compose logs db
```

Inside Compose, use `db` as the hostname rather than `localhost`.

## Problem 2: Module Not Found

Check dependencies:

```bash
docker compose exec web pip list
```

Rebuild the image:

```bash
docker compose up --build -d
```

Verify the package exists in `requirements.txt`.

## Problem 3: Migration Required

Run:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

## Problem 4: Port Already in Use

Change the host-side port in Compose:

```yaml
ports:
  - "8001:8000"
```

Then open:

```text
http://localhost:8001/
```

The container still listens on port `8000`.

## Problem 5: Celery Tasks Are Not Running

Check worker logs:

```bash
docker compose logs -f celery
```

Check Redis:

```bash
docker compose exec redis redis-cli ping
```

Verify that the worker and Django use the same broker URL.

## Problem 6: Data Disappears

Verify that PostgreSQL uses a named volume:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

Do not remove the volume unless you intentionally want to delete its data. A volume is not a substitute for a backup.

---

# 16. Git Ignore

Create `.gitignore`:

```text
venv/
.venv/
__pycache__/
*.py[cod]
.env
.git/
.pytest_cache/
.coverage
staticfiles/
media/
```

Never commit passwords, private keys, or production secrets.

---

# 17. Quick Reference

| Task | Command |
|---|---|
| Start services | `docker compose up -d` |
| Build and start | `docker compose up --build -d` |
| View status | `docker compose ps` |
| View logs | `docker compose logs -f` |
| Django migrations | `docker compose exec web python manage.py migrate` |
| Create migrations | `docker compose exec web python manage.py makemigrations` |
| Create admin user | `docker compose exec web python manage.py createsuperuser` |
| Django checks | `docker compose exec web python manage.py check` |
| Django shell | `docker compose exec web python manage.py shell` |
| PostgreSQL shell | `docker compose exec db psql -U django_user -d django_db` |
| Redis CLI | `docker compose exec redis redis-cli` |
| Celery logs | `docker compose logs -f celery` |
| Stop services | `docker compose down` |

---

# 18. Learning Roadmap

## Beginner

- Learn Python fundamentals.
- Learn Django models, views, URLs, and templates.
- Learn basic SQL.
- Understand Docker images and containers.
- Run Django with PostgreSQL.

## Intermediate

- Build REST APIs with Django REST Framework.
- Learn authentication and permissions.
- Use Docker Compose.
- Add Redis caching.
- Add Celery background tasks.
- Learn migrations, indexes, and query optimization.
- Write tests.

## Advanced

- Build production Docker images.
- Use Gunicorn and a reverse proxy.
- Secure environment variables and services.
- Add CI/CD.
- Monitor logs and errors.
- Configure backups and recovery.
- Optimize database performance.
- Scale web and worker services independently.
- Learn deployment, observability, and reliability engineering.

---

# Final Notes

This guide provides a practical starting point for a Django backend stack using Docker, PostgreSQL, Redis, and Celery.

Before production deployment, review the exact configuration, pin dependency versions, configure secrets securely, test backups, and apply the security settings required by your hosting environment.
