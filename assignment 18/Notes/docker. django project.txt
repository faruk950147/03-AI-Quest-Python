# Django + Docker + PostgreSQL + Redis + Celery

## Complete Docker Notes

---

# 1. Project Structure

একটি সাধারণ Django + Docker project structure:

```text
myproject/
│
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── manage.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
└── .env
```

> `docker-compose.yml` এখনো কাজ করে, তবে modern Docker Compose-এ `compose.yaml` বা `compose.yml` ব্যবহার করা recommended।

---

# 2. requirements.txt

উদাহরণ:

```text
Django
psycopg[binary]
redis
celery
django-redis
```

যদি Django REST Framework ব্যবহার করো:

```text
djangorestframework
```

Production project-এ সাধারণত package version pin করা ভালো:

```text
Django==5.2.7
psycopg[binary]==3.2.10
redis==6.4.0
celery==5.5.3
django-redis==6.0.0
```

> Version example হিসেবে দেওয়া হয়েছে। নিজের project অনুযায়ী compatible version ব্যবহার করবে।

---

# 3. Dockerfile

```dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Explanation

### `FROM`

```dockerfile
FROM python:3.12-slim
```

Python-এর lightweight image ব্যবহার করছে।

---

### `ENV`

```dockerfile
ENV PYTHONUNBUFFERED=1
```

Python output buffer না করে সরাসরি logs-এ দেখাতে সাহায্য করে।

Docker environment-এ logging-এর জন্য এটি useful।

---

### `WORKDIR`

```dockerfile
WORKDIR /app
```

Container-এর ভিতরে working directory `/app`।

---

### `COPY`

```dockerfile
COPY requirements.txt .
```

প্রথমে শুধু `requirements.txt` copy করা হচ্ছে।

এরপর:

```dockerfile
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
```

Dependencies install করা হচ্ছে।

শেষে:

```dockerfile
COPY . .
```

Project-এর বাকি files container-এ copy করা হচ্ছে।

---

### `EXPOSE`

```dockerfile
EXPOSE 8000
```

Container-এর application port হিসেবে 8000 document করে।

---

### `CMD`

```dockerfile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Django development server চালায়।

---

# 4. Docker Compose

Django + PostgreSQL + Redis + Celery:

```yaml
services:

  web:
    build: .
    container_name: django-app
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:16
    container_name: postgres-db
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    restart: unless-stopped

  celery:
    build: .
    container_name: celery-worker
    command: celery -A myproject worker -l info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - redis
      - db
    restart: unless-stopped

volumes:
  postgres_data:
```

## Important

তোমার original command ছিল:

```yaml
command: celery -A config worker -l info
```

এখানে `config` যদি তোমার Django project package-এর নাম না হয়, তাহলে এটি কাজ করবে না।

যদি structure হয়:

```text
myproject/
    settings.py
    urls.py
```

তাহলে সাধারণত:

```bash
celery -A myproject worker -l info
```

ব্যবহার করবে।

---

# 5. `.env`

Database configuration:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=portfolio
DB_USER=postgres
DB_PASSWORD=admin
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### Important

`.env` সাধারণত Git-এ commit করা উচিত নয়।

`.gitignore`:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

# 6. Django Settings

`settings.py`:

```python
import os


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS",
        "localhost"
    ).split(",")
]
```

---

# 7. PostgreSQL Configuration

```python
DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "DB_ENGINE",
            "django.db.backends.postgresql",
        ),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
```

## Important Concept

Docker Compose-এর ভিতরে:

```text
DB_HOST=db
```

এখানে `db` হলো PostgreSQL service-এর নাম।

এজন্য Django container থেকে PostgreSQL-এ connect করতে:

```text
db:5432
```

ব্যবহার করবে।

`localhost:5432` ব্যবহার করবে না।

কারণ Django application container-এর ভিতরে `localhost` মানে Django container নিজেই।

---

# 8. Docker Network Concept

