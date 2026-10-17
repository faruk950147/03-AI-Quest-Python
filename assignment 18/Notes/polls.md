# Django Class-Based Views (CBV)

## 1. What Are Class-Based Views?

**Class-Based Views (CBV)** are a way to handle HTTP requests in Django using Python classes instead of functions.

CBVs allow us to organize request-handling logic into methods such as `get()` and `post()`.

### Example

```python
from django.http import HttpResponse
from django.views import View


class HomeView(View):
    def get(self, request):
        return HttpResponse("Hello, Django CBV!")
```

**Explanation:**

- `View` is Django's built-in base class.
- `HomeView` is our custom view class.
- `get()` handles GET requests.
- `request` contains information about the incoming HTTP request.

## 2. Function-Based Views (FBV) vs Class-Based Views (CBV)

### Function-Based View (FBV)

```python
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello, Django!")
```

### Class-Based View (CBV)

```python
from django.http import HttpResponse
from django.views import View


class HomeView(View):
    def get(self, request):
        return HttpResponse("Hello, Django!")
```

### Differences

| FBV | CBV |
|---|---|
| Uses functions | Uses classes |
| Defined using `def` | Defined using `class` |
| Often uses `if request.method == "POST"` | Can use separate `get()` and `post()` methods |
| Simple for straightforward logic | Supports inheritance and reusable behavior |
| Uses function-based decorators | Can use method decorators or override `dispatch()` |

## 3. Common HTTP Methods in CBV

```python
from django.http import HttpResponse
from django.views import View


class ExampleView(View):

    def get(self, request):
        return HttpResponse("GET request")

    def post(self, request):
        return HttpResponse("POST request")

    def put(self, request):
        return HttpResponse("PUT request")

    def delete(self, request):
        return HttpResponse("DELETE request")
```

- `get()` — Retrieves or displays information.
- `post()` — Submits data or performs an operation.
- `put()` — Typically replaces an existing resource.
- `delete()` — Deletes a resource.

Django's standard HTML forms primarily use GET and POST. PUT and DELETE generally require additional handling or API clients.

## 4. URL Configuration in CBV

Use `as_view()` to connect a CBV to a URL.

### views.py

```python
from django.http import HttpResponse
from django.views import View


class HomeView(View):
    def get(self, request):
        return HttpResponse("Home Page")
```

### urls.py

```python
from django.urls import path
from .views import HomeView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
```

**Important:** `HomeView.as_view()` converts the class into a callable view that Django can use to process requests.

## 5. Important Built-in Generic CBVs

Django provides several generic class-based views for common application tasks.

### 5.1 ListView

`ListView` displays a list of database objects.

```python
from django.views.generic import ListView
from .models import Question


class QuestionListView(ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "questions"
    ordering = ["-pub_date"]
```

**Important attributes:**

- `model` — Specifies the model to retrieve data from.
- `template_name` — Specifies the template to render.
- `context_object_name` — Specifies the variable name used in the template.
- `ordering` — Specifies the default ordering of objects.

### 5.2 DetailView

`DetailView` displays the details of a single object.

```python
from django.views.generic import DetailView
from .models import Question


class QuestionDetailView(DetailView):
    model = Question
    template_name = "polls/detail.html"
    context_object_name = "question"
```

By default, `DetailView` uses the `pk` URL parameter to identify the object.

### 5.3 CreateView

`CreateView` provides functionality for creating new database objects.

```python
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Question


class QuestionCreateView(CreateView):
    model = Question
    fields = ["question_text"]
    template_name = "polls/question_form.html"
    success_url = reverse_lazy("polls:index")
```

- `fields` specifies which model fields appear in the form.
- `success_url` specifies where the user is redirected after successful creation.
- Django handles form validation and object creation.

### 5.4 UpdateView

`UpdateView` provides functionality for updating existing objects.

```python
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import Question


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ["question_text"]
    template_name = "polls/question_form.html"
    success_url = reverse_lazy("polls:index")
```

### 5.5 DeleteView

`DeleteView` provides functionality for deleting existing objects.

```python
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import Question


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = "polls/question_confirm_delete.html"
    success_url = reverse_lazy("polls:index")
```

Deletion is normally confirmed through a POST form.

### 5.6 TemplateView

`TemplateView` renders a specified template.

```python
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "about.html"
```

### 5.7 RedirectView

