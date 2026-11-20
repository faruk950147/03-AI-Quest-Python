# HTMX Complete Notes
## Beginner to Advanced | বাংলা Tutorial

---

# 1. What is HTMX?

HTMX হলো একটি lightweight JavaScript library, যার মাধ্যমে HTML attributes ব্যবহার করে AJAX requests, dynamic content updates এবং server interactions করা যায়।

সহজ ভাষায়:

HTMX ব্যবহার করে JavaScript না লিখেও ওয়েবসাইটের নির্দিষ্ট অংশ update করা যায়, পুরো page reload ছাড়াই।

### HTMX কেন ব্যবহার করব?

- Full page reload ছাড়াই content update করা যায়।
- JavaScript code কম লিখতে হয়।
- Backend-driven web application তৈরি করা সহজ।
- Django, Flask, FastAPI ইত্যাদির সঙ্গে ব্যবহার করা যায়।
- HTML দিয়েই AJAX request করা যায়।

### HTMX CDN

```html
<script src="https://unpkg.com/htmx.org@2.0.4"></script>
```

---

# 2. How HTMX Works

HTMX মূলত HTML attributes ব্যবহার করে server-এ HTTP request পাঠায়।

Workflow:

1. User button click করে।
2. HTMX HTTP request পাঠায়।
3. Backend request process করে।
4. Backend HTML response পাঠায়।
5. HTMX নির্দিষ্ট HTML element update করে।

Example:

```html
<button hx-get="/hello/" hx-target="#result">
    Click Me
</button>

<div id="result">
    Original Content
</div>
```

Django response:

```python
from django.http import HttpResponse

def hello(request):
    return HttpResponse("<h2>Hello from Django!</h2>")
```

Button click করলে `#result` element-এর content পরিবর্তন হবে।

---

# 3. Important HTMX Attributes

## 3.1 hx-get

GET request পাঠায়।

```html
<button hx-get="/users/">
    Load Users
</button>
```

## 3.2 hx-post

POST request পাঠায়।

```html
<button hx-post="/save/">
    Save Data
</button>
```

## 3.3 hx-put

PUT request পাঠায়।

```html
<button hx-put="/update/">
    Update
</button>
```

## 3.4 hx-patch

PATCH request পাঠায়।

```html
<button hx-patch="/update-name/">
    Update Name
</button>
```

## 3.5 hx-delete

DELETE request পাঠায়।

```html
<button hx-delete="/delete/">
    Delete
</button>
```

## 3.6 hx-target

Server response কোন HTML element-এ বসবে তা নির্ধারণ করে।

```html
<button hx-get="/users/" hx-target="#result">
    Load
</button>

<div id="result"></div>
```

## 3.7 hx-swap

কীভাবে response HTML-এর মধ্যে বসবে তা নির্ধারণ করে।

Important values:

| Value | কাজ |
|---|---|
| innerHTML | ভিতরের content replace |
| outerHTML | সম্পূর্ণ element replace |
| beforebegin | Element-এর আগে |
| afterbegin | Element-এর ভিতরে শুরুতে |
| beforeend | Element-এর ভিতরে শেষে |
| afterend | Element-এর পরে |
| delete | Target element delete |
| none | Response swap করবে না |

Example:

```html
<button
    hx-get="/message/"
    hx-target="#result"
    hx-swap="innerHTML">
    Load
</button>
```

## 3.8 hx-trigger

কখন request পাঠানো হবে তা নির্ধারণ করে।

```html
<button hx-get="/data/" hx-trigger="click">
    Load
</button>
```

অন্যান্য উদাহরণ:

```html
<input hx-get="/search/" hx-trigger="keyup">

<input hx-get="/search/" hx-trigger="change">

<div hx-get="/notifications/" hx-trigger="load"></div>
```

## 3.9 hx-indicator

Request চলাকালীন loading indicator দেখায়।

```html
<button hx-get="/data/" hx-indicator="#loading">
    Load Data
</button>

<span id="loading" class="htmx-indicator">
    Loading...
</span>
```

CSS:

```css
.htmx-indicator {
    display: none;
}

.htmx-request .htmx-indicator,
.htmx-request.htmx-indicator {
    display: inline;
}
```

## 3.10 hx-boost

সাধারণ link এবং form-কে AJAX navigation-এ রূপান্তর করতে পারে।

```html
<div hx-boost="true">
    <a href="/about/">About</a>
    <a href="/contact/">Contact</a>
</div>
```

## 3.11 hx-confirm

Action করার আগে confirmation নেয়।

```html
<button
    hx-delete="/delete/1/"
    hx-confirm="Are you sure?">
    Delete
</button>
```

## 3.12 hx-vals

