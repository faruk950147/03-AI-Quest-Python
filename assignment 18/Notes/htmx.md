# Django HTMX – Complete Notes (বাংলায়)

## Table of Contents

1. What is HTMX?
2. Django vs Django + HTMX
3. Installation
4. Django Configuration
5. What is request.htmx?
6. HTMX Workflow
7. Important HTMX Attributes
8. Django HTMX Template Tags
9. Practical Project – Live Search
10. Django HTMX CRUD
11. Advanced django-htmx Features
12. Advanced HTMX Attributes
13. Best Practices
14. Common Errors & Solutions
15. Interview Questions & Answers
16. Practical Project Ideas
17. Learning Roadmap
18. Official Documentation

---

# 1. What is HTMX?

HTMX is a JavaScript library that allows developers to create dynamic and interactive web applications using HTML attributes.

It allows HTML elements to make HTTP requests directly to the server and update specific parts of a webpage without reloading the entire page.

### Main Features

- AJAX requests without writing custom JavaScript.
- Dynamic HTML updates.
- Live search.
- Dynamic form submission.
- Delete without page reload.
- Dynamic pagination.
- Infinite scrolling.
- Modal popup.
- Dynamic filtering.
- Server-side rendering.

### Django vs Django + HTMX

| Traditional Django | Django + HTMX |
|---|---|
| Full page reload | Partial page update |
| More JavaScript may be needed | HTML attributes handle interactions |
| AJAX manually implemented | AJAX becomes easier |
| Full template response | Partial template response |

# 2. Installation

### Step 1: Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Step 2: Install django-htmx

```bash
pip install django-htmx
```

### Step 3: Verify Installation

```bash
pip show django-htmx
```

### Step 4: Install HTMX JavaScript

Add HTMX to your Django base template:

```html
<script src="https://unpkg.com/htmx.org@2.0.4"></script>
```

### Important Difference

There are two separate components:

1. `django-htmx`: Python package for Django integration.
2. `htmx`: JavaScript library for browser-side interactions.

# 3. Django Project Configuration

Create Django project:

```bash
django-admin startproject config

cd config

python manage.py startapp core
```

### settings.py

Add applications:

```python
INSTALLED_APPS = [
    # Default Django apps

    "django_htmx",
    "core",
]
```

Add middleware:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    "django_htmx.middleware.HtmxMiddleware",

    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
```

### Why HtmxMiddleware?

`HtmxMiddleware` attaches an `htmx` object to Django's request object.

After configuring middleware, you can access:

```python
request.htmx
```

# 4. What is request.htmx?

`request.htmx` is one of the most important features of django-htmx.

It helps determine whether an incoming request was made by HTMX.

### Example

```python
from django.shortcuts import render

def home(request):

    if request.htmx:
        return render(
            request,
            "partials/content.html"
        )

    return render(
        request,
        "home.html"
    )
```

### Explanation

- `request.htmx` returns an HTMX-specific object when the request contains the appropriate HTMX header.
- It returns `None` when the request is not an HTMX request.
- You can use it to return full pages or partial HTML.

### Important Properties

```python
request.htmx.boosted

request.htmx.current_url

request.htmx.history_restore_request

request.htmx.prompt

request.htmx.target

request.htmx.trigger

request.htmx.trigger_name
```

### Example

```python
def dashboard(request):

    if request.htmx:
        print("HTMX Request")

        print(request.htmx.target)
        print(request.htmx.trigger)

    return render(request, "dashboard.html")
```

# 5. How HTMX Works

HTMX workflow:

1. User performs an action.
2. HTMX sends an HTTP request.
3. Django receives the request.
4. Django executes business logic.
5. Django returns HTML.
6. HTMX updates the targeted HTML element.

### Workflow Diagram

```text
User Action
    |
    v
HTMX Request
    |
    v
Django View
    |
    v
Business Logic
    |
    v
Database Query
    |
    v
HTML Response
    |
    v
HTMX DOM Update
```

# 6. Important HTMX Attributes

| Attribute | Description |
|---|---|
| hx-get | Sends GET request |
| hx-post | Sends POST request |
| hx-put | Sends PUT request |
| hx-patch | Sends PATCH request |
| hx-delete | Sends DELETE request |
| hx-target | Selects target element |
| hx-swap | Controls HTML replacement |
| hx-trigger | Defines request trigger |
| hx-select | Selects response HTML |
| hx-indicator | Shows loading indicator |
| hx-confirm | Shows confirmation popup |
| hx-vals | Sends additional values |
| hx-include | Includes other input values |
| hx-headers | Sends custom headers |
| hx-push-url | Updates browser history |
| hx-boost | Converts links/forms into HTMX requests |
| hx-sync | Synchronizes requests |
| hx-disabled-elt | Disables elements during requests |
| hx-swap-oob | Updates elements outside the main target |

## 6.1 hx-get

Sends an HTTP GET request.

HTML:

```html
<button hx-get="/hello/">
    Click Me
</button>
```

Django View:

```python
from django.http import HttpResponse

def hello(request):

    return HttpResponse(
        "<h2>Hello Django HTMX!</h2>"
    )
```

URL:

```python
from django.urls import path
from . import views

urlpatterns = [
    path(
        "hello/",
        views.hello,
        name="hello"
    ),
]
```

## 6.2 hx-post

Sends an HTTP POST request.

HTML:

```html
<form
    hx-post="/submit/"
    hx-target="#result">

    {% csrf_token %}

    <input
        type="text"
        name="username"
        placeholder="Username"
    >

    <button type="submit">
        Submit
    </button>

</form>

<div id="result"></div>
```

Django View:

```python
from django.http import HttpResponse
from django.views.decorators.http import require_POST