`RedirectView` redirects users to another URL.

```python
from django.views.generic import RedirectView


class GoogleRedirectView(RedirectView):
    url = "https://www.google.com/"
```

## 6. Django Polls Application Using CBV

This project includes:

- Questions and multiple choices
- Voting functionality
- Database storage
- Vote results
- Django Admin management

### Step 1: Create Models

File: `polls/models.py`

```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
    )
    choice_text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.choice_text
```

**Model explanation:**

- `Question` stores poll questions.
- `Choice` stores the available options for each question.
- `ForeignKey` establishes a relationship between `Choice` and `Question`.
- `on_delete=models.CASCADE` deletes associated choices when a question is deleted.
- `related_name="choices"` allows access through `question.choices.all()`.
- `votes` stores the number of votes received by each choice.

### Step 2: Register the Application

File: `mysite/settings.py`

Add `"polls"` to `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "polls",
]
```

### Step 3: Create Class-Based Views

File: `polls/views.py`

```python
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Question, Choice


class IndexView(ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "questions"
    ordering = ["-pub_date"]


class QuestionDetailView(DetailView):
    model = Question
    template_name = "polls/detail.html"
    context_object_name = "question"


class VoteView(View):
    def post(self, request, question_id):
        question = get_object_or_404(
            Question,
            pk=question_id,
        )

        choice_id = request.POST.get("choice")

        if not choice_id:
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "You did not select a choice.",
                },
                status=400,
            )

        choice = get_object_or_404(
            Choice,
            pk=choice_id,
            question=question,
        )

        Choice.objects.filter(pk=choice.pk).update(
            votes=F("votes") + 1
        )

        return redirect(
            reverse("polls:results", args=[question.pk])
        )


class ResultsView(DetailView):
    model = Question
    template_name = "polls/results.html"
    context_object_name = "question"
```

**Explanation:**

- `IndexView` displays all questions.
- `QuestionDetailView` displays a specific question and its choices.
- `VoteView` processes submitted votes.
- `ResultsView` displays the voting results.
- `get_object_or_404()` retrieves an object or returns an HTTP 404 response.
- `F("votes") + 1` increments the vote count in the database without first reading and modifying the count in Python.

### Step 4: Configure Application URLs

File: `polls/urls.py`

```python
from django.urls import path

from .views import (
    IndexView,
    QuestionDetailView,
    VoteView,
    ResultsView,
)

app_name = "polls"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    path(
        "<int:pk>/",
        QuestionDetailView.as_view(),
        name="detail",
    ),

    path(
        "<int:question_id>/vote/",
        VoteView.as_view(),
        name="vote",
    ),

    path(
        "<int:pk>/results/",
        ResultsView.as_view(),
        name="results",
    ),
]
```

File: `mysite/urls.py`

```python
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("polls/", include("polls.urls")),
]
```

**Important:** `DetailView` uses `pk` by default, while `VoteView` uses the custom parameter `question_id`.

### Step 5: Create the Index Template

File: `polls/templates/polls/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Polls Application</title>
</head>
<body>
    <h1>Recent Questions</h1>

    {% for question in questions %}
        <p>
            <a href="{% url 'polls:detail' question.pk %}">
                {{ question.question_text }}
            </a>
        </p>
    {% empty %}
        <p>No questions are available.</p>
    {% endfor %}
</body>
</html>
```

### Step 6: Create the Detail Template

File: `polls/templates/polls/detail.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ question.question_text }}</title>
</head>
<body>
    <h1>{{ question.question_text }}</h1>

    {% if error_message %}
        <p>{{ error_message }}</p>
    {% endif %}

    <form
        action="{% url 'polls:vote' question.pk %}"
        method="post"
    >
        {% csrf_token %}

        {% for choice in question.choices.all %}
            <label>
                <input
                    type="radio"
                    name="choice"
                    value="{{ choice.pk }}"
                >
                {{ choice.choice_text }}
            </label>
            <br>
        {% empty %}
            <p>No choices are available.</p>
        {% endfor %}

        <button type="submit">Vote</button>
    </form>

    <p>
        <a href="{% url 'polls:index' %}">
            View all questions
        </a>
    </p>
</body>
</html>
```

### Step 7: Create the Results Template