Compose automatically একটি network তৈরি করে।

```text
                  Docker Network
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
     web              db             redis
   Django          PostgreSQL        Redis
```

Django:

```text
db:5432
```

Redis:

```text
redis:6379
```

Celery:

```text
redis:6379
```

ব্যবহার করতে পারে।

---

# 9. Django + PostgreSQL Flow

```text
Browser
   │
   ▼
Django Container
   │
   │ PostgreSQL connection
   ▼
PostgreSQL Container
```

---

# 10. Django + Redis + Celery Architecture

```text
                    Browser
                       │
                       ▼
                ┌─────────────┐
                │    Django   │
                │     Web     │
                └──────┬──────┘
                       │
                       │ Task
                       ▼
                ┌─────────────┐
                │    Redis    │
                │   Broker    │
                └──────┬──────┘
                       │
                       │ Task
                       ▼
                ┌─────────────┐
                │    Celery   │
                │   Worker    │
                └──────┬──────┘
                       │
                       ▼
                Background Task
```

উদাহরণ:

```text
Django
   ↓
send_email.delay()
   ↓
Redis
   ↓
Celery Worker
   ↓
Email sent
```

---

# 11. Run Project — Step by Step

## Step 1 — Build

Modern Compose syntax:

```bash
docker compose build
```

---

## Step 2 — Start

```bash
docker compose up
```

Background-এ:

```bash
docker compose up -d
```

---

## Step 3 — Run Migration

```bash
docker compose exec web python manage.py migrate
```

এটি running `web` container-এর ভিতরে migration চালায়।

One-time container দিয়েও করা যায়:

```bash
docker compose run --rm web python manage.py migrate
```

### Difference

```bash
docker compose exec web ...
```

চলে running container-এর ভিতরে।

```bash
docker compose run --rm web ...
```

নতুন temporary container তৈরি করে command চালায়।

---

# 12. Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

তারপর:

```text
http://localhost:8000/admin/
```

এ গিয়ে Django admin access করা যাবে।

---

# 13. Stop Project

```bash
docker compose down
```

এতে containers এবং Compose-created network remove হবে।

PostgreSQL data থাকবে কারণ:

```yaml
volumes:
  postgres_data:
```

ব্যবহার করা হয়েছে।

---

# 14. Stop + Remove Volumes

```bash
docker compose down -v
```

⚠️ এটি PostgreSQL-এর persistent volume-ও remove করতে পারে।

অর্থাৎ database data হারাতে পারো।

Development environment-এও এই command ব্যবহার করার আগে সতর্ক থাকতে হবে।

---

# 15. Docker Image Commands

## Download Image

```bash
docker pull python
```

Specific version:

```bash
docker pull python:3.12
```

---

## List Images

```bash
docker images
```

অথবা:

```bash
docker image ls
```

---

## Delete Image

```bash
docker rmi image_id
```

অথবা:

```bash
docker rmi image_name
```

---

## Remove Unused Images

```bash
docker image prune
```

---

# 16. Container Commands

## Run Container

```bash
docker run python
```

---

## Interactive Container

```bash
docker run -it python
```

---

## Run with Port Mapping

```bash
docker run -p 8000:8000 django-app
```

Meaning:

```text
Host Port : Container Port
8000      : 8000
```

---

## Give Container a Name

```bash
docker run \
  -p 8000:8000 \
  --name django-container \
  django-app
```

---

# 17. List Containers

Running containers:

```bash
docker ps
```

All containers:

```bash
docker ps -a
```

---

# 18. Stop Container

By ID:

```bash
docker stop container_id
```

By name:

```bash
docker stop container_name
```

---

# 19. Restart Container

```bash
docker restart container_id
```

---

# 20. Remove Container

```bash
docker rm container_id
```

Running container remove করতে সাধারণত আগে stop করবে।

---

# 21. Remove Stopped Containers

```bash
docker container prune
```

---

# 22. Build Docker Image

```bash
docker build -t django-app .
```