@require_POST
def submit(request):

    username = request.POST.get("username")

    return HttpResponse(
        f"Welcome {username}"
    )
```

## 6.3 hx-target

Defines where the server response should be inserted.

```html
<button
    hx-get="/hello/"
    hx-target="#content">

    Load Content

</button>

<div id="content">
    Original Content
</div>
```

Here, the `#content` element will be updated.

## 6.4 hx-swap

Controls how the response is inserted into the target element.

| Value | Description |
|---|---|
| innerHTML | Replaces inner HTML |
| outerHTML | Replaces entire element |
| beforebegin | Inserts before target |
| afterbegin | Inserts as first child |
| beforeend | Inserts as last child |
| afterend | Inserts after target |
| textContent | Replaces text content |
| delete | Deletes target |
| none | Does not swap response |

Example:

```html
<button
    hx-get="/hello/"
    hx-target="#content"
    hx-swap="innerHTML">

    Load

</button>
```

## 6.5 hx-trigger

Defines when an HTTP request should be sent.

Example:

```html
<button
    hx-get="/hello/"
    hx-trigger="click">

    Click

</button>
```

Input example:

```html
<input
    type="text"
    name="search"
    hx-get="/search/"
    hx-trigger="keyup changed delay:500ms"
    hx-target="#results"
>
```

Important trigger events:

- click
- change
- keyup
- keydown
- submit
- load
- revealed
- intersect

Trigger modifiers:

- changed
- delay
- throttle
- once
- from
- target
- consume
- queue

## 6.6 hx-indicator

Displays a loading indicator during an HTMX request.

HTML:

```html
<button
    hx-get="/data/"
    hx-target="#result"
    hx-indicator="#loading">

    Load Data

</button>

<span
    id="loading"
    class="htmx-indicator">

    Loading...

</span>

<div id="result"></div>
```

CSS:

```css
.htmx-indicator {
    display: none;
}

.htmx-request .htmx-indicator {
    display: inline;
}
```

## 6.7 hx-confirm

Displays a confirmation popup before sending a request.

```html
<button
    hx-delete="/delete/1/"
    hx-confirm="Are you sure?"
    hx-target="#item">

    Delete

</button>
```

## 6.8 hx-push-url

Pushes a new URL into browser history.

```html
<a
    hx-get="/products/"
    hx-push-url="true"
    hx-target="#content">

    Products

</a>
```

## 6.9 hx-vals

Sends additional values with the request.

```html
<button
    hx-get="/products/"
    hx-vals='{"category": "electronics"}'
    hx-target="#products">

    Electronics

</button>
```

## 6.10 hx-include

Includes values from other HTML elements in the request.

```html
<input
    id="username"
    name="username"
>

<button
    hx-get="/profile/"
    hx-include="#username">

    Load Profile

</button>
```

# 7. Django HTMX Template Tags

django-htmx provides a template tag for including HTMX JavaScript.

### base.html

```html
{% load django_htmx %}

<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <title>Django HTMX</title>

    {% htmx_script %}

</head>

<body>

    <div id="content">

        {% block content %}
        {% endblock %}

    </div>

</body>
</html>
```

### Important

`{% htmx_script %}` includes the HTMX script and django-htmx JavaScript extension.

Therefore, you generally do not need to include another HTMX CDN script.

### CSRF Configuration

You can configure HTMX to send the Django CSRF token.

```html
<body
    hx-headers='{"x-csrftoken": "{{ csrf_token }}"}'
>
```

This is useful for POST, PUT, PATCH and DELETE requests.

# 8. Practical Project – Live Search

Now build a real Django HTMX live search application.

### Step 1: Create Model

models.py:

```python
from django.db import models


class Product(models.Model):

    name = models.CharField(
        max_length=200
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.name
```

Run migrations:

```bash
python manage.py makemigrations

python manage.py migrate
```

### Step 2: Create Views

views.py:

```python
from django.shortcuts import render

from .models import Product


def product_list(request):

    products = Product.objects.all()

    return render(
        request,
        "products.html",
        {
            "products": products
        }
    )


def product_search(request):

    query = request.GET.get(
        "search",
        ""
    )

    products = Product.objects.filter(
        name__icontains=query
    )

    return render(
        request,
        "partials/product_results.html",
        {
            "products": products
        }
    )
```

### Step 3: Configure URLs

urls.py:

```python
from django.urls import path

from . import views


urlpatterns = [

    path(
        "products/",
        views.product_list,
        name="product_list"
    ),

    path(
        "search/",
        views.product_search,
        name="product_search"
    ),

]
```

### Step 4: Main Template

products.html:

```html
{% extends "base.html" %}

{% block content %}

<h1>Product Search</h1>

<input
    type="search"
    name="search"
    placeholder="Search products..."

    hx-get="{% url 'product_search' %}"

    hx-trigger="keyup changed delay:500ms"

    hx-target="#product-results"
>

<div id="product-results">

    {% include "partials/product_results.html" %}

</div>

{% endblock %}
```

### Step 5: Partial Template

partials/product_results.html:

```html
{% for product in products %}

    <div>

        <h3>{{ product.name }}</h3>

        <p>
            Price: {{ product.price }}
        </p>

    </div>

{% empty %}

    <p>No products found.</p>

{% endfor %}
```

### Result

Now when the user types into the search box:

1. HTMX sends a GET request.
2. Django searches the database.
3. Django returns the product results.
4. HTMX updates the result container.
5. The entire page does not reload.

# 9. Django HTMX CRUD

CRUD means:

- Create
- Read
- Update
- Delete

## 9.1 Create Product

HTML:

```html
<form
    hx-post="{% url 'product_create' %}"
    hx-target="#product-list"
    hx-swap="afterbegin">

    {% csrf_token %}

    <input
        names %}
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