File: `polls/templates/polls/results.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Poll Results</title>
</head>
<body>
    <h1>{{ question.question_text }}</h1>
    <h2>Voting Results</h2>

    <ul>
        {% for choice in question.choices.all %}
            <li>
                {{ choice.choice_text }} —
                {{ choice.votes }} votes
            </li>
        {% empty %}
            <li>No choices are available.</li>
        {% endfor %}
    </ul>

    <a href="{% url 'polls:detail' question.pk %}">
        Vote again
    </a>

    <br><br>

    <a href="{% url 'polls:index' %}">
        View all questions
    </a>
</body>
</html>
```

### Step 8: Configure Django Admin

File: `polls/admin.py`

```python
from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date")
    search_fields = ("question_text",)
    inlines = [ChoiceInline]
```

### Step 9: Run the Project

Install Django:

```bash
pip install django
```

Create database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

**Application URLs:**

- Polls application: `http://127.0.0.1:8000/polls/`
- Django Admin: `http://127.0.0.1:8000/admin/`

Log in to the Admin panel, create a question with at least two choices, and then open the Polls application to vote.

## 7. Important CBV Concepts

### `as_view()`

Converts a class-based view into a callable that Django can use in URL configuration.

```python
path("", IndexView.as_view(), name="index")
```

### `model`

Specifies the model used by a generic view.

```python
model = Question
```

### `template_name`

Specifies which template should be rendered.

```python
template_name = "polls/index.html"
```

### `context_object_name`

Specifies the variable name used to access the objects in the template.

```python
context_object_name = "questions"
```

### `get_queryset()`

Customizes which objects are retrieved from the database.

```python
class QuestionListView(ListView):
    model = Question

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")
```

### `get_context_data()`

Adds extra data to the template context.

```python
class QuestionListView(ListView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_questions"] = Question.objects.count()
        return context
```

### `get_object()`

Generic detail views use this method to retrieve the object being displayed. It can be overridden to customize object retrieval.

### `reverse_lazy()`

Resolves a named URL lazily, making it useful for class attributes such as `success_url`.

```python
from django.urls import reverse_lazy

success_url = reverse_lazy("polls:index")
```

## 8. Advantages of CBV

1. Supports code reuse through inheritance.
2. Separates request handling into methods.
3. Provides built-in generic views for common operations.
4. Reduces boilerplate code for CRUD operations.
5. Supports customization through methods such as `get_queryset()` and `get_context_data()`.
6. Helps organize larger applications.

## 9. Important Limitations and Security Notes

- CBVs are not automatically better than FBVs for every task; choose the approach that makes the code easiest to understand and maintain.
- The example application allows the same user to vote multiple times.
- `F()` expressions help prevent lost updates to vote counts, but they do not prevent duplicate voting.
- Production applications should implement authentication where appropriate, duplicate-vote prevention, validation, and suitable authorization and transaction handling.
- The example uses Django's CSRF token in the voting form.

## 10. Interview Questions and Answers

**Q1. What is a Class-Based View?**

A CBV is a Django view implemented as a Python class that handles HTTP requests through methods.

**Q2. What is the purpose of `as_view()`?**

It converts a class-based view into a callable view that Django can use in URL configuration.

**Q3. What is the difference between `ListView` and `DetailView`?**

`ListView` displays multiple objects, while `DetailView` displays one object's details.

**Q4. What is `context_object_name`?**

It defines the variable name used to access the view's object or queryset in a template.

**Q5. What is `get_queryset()`?**

It is a method used to customize the queryset retrieved by a generic view.

**Q6. What is `get_context_data()`?**

It is a method used to add additional data to a template's context.

**Q7. Why do we use `reverse_lazy()`?**

It resolves a named URL lazily and is useful when configuring URL-dependent class attributes.

**Q8. Can a CBV handle GET and POST requests?**

Yes. A class derived from `View` can define `get()` and `post()` methods to handle those HTTP methods.

**Q9. What are generic CBVs?**

They are Django's built-in class-based views that simplify common tasks such as listing, displaying, creating, updating, and deleting objects.

**Q10. What is the difference between FBV and CBV?**

An FBV uses a function to handle requests, while a CBV uses a class and its methods.

**Q11. What is `dispatch()`?**

`dispatch()` routes a request to the appropriate method, such as `get()` or `post()`, based on the HTTP method.

**Q12. What is the purpose of `F()` expressions?**

They allow database operations to reference existing field values directly, which is useful for atomic increments and updates.