এখানে:

```text
docker build     → image build command
-t django-app    → image name
.                → current directory as build context
```

---

## Version Tag

```bash
docker build -t django-app:v1 .
```

Image:

```text
django-app:v1
```

---

# 23. Docker Logs

```bash
docker logs container_id
```

Real-time logs:

```bash
docker logs -f container_id
```

---

# 24. Enter Container Shell

```bash
docker exec -it container_id bash
```

যদি `bash` না থাকে:

```bash
docker exec -it container_id sh
```

---

# 25. Docker Compose Commands

## Check Compose Version

```bash
docker compose version
```

---

## Start Services

```bash
docker compose up
```

---

## Detached Mode

```bash
docker compose up -d
```

---

## Build + Start

```bash
docker compose up --build
```

---

## Stop and Remove

```bash
docker compose down
```

---

## Restart

```bash
docker compose restart
```

---

## Check Status

```bash
docker compose ps
```

---

# 26. Docker Compose Logs

All services:

```bash
docker compose logs
```

Follow logs:

```bash
docker compose logs -f
```

Specific service:

```bash
docker compose logs web
```

Specific service + follow:

```bash
docker compose logs -f web
```

উদাহরণ:

```bash
docker compose logs -f celery
```

---

# 27. Execute Command Inside Compose Container

```bash
docker compose exec web bash
```

যদি bash না থাকে:

```bash
docker compose exec web sh
```

Django shell:

```bash
docker compose exec web python manage.py shell
```

Database migration:

```bash
docker compose exec web python manage.py migrate
```

---

# 28. Run One-Time Command

```bash
docker compose run --rm web python manage.py migrate
```

আরেকটি example:

```bash
docker compose run --rm web python manage.py createsuperuser
```

---

# 29. Build Images Only

```bash
docker compose build
```

---

# 30. Pull Images

```bash
docker compose pull
```

---

# 31. Start / Stop Specific Service

Start:

```bash
docker compose start web
```

Stop:

```bash
docker compose stop web
```

উদাহরণ:

```bash
docker compose stop celery
```

---

# 32. Remove Stopped Compose Containers

```bash
docker compose rm
```

---

# 33. Scale Service

```bash
docker compose up --scale web=3
```

এর মাধ্যমে একাধিক `web` container চালানো যায়।

তবে একই host port `8000:8000` সরাসরি multiple replicas-এর ক্ষেত্রে সমস্যা তৈরি করতে পারে।

Production scaling-এর জন্য সাধারণত reverse proxy/load balancer ব্যবহার করা হয়।

---

# 34. Validate Compose Configuration

```bash
docker compose config
```

এটি Compose configuration parse/resolve করতে সাহায্য করে।

---

# 35. View Processes

```bash
docker compose top
```

Running services-এর processes দেখতে ব্যবহার করা যায়।

---

# 36. Docker Network

List:

```bash
docker network ls
```

Create:

```bash
docker network create mynetwork
```

Inspect:

```bash
docker network inspect mynetwork
```

---

# 37. Docker Volume

List:

```bash
docker volume ls
```

Create:

```bash
docker volume create myvolume
```

Inspect:

```bash
docker volume inspect myvolume
```

---

# 38. Save Docker Image

```bash
docker save -o django-app.tar django-app
```

এতে image একটি `.tar` file হিসেবে save হবে।

---

# 39. Load Docker Image

```bash
docker load -i django-app.tar
```

অন্য machine-এ image import করার জন্য useful।

---

# 40. Docker Image Tag

ধরো:

```text
IMAGE ID = ac6ff836d5ff
```

তাহলে:

```bash
docker tag ac6ff836d5ff faruk950147/docker-test:latest
```

এখানে:

```text
ac6ff836d5ff
        ↓
IMAGE ID

faruk950147/docker-test
        ↓
Repository / image name

latest
        ↓
Tag
```

---

# 41. Docker Hub Push

প্রথমে Docker Hub-এ login:

```bash
docker login
```

তারপর:

```bash
docker push faruk950147/docker-test:latest
```

### Simple Reminder

```text
docker-test:latest
        │       │
        │       └── Tag
        │
        └────────── Image / Repository name
```

---

# 42. Docker System Cleanup

Basic cleanup:

```bash
docker system prune
```

More aggressive cleanup:

```bash
docker system prune -a
```

⚠️ `-a` ব্যবহার করলে unused images-সহ আরও resources remove হতে পারে। তাই command দেওয়ার আগে কী remove হবে বুঝে নেওয়া ভালো।

---

# 43. Django Docker Basic Flow

Simple Django application:

```bash
docker build -t django-app .
```

তারপর:

```bash
docker run -p 8000:8000 django-app
```

Flow:

```text
Dockerfile
    ↓
docker build
    ↓
Docker Image
    ↓
docker run
    ↓
Container
    ↓
Django
    ↓
localhost:8000
```

---

# 44. Complete Docker Compose Workflow

Development-এ একটি common workflow:

### Start

```bash
docker compose up -d --build
```

### Check status

```bash
docker compose ps
```

### Watch logs

```bash
docker compose logs -f
```

### Enter Django container

```bash
docker compose exec web bash
```

### Migration

```bash
docker compose exec web python manage.py migrate
```

### Create superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### Stop

```bash
docker compose down
```

---

# 45. Important Docker Commands — Quick Table

| Command               | কাজ                          |
| --------------------- | ---------------------------- |
| `docker --version`    | Docker version               |
| `docker info`         | Docker system information    |
| `docker pull`         | Image download               |
| `docker images`       | Images list                  |
| `docker build`        | Image build                  |
| `docker run`          | Container create/run         |
| `docker ps`           | Running containers           |
| `docker ps -a`        | All containers               |
| `docker stop`         | Stop container               |
| `docker start`        | Start stopped container      |
| `docker restart`      | Restart container            |
| `docker rm`           | Remove container             |
| `docker rmi`          | Remove image                 |
| `docker logs`         | Container logs               |
| `docker exec`         | Run command inside container |
| `docker volume ls`    | Volumes list                 |
| `docker network ls`   | Networks list                |
| `docker system prune` | Cleanup unused resources     |

---

# 46. Docker Compose — Quick Table

| Command                     | কাজ                         |
| --------------------------- | --------------------------- |
| `docker compose up`         | Services start              |
| `docker compose up -d`      | Background-এ start          |
| `docker compose up --build` | Build + start               |
| `docker compose down`       | Stop + remove services      |
| `docker compose down -v`    | Services + volumes remove   |
| `docker compose ps`         | Service status              |
| `docker compose logs`       | Logs                        |
| `docker compose logs -f`    | Real-time logs              |
| `docker compose exec`       | Running container-এ command |
| `docker compose run`        | One-time container command  |
| `docker compose build`      | Images build                |
| `docker compose pull`       | Images pull                 |
| `docker compose restart`    | Services restart            |
| `docker compose start`      | Stopped services start      |
| `docker compose stop`       | Services stop               |
| `docker compose config`     | Compose config inspect      |
| `docker compose top`        | Processes দেখায়             |

---

# 47. Important Docker Concepts

## Image

Image হলো application-এর packaged template।

```text
Image
  ↓
Container
```

একটি image থেকে multiple containers তৈরি করা যায়।

---

## Container

Container হলো image-এর running instance।

```text
Image
   ↓
Container
   ↓
Application Running
```

---

## Volume

Container delete হলেও data persist করার জন্য volume ব্যবহার করা হয়।

PostgreSQL:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

এখানে database data container-এর lifecycle-এর বাইরে persist করতে পারে।

---

## Network

একাধিক container-কে একে অপরের সাথে communicate করতে network ব্যবহৃত হয়।

Compose automatically service discovery দেয়।

যেমন:

```text
Django → db:5432
Django → redis:6379
Celery → redis:6379
```

