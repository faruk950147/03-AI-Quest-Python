# Django + Nginx Full Notes
## Bangla | WSL Ubuntu | Python Backend Development

---

## 1. Django কী?

Django হলো Python-এর একটি web framework। এটি দিয়ে website, backend application এবং REST API তৈরি করা যায়।

প্রধান বিষয়:
- Models
- Views
- URLs
- Templates
- ORM
- Authentication
- Django Admin
- Django REST Framework (DRF)

## 2. Nginx কী?

Nginx হলো একটি web server এবং reverse proxy।

প্রধান কাজ:
- HTTP request গ্রহণ করা
- Django application-এ request forward করা
- Static files পরিবেশন করা
- HTTPS/TLS পরিচালনা করা
- Reverse proxy হিসেবে কাজ করা

## 3. Architecture

Browser → Nginx → Gunicorn → Django → Database

- Browser: Request পাঠায়।
- Nginx: Request গ্রহণ করে।
- Gunicorn: Django WSGI application চালায়।
- Django: Business logic ও API response তৈরি করে।
- Database: Data সংরক্ষণ করে।

## 4. WSL Ubuntu setup

### Update packages

```bash
sudo apt update
sudo apt upgrade -y
```

### Install packages

```bash
sudo apt install python3 python3-venv python3-pip nginx curl git -y
```

### Check versions

```bash
python3 --version
pip3 --version
nginx -v
git --version
```

## 5. Linux commands

```bash
pwd
ls -la
cd ~
mkdir practice
cd practice
whoami
```

- `pwd`: বর্তমান directory।
- `ls -la`: ফাইল ও hidden files।
- `cd ~`: Home directory।
- `mkdir`: Directory তৈরি।
- `whoami`: বর্তমান username।

## 6. Django project তৈরি

```bash
mkdir -p ~/django-nginx-demo
cd ~/django-nginx-demo

python3 -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
pip install django djangorestframework gunicorn

django-admin startproject config .
python manage.py migrate
```

## 7. Django project structure

```text
django-nginx-demo/
├── venv/
├── manage.py
└── config/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

- `manage.py`: Django management commands।
- `settings.py`: Project settings।
- `urls.py`: URL routing।
- `wsgi.py`: Gunicorn-এর WSGI entry point।
- `asgi.py`: ASGI application entry point।
- `venv/`: Virtual environment।

## 8. Django development server

```bash
cd ~/django-nginx-demo
source venv/bin/activate
python manage.py runserver 127.0.0.1:8000
```

Browser:

http://127.0.0.1:8000

বন্ধ করতে `Ctrl+C` চাপুন।

নোট: `runserver` শুধু development ও testing-এর জন্য।

## 9. Django REST Framework API তৈরি

### Install DRF

```bash
pip install djangorestframework
```

### Add apps to config/settings.py

বিদ্যমান `INSTALLED_APPS`-এ যোগ করুন:

```python
'rest_framework',
'api',
```

### Create app

```bash
python manage.py startapp api
```

### api/views.py

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def home_api(request):
    return Response({
        "message": "Django API is running!",
        "status": "success"
    })
```

### Create api/urls.py

```python
from django.urls import path
from .views import home_api

urlpatterns = [
    path("", home_api, name="home-api"),
]
```

### config/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
```

### Test API

```bash
python manage.py check
python manage.py runserver 127.0.0.1:8000
```

Browser:

http://127.0.0.1:8000/api/

Expected response:

```json
{
  "message": "Django API is running!",
  "status": "success"
}
```

## 10. Gunicorn setup

Gunicorn হলো Python WSGI application server।

```bash
cd ~/django-nginx-demo
source venv/bin/activate
gunicorn --workers 3 --bind 127.0.0.1:8000 config.wsgi:application
```

Test from another terminal:

```bash
curl http://127.0.0.1:8000/api/
```

Gunicorn বন্ধ করতে `Ctrl+C` চাপুন।

নোট: Django development server এবং Gunicorn একই port-এ একসঙ্গে চালাবেন না।

## 11. Nginx installation

```bash
sudo apt update
sudo apt install nginx -y
sudo service nginx start
sudo service nginx status
```

Nginx version:

```bash
nginx -v
```

## 12. Nginx configuration

Configuration file তৈরি করুন:

```bash
sudo nano /etc/nginx/sites-available/django-demo
```

এই configuration paste করুন:

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Save: `Ctrl+O` → `Enter` → `Ctrl+X`।

## 13. Enable Nginx site

```bash
sudo ln -sf /etc/nginx/sites-available/django-demo /etc/nginx/sites-enabled/django-demo
```

Default site সরাতে:

```bash
sudo rm -f /etc/nginx/sites-enabled/default
```

Configuration test:

```bash
sudo nginx -t
```

Restart:

```bash
sudo service nginx restart
```

## 14. End-to-end test

প্রথমে Gunicorn চালু করুন:

```bash
cd ~/django-nginx-demo
source venv/bin/activate
gunicorn --bind 127.0.0.1:8000 config.wsgi:application
```

Browser:

- http://localhost/
- http://localhost/api/
- http://localhost/admin/

API test:

```bash
curl http://localhost/api/
```

এখন request flow:

Browser → Nginx port 80 → Gunicorn port 8000 → Django API

## 15. Static files

config/settings.py-তে:

```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