Request-এর সঙ্গে অতিরিক্ত data পাঠায়।

```html
<button
    hx-post="/save/"
    hx-vals='{"name":"Faruk","role":"Developer"}'>
    Save
</button>
```

## 3.13 hx-include

অন্য input field-এর value request-এর সঙ্গে পাঠায়।

```html
<input id="username" name="username">

<button
    hx-post="/save/"
    hx-include="#username">
    Submit
</button>
```

## 3.14 hx-headers

Request-এর সঙ্গে অতিরিক্ত HTTP headers পাঠায়।

```html
<button
    hx-post="/api/"
    hx-headers='{"X-Custom-Header":"value"}'>
    Send
</button>
```

---

# 4. HTMX Request Methods

| HTTP Method | HTMX Attribute | Purpose |
|---|---|---|
| GET | hx-get | Data retrieve |
| POST | hx-post | Data create |
| PUT | hx-put | Data replace |
| PATCH | hx-patch | Partial update |
| DELETE | hx-delete | Data delete |

Example:

```html
<button hx-get="/users/">GET</button>
<button hx-post="/users/">POST</button>
<button hx-put="/users/1/">PUT</button>
<button hx-patch="/users/1/">PATCH</button>
<button hx-delete="/users/1/">DELETE</button>
```

---

# 5. HTMX with Django

Django এবং HTMX একসঙ্গে ব্যবহার করে dynamic application তৈরি করা যায়।

## Step 1: Install Django

```bash
pip install django
```

## Step 2: Create Project

```bash
django-admin startproject config
cd config
python manage.py startapp core
```

## Step 3: Configure settings.py

```python
INSTALLED_APPS = [
    # Existing apps
    "core",
]
```

## Step 4: Add HTMX CDN

base.html:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Django HTMX</title>
    <script src="https://unpkg.com/htmx.org@2.0.4"></script>
</head>
<body>

    {% block content %}
    {% endblock %}

</body>
</html>
```

## Step 5: Create Django View

core/views.py:

```python
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "home.html")

def hello(request):
    return HttpResponse("<h2>Hello from Django HTMX!</h2>")
```

## Step 6: Configure URLs

core/urls.py:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("hello/", views.hello, name="hello"),
]
```

config/urls.py:

```python
from django.urls import path, include

urlpatterns = [
    path("", include("core.urls")),
]
```

## Step 7: Create HTML Template

templates/home.html:

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://unpkg.com/htmx.org@2.0.4"></script>
</head>
<body>

    <h1>Django + HTMX</h1>

    <button
        hx-get="/hello/"
        hx-target="#result">
        Click Me
    </button>

    <div id="result">
        Result will appear here.
    </div>

</body>
</html>
```

Run:

```bash
python manage.py runserver
```

---

# 6. Django HTMX CRUD

CRUD মানে:

- Create
- Read
- Update
- Delete

## 6.1 Create Model

models.py:

```python
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 6.2 Create View

views.py:

```python
from django.shortcuts import render
from django.http import HttpResponse
from .models import Todo

def todo_list(request):
    todos = Todo.objects.all()
    return render(request, "todo/list.html", {
        "todos": todos
    })

def todo_create(request):
    if request.method == "POST":
        title = request.POST.get("title")

        if title:
            Todo.objects.create(title=title)

        todos = Todo.objects.all()

        return render(request, "todo/todo_items.html", {
            "todos": todos
        })

    return HttpResponse(status=405)
```

## 6.3 Create HTML

todo/list.html:

```html
<h1>Todo Application</h1>

<form
    hx-post="/todos/create/"
    hx-target="#todo-list"
    hx-swap="innerHTML">

    {% csrf_token %}

    <input
        type="text"
        name="title"
        placeholder="Enter todo">

    <button type="submit">
        Add Todo
    </button>
</form>

<div id="todo-list">
    {% include "todo/todo_items.html" %}
</div>
```

todo/todo_items.html:

```html
{% for todo in todos %}
    <div>
        {{ todo.title }}
    </div>
{% empty %}
    <p>No todos available.</p>
{% endfor %}
```

## 6.4 URLs

```python
from django.urls import path
from . import views

urlpatterns = [
    path("todos/", views.todo_list),
    path("todos/create/", views.todo_create),
]
```

এখন form submit করলে পুরো page reload হবে না।

---

# 7. HTMX Search System

HTMX দিয়ে live search তৈরি করা যায়।

HTML:

```html
<input
    type="text"
    name="q"
    placeholder="Search users..."
    hx-get="/search/"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#search-results">

<div id="search-results"></div>
```

Django View:

```python
from django.shortcuts import render
from .models import Todo

def search(request):
    query = request.GET.get("q", "")

    results = Todo.objects.filter(
        title__icontains=query
    )

    return render(request, "search_results.html", {
        "results": results
    })
```

search_results.html:

```html
{% for item in results %}
    <p>{{ item.title }}</p>
{% empty %}
    <p>No results found.</p>
{% endfor %}
```

এখানে:

- `keyup`: Keyboard event।
- `changed`: Value পরিবর্তন হলে।
- `delay:500ms`: 500 milliseconds অপেক্ষা করে request পাঠায়।

---

# 8. HTMX Form Validation

HTML:

```html
<form
    hx-post="/register/"
    hx-target="#form-result">

    {% csrf_token %}

    <input
        type="text"
        name="username"
        placeholder="Username">

    <input
        type="email"
        name="email"
        placeholder="Email">

    <button type="submit">
        Register
    </button>
</form>

<div id="form-result"></div>
```

Django:

```python
from django.shortcuts import render
from django.http import HttpResponse

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        if not username or not email:
            return HttpResponse(
                "<p>Please fill all fields.</p>",
                status=400
            )

        return HttpResponse(
            "<p>Registration successful!</p>"
        )

    return HttpResponse(status=405)
```

বাস্তব project-এ Django Forms ব্যবহার করে validation করা উত্তম।

---

# 9. HTMX Pagination

HTML:

```html
<div id="items">
    {% include "items.html" %}
</div>
```

Django View:

```python
from django.core.paginator import Paginator
from django.shortcuts import render

def item_list(request):
    paginator = Paginator(Item.objects.all(), 10)
    page = paginator.get_page(request.GET.get("page"))

    template = (
        "items.html"
        if request.headers.get("HX-Request")
        else "item_page.html"
    )

    return render(request, template, {
        "page": page
    })
```

Pagination template:

```html
{% for item in page %}
    <p>{{ item.name }}</p>
{% endfor %}

{% if page.has_next %}
    <button
        hx-get="?page={{ page.next_page_number }}"
        hx-target="#items"
        hx-swap="innerHTML">
        Next
    </button>
{% endif %}
```

---

# 10. HTMX Delete Operation

HTML:

```html
<div id="todo-{{ todo.id }}">
    {{ todo.title }}

    <button
        hx-delete="/todos/{{ todo.id }}/delete/"
        hx-target="#todo-{{ todo.id }}"
        hx-swap="outerHTML"
        hx-confirm="Are you sure?">
        Delete
    </button>
</div>
```

Django View:

```python
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Todo

def todo_delete(request, pk):
    if request.method != "DELETE":
        return HttpResponse(status=405)

    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()

    return HttpResponse("")
```

URL:

```python
path(
    "todos/<int:pk>/delete/",
    views.todo_delete
)
```

---

# 11. HTMX Loading Indicator

```html
<button
    hx-get="/load-data/"
    hx-target="#result"
    hx-indicator="#spinner">
    Load Data
</button>

<span id="spinner" class="htmx-indicator">
    Loading...
</span>

<div id="result"></div>
```

CSS:

```css
.htmx-indicator {
    display: none;
}

.htmx-request .htmx-indicator,
.htmx-request.htmx-indicator {
    display: inline-block;
}
```

---

# 12. HTMX Events

HTMX বিভিন্ন JavaScript events প্রদান করে।

Important events:

| Event | Purpose |
|---|---|
| htmx:configRequest | Request configuration |
| htmx:beforeRequest | Request পাঠানোর আগে |
| htmx:afterRequest | Request শেষ হলে |
| htmx:beforeSwap | Response swap হওয়ার আগে |
| htmx:afterSwap | Content swap হওয়ার পরে |
| htmx:responseError | HTTP error response |
| htmx:sendError | Network error |

Example:

```javascript
document.body.addEventListener(
    "htmx:afterRequest",
    function(event) {
        console.log("Request completed");
    }
);
```

---

# 13. HTMX with Django REST Framework

HTMX শুধু Django Template-এর সঙ্গে নয়, API backend-এর সঙ্গেও কাজ করতে পারে।

তবে HTMX সাধারণত HTML response নিয়ে কাজ করার জন্য বেশি উপযোগী।

Django REST Framework:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def user_api(request):
    return Response({
        "name": "Faruk",
        "role": "Backend Developer"
    })
```

এই API JSON response পাঠাবে।

HTMX-এর HTML swap workflow-এর জন্য Django view থেকে HTML partial response পাঠানো সাধারণত সহজ।

---

# 14. HTMX Security

Security খুব গুরুত্বপূর্ণ।

### 1. CSRF Protection

Django POST request:

```html
<form hx-post="/save/">
    {% csrf_token %}

    <input name="title">

    <button type="submit">
        Save
    </button>
