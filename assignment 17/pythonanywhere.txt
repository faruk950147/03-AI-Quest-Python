# PythonAnywhere-এ Django Project Deploy করার ধাপ

## 1. Project Folder-এ প্রবেশ করুন

PythonAnywhere-এর **Bash Console** খুলে project directory-তে যান:

```bash
cd ~/devlopyment-3
```

---

## 2. Virtual Environment তৈরি ও Activate করুন

Virtual environment তৈরি করুন:

```bash
python3 -m venv venv
```

তারপর activate করুন:

```bash
source venv/bin/activate
```

Activate হওয়ার পর সাধারণত terminal-এ `(venv)` দেখা যাবে।

---

## 3. Required Packages ইনস্টল করুন

যদি `requirements.txt` থাকে:

```bash
pip install -r requirements.txt
```

যদি `requirements.txt` না থাকে, প্রয়োজনীয় package manually install করুন। যেমন:

```bash
pip install django
```

Deployment-এর আগে `requirements.txt` তৈরি করে রাখা ভালো:

```bash
pip freeze > requirements.txt
```

---

# 4. PythonAnywhere Web Tab Setup

PythonAnywhere Dashboard থেকে:

**Web → Add a new web app**

এ যান এবং আপনার project অনুযায়ী Web App তৈরি করুন।

### Code Section

**Source code:**

```text
/home/YOUR_USERNAME/devlopyment-3
```

**Working directory:**

```text
/home/YOUR_USERNAME/devlopyment-3
```

> `YOUR_USERNAME`-এর জায়গায় আপনার PythonAnywhere username বসাবেন।

### Virtualenv Section

Virtualenv path দিন:

```text
/home/YOUR_USERNAME/devlopyment-3/venv
```

---

# 5. Static Files Setup

PythonAnywhere-এর **Static files** section-এ আপনার Django project-এর static/media configuration অনুযায়ী mapping দিন।

| URL        | Directory                                  |
| ---------- | ------------------------------------------ |
| `/static/` | `/home/YOUR_USERNAME/devlopyment-3/static` |
| `/media/`  | `/home/YOUR_USERNAME/devlopyment-3/media`  |

যদি `STATIC_ROOT` হিসেবে `staticfiles` ব্যবহার করেন, তাহলে আগে:

```bash
python manage.py collectstatic
```

চালান।

তারপর `staticfiles` directory-এর mapping প্রয়োজন হলে:

```text
/static/ → /home/YOUR_USERNAME/devlopyment-3/staticfiles
```

**একই `/static/` URL-এর জন্য `static` এবং `staticfiles` দুটো mapping একসাথে ব্যবহার করবেন না।** সাধারণত production-এ `STATIC_ROOT` হিসেবে `staticfiles` ব্যবহার করে সেটিকেই `/static/` হিসেবে map করা হয়।

---

# 6. Django WSGI Configuration

PythonAnywhere-এর **Web** tab থেকে:

**WSGI configuration file** লিঙ্কে ক্লিক করুন।

Django project-এর WSGI file সাধারণত এমন হয়:

```text
/home/YOUR_USERNAME/devlopyment-3/project_name/wsgi.py
```

এখানে `project_name`-এর জায়গায় আপনার Django project's folder name বসবে।

WSGI configuration-এ project path এবং Django settings module সঠিকভাবে সেট করতে হবে।

উদাহরণ:

```
import os
import sys
from django.core.wsgi import get_wsgi_application

path = '/home/faruk950147/devlopyment-3'

if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

application = get_wsgi_application()
```

---

# 7. Django Settings Check করুন

`settings.py`-তে production deployment-এর জন্য প্রয়োজনীয় configuration ঠিক আছে কিনা দেখুন।

উদাহরণ:

```python
ALLOWED_HOSTS = [
    'YOUR_USERNAME.pythonanywhere.com',
]
```

Static configuration:

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Media ব্যবহার করলে:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

# 8. Database Migration করুন

Virtual environment activate থাকা অবস্থায়:

```bash
python manage.py migrate
```

তারপর static files collect করুন:

```bash
python manage.py collectstatic
```

---

# 9. Final Step — Reload

সব configuration ঠিক করার পর PythonAnywhere-এর:

**Web → Reload**

সবুজ **Reload** button-এ ক্লিক করুন।

তারপর আপনার website-এর URL-এ গিয়ে project check করুন:

```text
https://YOUR_USERNAME.pythonanywhere.com/
```

## Quick Checklist

* [ ] Project path সঠিক
* [ ] Virtual environment তৈরি হয়েছে
* [ ] Virtual environment activate হয়েছে
* [ ] `requirements.txt` install হয়েছে
* [ ] `ALLOWED_HOSTS` ঠিক আছে
* [ ] WSGI configuration ঠিক আছে
* [ ] `DJANGO_SETTINGS_MODULE` ঠিক আছে
* [ ] `migrate` চালানো হয়েছে
* [ ] `collectstatic` চালানো হয়েছে
* [ ] Static/Media mapping ঠিক আছে
* [ ] Web App Reload করা হয়েছে

Developed the portfolio website using Django with a structured and maintainable backend.
Implemented Django REST Framework (DRF) for RESTful API development.
Integrated JWT authentication using Simple JWT for secure API authentication.
Used MySQL for database management and Django ORM for database operations.
Integrated Redis and Celery for background task processing.
Implemented Django Channels and ASGI support for asynchronous functionality.
Added CKEditor for rich-text content management and Django Unfold for an enhanced admin interface.
Implemented CORS handling and environment variable management using python-dotenv.
Configured production-related tools including WhiteNoise for static files.

DB_ENGINE=django.db.backends.mysql
DB_NAME=faruk950147$dbms
DB_USER=faruk950147
DB_PASSWORD=iloved950147
DB_HOST=faruk950147.mysql.pythonanywhere-services.com
DB_PORT=3306

# Django secret key
SECRET_KEY=django-insecure-*9_(^diffqh45ol_^c5)x6ssscvngn3927%(r7=dkkith@7snxa)

# Debug mode
DEBUG=True
ALLOWED_HOSTS=faruk950147.pythonanywhere.com
BASE_URL=faruk950147.pythonanywhere.com

# ================= EMAIL =================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_USE_TLS=True
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=md.omarfaruk950147@gmail.com
EMAIL_HOST_PASSWORD=lqsd vtui jcxf mfqm
EMAIL_PORT=587