বিদ্যমান settings থাকলে duplicate করবেন না।

Static files সংগ্রহ করুন:

```bash
python manage.py collectstatic --noinput
```

Nginx configuration-এ যোগ করুন:

```nginx
location /static/ {
    alias /home/omar-faruk/django-nginx-demo/staticfiles/;
}
```

`/home/omar-faruk/` path আপনার প্রকৃত Linux username অনুযায়ী পরিবর্তন করুন।

তারপর:

```bash
sudo nginx -t
sudo service nginx reload
```

## 16. Important Nginx commands

```bash
sudo nginx -t
sudo service nginx start
sudo service nginx stop
sudo service nginx restart
sudo service nginx reload
sudo service nginx status
```

## 17. Logs

Nginx error log:

```bash
sudo tail -n 50 /var/log/nginx/error.log
```

Access log:

```bash
sudo tail -n 50 /var/log/nginx/access.log
```

Live error log:

```bash
sudo tail -f /var/log/nginx/error.log
```

বন্ধ করতে `Ctrl+C` চাপুন।

## 18. Common errors

### 502 Bad Gateway

কারণ: Gunicorn বন্ধ বা ভুল port।

```bash
curl http://127.0.0.1:8000/api/
```

Gunicorn চালু করুন।

### DisallowedHost

`config/settings.py`-তে local testing-এর জন্য:

```python
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
```

### Nginx configuration error

```bash
sudo nginx -t
```

Error message দেখে configuration ঠিক করুন।

### Port already in use

```bash
sudo ss -ltnp | grep ':8000'
```

Port ব্যবহার করছে কোন process, সেটি শনাক্ত করুন।

## 19. Production security

Production deployment-এর আগে:

- `DEBUG = False`
- নিরাপদ `SECRET_KEY`
- সঠিক `ALLOWED_HOSTS`
- HTTPS/TLS
- Gunicorn service management
- PostgreSQL configuration
- Static ও media file handling
- Database backups
- Logs ও monitoring
- Firewall configuration

Secret key source code বা public GitHub repository-তে রাখবেন না।

Deployment check:

```bash
python manage.py check --deploy
```

Official documentation:

- Django: https://docs.djangoproject.com/en/6.0/howto/deployment/
- Django REST Framework: https://www.django-rest-framework.org/
- Nginx: https://nginx.org/en/docs/
- Gunicorn: https://docs.gunicorn.org/

## 20. Final quick commands

```bash
# Enter project
cd ~/django-nginx-demo

# Activate virtual environment
source venv/bin/activate

# Database migrations
python manage.py migrate

# Check project
python manage.py check

# Start Django development server
python manage.py runserver 127.0.0.1:8000

# Start Gunicorn
gunicorn --bind 127.0.0.1:8000 config.wsgi:application

# Test API directly
curl http://127.0.0.1:8000/api/

# Test API through Nginx
curl http://localhost/api/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo service nginx restart

# Check status
sudo service nginx status
```

## Learning roadmap

1. Linux ও WSL fundamentals
2. Python virtual environment ও package management
3. Django project, app, models, views ও URLs
4. Django REST Framework ও authentication
5. Gunicorn ও WSGI
6. Nginx reverse proxy ও static files
7. PostgreSQL ও database migration
8. HTTPS, security ও production deployment