---

# 48. Port Mapping

```yaml
ports:
  - "8000:8000"
```

মানে:

```text
Host                 Container
localhost:8000  →    8000
```

Browser:

```text
http://localhost:8000
```

Container-এর Django server:

```text
0.0.0.0:8000
```

---

# 49. `localhost` vs Service Name

Docker Compose-এ এটি খুব important।

ভুল ধারণা:

```text
Django → localhost:5432 → PostgreSQL
```

সাধারণত এটি কাজ করবে না।

সঠিক:

```text
Django → db:5432 → PostgreSQL
```

Redis-এর ক্ষেত্রে:

```text
Django → redis:6379
```

কারণ:

```text
db
redis
```

হলো Compose service names।

---

# 50. `depends_on` সম্পর্কে Important Note

```yaml
depends_on:
  - db
  - redis
```

এর অর্থ হলো Compose dependency অনুযায়ী service start করার order পরিচালনা করবে।

কিন্তু শুধু `depends_on` দিয়ে নিশ্চিত হওয়া যায় না যে PostgreSQL/Redis application-এর জন্য fully ready হয়ে গেছে।

Production বা robust setup-এ healthcheck এবং retry logic ব্যবহার করা ভালো।

---

# 51. Development vs Production

উপরের Dockerfile-এ:

```dockerfile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

এটি **development server**।

Production-এ সাধারণত Django `runserver` ব্যবহার করা হয় না।

সেখানে সাধারণত:

```text
Reverse Proxy
      ↓
Gunicorn / Uvicorn
      ↓
Django
```

ব্যবহার করা হয়।

যদি ASGI/async application হয়:

```text
Nginx / Reverse Proxy
        ↓
Uvicorn
        ↓
Django ASGI
```

এরকম architecture ব্যবহার করা যেতে পারে।

---

# 52. Production Architecture

একটি typical production architecture:

```text
                  Internet
                     │
                     ▼
              Reverse Proxy
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
      Django Web            Static/Media
          │
    ┌─────┼─────────┐
    │     │         │
    ▼     ▼         ▼
 PostgreSQL Redis   Celery
                    Worker
```

---

# 53. Security Checklist

Production-এ:

```env
DJANGO_DEBUG=False
```

ব্যবহার করা উচিত।

Secret key hard-code না করে environment variable ব্যবহার করা ভালো:

```env
DJANGO_SECRET_KEY=...
```

Database credentials-ও secret হিসেবে রাখা উচিত।

আর:

```text
.env
```

Git repository-তে commit করা উচিত নয়।

---

# 54. Most Important Mental Model

Docker-এর পুরো concept এভাবে মনে রাখো:

```text
Dockerfile
    ↓
docker build
    ↓
Image
    ↓
docker run / docker compose up
    ↓
Container
    ↓
Application
```

আর Docker Compose:

```text
compose.yaml
      │
      ├── web
      │
      ├── db
      │
      ├── redis
      │
      └── celery
```

একটি command:

```bash
docker compose up
```

দিয়ে পুরো multi-container application চালানো যায়।

---

# 55. Final Quick Revision

### Docker

```text
Dockerfile → Image → Container
```

### Compose

```text
compose.yaml → Multiple Services
```

### Django

```text
web container
```

### Database

```text
PostgreSQL → db:5432
```

### Cache / Broker

```text
Redis → redis:6379
```

### Background Task

```text
Django → Redis → Celery Worker
```

### Persistent Database

```text
PostgreSQL Container
        ↓
postgres_data Volume
```

### Most Used Commands

```bash
docker compose up -d
docker compose up -d --build
docker compose ps
docker compose logs -f
docker compose exec web bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose down
```

### One-line Memory Trick

```text
Build → Image
Run   → Container
Compose → Multiple Containers
Volume → Persistent Data
Network → Container Communication
Redis → Cache/Broker
Celery → Background Tasks
PostgreSQL → Database
```