</form>
```

### 2. Authentication

Backend-এ user authentication নিশ্চিত করতে হবে।

### 3. Authorization

প্রতিটি update এবং delete request-এ permission check করতে হবে।

### 4. Input Validation

User input কখনো সরাসরি trust করা যাবে না।

### 5. SQL Injection

Django ORM ব্যবহার করো এবং raw SQL ব্যবহার করলে parameterized query ব্যবহার করো।

---

# 15. HTMX vs React vs JavaScript

| Feature | HTMX | JavaScript | React |
|---|---|---|---|
| Learning curve | Easy | Medium | Medium/Hard |
| AJAX | Built-in | Fetch API | Fetch/API |
| DOM updates | Built-in | Manual | Automatic |
| Backend integration | Excellent | Flexible | API-based |
| SPA support | Limited | Possible | Excellent |
| HTML rendering | Server-friendly | Flexible | Client-side |
| Best for | Server-driven UI | General purpose | Complex frontend |

### কখন HTMX ব্যবহার করবে?

- Django-based applications
- Admin dashboards
- CRUD applications
- Dynamic forms
- Server-rendered applications
- Search and filtering

### কখন React ব্যবহার করবে?

- Complex frontend state
- Large SPA
- Highly interactive interfaces
- Complex client-side applications

---

# 16. HTMX Best Practices

1. Backend থেকে প্রয়োজন অনুযায়ী HTML partial return করো।
2. অপ্রয়োজনীয় request কমাও।
3. Search input-এ debounce ব্যবহার করো।
4. Form validation backend-এ করো।
5. CSRF protection নিশ্চিত করো।
6. Authentication এবং authorization বজায় রাখো।
7. Loading indicator ব্যবহার করো।
8. Error handling implement করো।
9. HTML response ছোট ও maintainable রাখো।
10. Reusable Django template partial তৈরি করো।

---

# 17. HTMX Learning Roadmap

## Beginner

- HTMX Introduction
- CDN Setup
- hx-get
- hx-post
- hx-target
- hx-swap
- hx-trigger

## Intermediate

- Django Integration
- Dynamic Search
- Form Submission
- Form Validation
- CRUD Application
- Pagination
- Loading Indicators

## Advanced

- HTMX Events
- hx-boost
- hx-vals
- hx-include
- hx-headers
- Authentication
- Authorization
- Security
- Performance Optimization
- Production Deployment

---

# 18. Practice Projects

| Level | Project |
|---|---|
| Beginner | Dynamic Greeting App |
| Beginner | Live Search |
| Beginner | Dynamic Counter |
| Intermediate | Todo Application |
| Intermediate | Student Management |
| Intermediate | Dynamic CRUD Dashboard |
| Intermediate | Product Filtering |
| Advanced | Blog Application |
| Advanced | E-commerce Dashboard |
| Advanced | Real-time Notification UI |

---

# 19. Important Interview Questions

### Q1. What is HTMX?

HTMX is a JavaScript library that allows developers to access AJAX, CSS transitions, and other modern browser features directly from HTML attributes.

### Q2. What is hx-get?

It sends an HTTP GET request to a specified URL.

### Q3. What is hx-post?

It sends an HTTP POST request to a specified URL.

### Q4. What is hx-target?

It specifies the HTML element where the server response should be inserted.

### Q5. What is hx-swap?

It controls how the server response is swapped into the target element.

### Q6. What is hx-trigger?

It specifies which event triggers an HTMX request.

### Q7. Can HTMX work with Django?

Yes. HTMX works very well with Django templates and views.

### Q8. Does HTMX require React?

No. HTMX can create many interactive interfaces without React.

### Q9. Does HTMX replace JavaScript?

No. HTMX reduces the need for custom JavaScript in many server-driven applications, but JavaScript is still useful.

### Q10. What is an HTML partial?

An HTML partial is a reusable portion of an HTML page returned independently by the backend.

---

# 20. Official Resources

- HTMX Official Website: https://htmx.org/
- HTMX Documentation: https://htmx.org/docs/
- HTMX Examples: https://htmx.org/examples/
- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/

---

# Final Summary

HTMX হলো একটি powerful tool যা HTML attributes ব্যবহার করে dynamic web applications তৈরি করতে সাহায্য করে।

Python Django Developer হিসেবে নিচের combination শেখা কার্যকর:

- Python
- Django
- Django ORM
- Django REST Framework
- HTMX
- PostgreSQL
- HTML
- CSS
- Basic JavaScript

**Recommended Stack:**

Django + HTMX + PostgreSQL + Tailwind CSS

এটি দিয়ে modern, fast এবং server-driven web applications তৈরি করা সম্ভব।
