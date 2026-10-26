# Django CRUD Application

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from .models import Student


# CREATE
def student_create(request):

    if request.method == 'POST':

        firstname = request.POST.get('firstname')
        surname = request.POST.get('surname')
        age = request.POST.get('age')
        classroom = request.POST.get('classroom')

        sql = """
            INSERT INTO student_student
            (firstname, surname, age, classroom)
            VALUES (%s, %s, %s, %s)
        """

        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                [firstname, surname, age, classroom]
            )

        return redirect('student_list')

    return render(request, 'create.html')


# READ ALL
def student_list(request):

    sql = "SELECT * FROM student_student"

    posts = Student.objects.raw(sql)

    print(posts)
    print(connection.queries)

    return render(request, 'output.html', {'data': posts})


# READ SINGLE
def detail(request, id):

    sql = "SELECT * FROM student_student WHERE id = %s"

    student = list(Student.objects.raw(sql, [id]))

    if not student:
        return HttpResponse("Student not found", status=404)

    return render(
        request,
        'detail.html',
        {'student': student[0]}
    )


# UPDATE
def student_update(request, id):

    sql = "SELECT * FROM student_student WHERE id = %s"

    student = list(Student.objects.raw(sql, [id]))

    if not student:
        return HttpResponse("Student not found", status=404)

    student = student[0]

    if request.method == 'POST':

        firstname = request.POST.get('firstname')
        surname = request.POST.get('surname')
        age = request.POST.get('age')
        classroom = request.POST.get('classroom')

        sql = """
            UPDATE student_student
            SET firstname = %s,
                surname = %s,
                age = %s,
                classroom = %s
            WHERE id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                [firstname, surname, age, classroom, id]
            )

        return redirect('student_list')

    return render(
        request,
        'update.html',
        {'student': student}
    )


# DELETE
def student_delete(request, id):

    if request.method == 'POST':

        sql = "DELETE FROM student_student WHERE id = %s"

        with connection.cursor() as cursor:
            cursor.execute(sql, [id])

        return redirect('student_list')

    return HttpResponse(
        "Use POST request to delete a student.",
        status=405
    )


# Django Class-Based Views (CBV) — Complete Notes
from django.db.models import F
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render  # <-- Added redirect
from django.urls import reverse
from django.views import View

from polls.models import Choice, Question


class HomePage(View):
    def get(self, request):
        questions = Question.objects.raw(
            """
            SELECT * FROM polls_question;
            """
        )

        context = {"questions": questions}

        return render(request, "polls/home.html", context)


class DetailPage(View):
    def get(self, request, pk):
        question = Question.objects.raw(
            """
            SELECT * FROM polls_question
            WHERE id = %s;
            """,
            [pk],
        )

        question = next(iter(question), None)

        if question is None:
            raise Http404("Question does not exist")

        context = {"question": question}

        return render(request, "polls/detail.html", context)


class VotingView(View):

    def post(self, request, pk):
        question = Question.objects.raw(
            """
            SELECT * FROM polls_question
            WHERE id = %s;
            """,
            [pk],
        )

        # Unwrap the RawQuerySet to get the actual Question instance
        question = next(iter(question), None)

        if question is None:
            raise Http404("Question does not exist")

        choice_id = request.POST.get("choice")

        if not choice_id:
            return redirect("polls:detail", pk=question.id)

        selected_choice = question.choice_set.filter(pk=choice_id).first()

        if selected_choice is None:
            return redirect("polls:detail", pk=question.id)

        selected_choice.votes = F("votes") + 1
        selected_choice.save(update_fields=["votes"])

        return HttpResponseRedirect(
            reverse("polls:results", args=[question.id])
        )


class ResultsPage(View):

    def get(self, request, pk):
        question = Question.objects.raw(
            """
            SELECT * FROM polls_question
            WHERE id = %s;
            """,
            [pk],
        )

        question = next(iter(question), None)

        if question is None:
            raise Http404("Question does not exist")

        context = {"question": question}

        return render(request, "polls/results.html", context)




# Django Class-Based Views (CBVs) + Polls Project — Full Notes

> Complete study notes covering Django Class-Based Views, a working Polls application, AJAX voting with JSON responses, authentication and permissions, common errors, interview questions, and practice tasks.

---

## Table of Contents

1. [What Are Class-Based Views?](#1-what-are-class-based-views)
2. [Common Built-in Generic Views](#2-common-built-in-generic-views)
3. [Important CBV Methods](#3-important-cbv-methods)
4. [Create the Django Project](#4-create-the-django-project)
5. [Create Models](#5-create-models)
6. [Migrations](#6-migrations)
7. [Configure URLs](#7-configure-urls)
8. [Build Class-Based Views](#8-build-class-based-views)
9. [Create Templates](#9-create-templates)
10. [Admin Panel](#10-admin-panel)
11. [Run and Test the Project](#11-run-and-test-the-project)
12. [AJAX Voting with JSON](#12-ajax-voting-with-json)
13. [Authentication and Permissions](#13-authentication-and-permissions)
14. [Security and Good Practices](#14-security-and-good-practices)
15. [Common Errors and Fixes](#15-common-errors-and-fixes)
16. [Interview Questions and Answers](#16-interview-questions-and-answers)
17. [Quick Revision](#17-quick-revision)
18. [Practice Roadmap](#18-practice-roadmap)

---

## 1. What Are Class-Based Views?

A **Class-Based View (CBV)** is a Django view written as a Python class rather than a function. It organizes request-handling logic into methods such as `get()` and `post()`.

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

Register a CBV in `urls.py` using `.as_view()`:

```python
path("", HomeView.as_view(), name="home")
```

### Why use CBVs?

- Organize related request logic in one class.
- Separate HTTP methods (`GET`, `POST`, etc.).
- Reuse behavior through inheritance and mixins.
- Use Django's generic views for common CRUD patterns.
- Keep larger applications structured.

CBVs are not automatically better for every situation. FBVs can be simpler for small, straightforward views.

---

## 2. Common Built-in Generic Views

Import generic views from `django.views.generic`.

| View | Purpose |
|---|---|
| `View` | Base class for custom request handling |
| `TemplateView` | Renders a template |
| `ListView` | Displays a list of objects |
| `DetailView` | Displays one object |
| `CreateView` | Creates an object using a form |
| `UpdateView` | Updates an object using a form |
| `DeleteView` | Deletes an object after confirmation |
| `FormView` | Handles a form without necessarily saving a model |

### Example: `TemplateView`

```python
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "about.html"
```

### Example: `ListView`

```python
from django.views.generic import ListView
from .models import Question

class QuestionListView(ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "questions"
    ordering = ["-pub_date"]
```

### Example: `DetailView`

```python
from django.views.generic import DetailView
from .models import Question

class QuestionDetailView(DetailView):
    model = Question
    template_name = "polls/detail.html"
    context_object_name = "question"
```

Django's generic views reduce repetitive code. Use a custom `View` when you need more control over the request flow.

---

## 3. Important CBV Methods

| Method | Purpose |
|---|---|
| `as_view()` | Converts a view class into a callable URL view |
| `setup()` | Initializes request-related attributes |
| `dispatch()` | Sends a request to the correct method |
| `get()` | Handles GET requests |
| `post()` | Handles POST requests |
| `get_queryset()` | Returns the objects a generic view works with |
| `get_context_data()` | Adds data to template context |
| `get_object()` | Retrieves the object for a detail/update/delete view |
| `form_valid()` | Handles a valid form |
| `form_invalid()` | Handles an invalid form |

### How `dispatch()` works

For a `GET` request, Django normally calls `get()`. For a `POST` request, Django normally calls `post()`. If the class does not support the requested method, Django returns `405 Method Not Allowed`.

---

## 4. Create the Django Project

### Install Django

```bash
python -m venv venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt**
```cmd
venv\Scripts\activate
```

**Linux/macOS**
```bash
source venv/bin/activate
```

Install Django:

```bash
python -m pip install django
```

### Create project and app

```bash
django-admin startproject config .
python manage.py startapp polls
```

Add the app in `config/settings.py`:

```python
INSTALLED_APPS = [
    # Django apps...
    "polls",
]
```

Suggested project structure:

```text
project/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
├── polls/
│   ├── migrations/
│   ├── templates/
│   │   └── polls/
│   │       ├── index.html
│   │       ├── detail.html
│   │       └── results.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
└── venv/
```

---

## 5. Create Models

In `polls/models.py`:

```python
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timezone.timedelta(days=1)


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

### Model concepts

- `CharField`: stores short text.
- `DateTimeField`: stores date and time.
- `ForeignKey`: creates a many-to-one relationship.
- `on_delete=models.CASCADE`: deletes related choices when their question is deleted.
- `related_name="choices"`: allows `question.choices.all()`.
- `default=0`: initializes the vote count.
- `__str__()`: gives the model a readable representation in the admin and shell.

If you prefer the classic Django tutorial style, you can omit `related_name` and use `question.choice_set.all()` in templates and Python.

---

## 6. Migrations

After changing models, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

- `makemigrations` creates migration files describing model changes.
- `migrate` applies migrations to the database.

Create an admin user:

```bash
python manage.py createsuperuser
```

---

## 7. Configure URLs

### `config/urls.py`

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("polls/", include("polls.urls")),
]
```

### `polls/urls.py`

```python
from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.QuestionDetailView.as_view(), name="detail"),
    path("<int:pk>/vote/", views.VoteView.as_view(), name="vote"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
]
```

### Important URL rule

The URL parameter name must match the keyword argument expected by the view.

For example:

```python
path("<int:pk>/vote/", VoteView.as_view(), name="vote")
```

matches:

```python
def post(self, request, pk):
    ...
```

If the URL uses `question_id`, then the view must accept `question_id` or the URL must be changed to use `pk`. A mismatch can produce a `TypeError`.

---

## 8. Build Class-Based Views

In `polls/views.py`:

```python
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import Choice, Question


class IndexView(View):
    def get(self, request):
        questions = Question.objects.order_by("-pub_date")
        return render(
            request,
            "polls/index.html",
            {"questions": questions},
        )


class QuestionDetailView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        return render(
            request,
            "polls/detail.html",
            {"question": question},
        )


class ResultsView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        return render(
            request,
            "polls/results.html",
            {"question": question},
        )


class VoteView(View):
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        choice_id = request.POST.get("choice")

        if not choice_id:
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "Please select a choice.",
                },
                status=400,
            )

        choice = get_object_or_404(
            Choice,
            pk=choice_id,
            question=question,
        )

        # Atomic database-side increment helps prevent lost updates.
        Choice.objects.filter(pk=choice.pk).update(votes=F("votes") + 1)

        return redirect("polls:results", pk=question.pk)
```

This is the non-AJAX baseline. Section 12 replaces `VoteView` with a version that supports both AJAX and regular form submissions.

### Why use `get_object_or_404()`?

It retrieves an object or returns a 404 response if the object does not exist. This is more appropriate than allowing a missing object to trigger an unhandled exception.

### Why validate the choice against the question?

The filter:

```python
Choice.objects.filter(pk=choice_id, question=question)
```

ensures a user cannot submit a choice belonging to a different question.

---

## 9. Create Templates

Create these files:

- `polls/templates/polls/index.html`
- `polls/templates/polls/detail.html`
- `polls/templates/polls/results.html`

### `index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Polls</title>
</head>
<body>
    <h1>Latest Questions</h1>

    {% if questions %}
        <ul>
            {% for question in questions %}
                <li>
                    <a href="{% url 'polls:detail' question.pk %}">
                        {{ question.question_text }}
                    </a>
                </li>
            {% endfor %}
        </ul>
    {% else %}
        <p>No polls are available.</p>
    {% endif %}
</body>
</html>
```

### `detail.html` — regular form version

This version is a simple baseline before AJAX is added:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ question.question_text }}</title>
</head>
<body>
    <h1>{{ question.question_text }}</h1>

    {% if error_message %}
        <p>{{ error_message }}</p>
    {% endif %}

    <form action="{% url 'polls:vote' question.pk %}" method="post">
        {% csrf_token %}

        {% for choice in question.choices.all %}
            <div>
                <input
                    type="radio"
                    name="choice"
                    id="choice{{ choice.pk }}"
                    value="{{ choice.pk }}"
                >
                <label for="choice{{ choice.pk }}">
                    {{ choice.choice_text }}
                </label>
            </div>
        {% endfor %}

        <button type="submit">Vote</button>
    </form>
</body>
</html>
```

### `results.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Poll Results</title>
</head>
<body>
    <h1>{{ question.question_text }}</h1>
    <h2>Results</h2>

    <ul>
        {% for choice in question.choices.all %}
            <li>
                {{ choice.choice_text }} — {{ choice.votes }} vote{{ choice.votes|pluralize }}
            </li>
        {% endfor %}
    </ul>

    <a href="{% url 'polls:detail' question.pk %}">Vote again</a>
    <a href="{% url 'polls:index' %}">Back to polls</a>
</body>
</html>
```

---

## 10. Admin Panel

In `polls/admin.py`:

```python
from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date"]
    search_fields = ["question_text"]


admin.site.register(Choice)
```

Visit `/admin/` and sign in with the superuser account. You can create questions and choices there.

---

## 11. Run and Test the Project

```bash
python manage.py check
python manage.py runserver
```

Open:

- Polls index: `http://127.0.0.1:8000/polls/`
- Admin: `http://127.0.0.1:8000/admin/`

Create at least one question with two or more choices before testing the vote form.

---

## 12. AJAX Voting with JSON

AJAX lets JavaScript send a request to Django and update part of the page without reloading the entire page. This example uses jQuery and Django's `JsonResponse`.

### 12.1 Replace `VoteView` in `views.py`

Keep the other views and replace only `VoteView` with:

```python
class VoteView(View):
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        choice_id = request.POST.get("choice")

        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        if not choice_id:
            message = "Please select a choice."

            if is_ajax:
                return JsonResponse(
                    {"success": False, "error": message},
                    status=400,
                )

            return render(
                request,
                "polls/detail.html",
                {"question": question, "error_message": message},
                status=400,
            )

        choice = get_object_or_404(
            Choice,
            pk=choice_id,
            question=question,
        )

        Choice.objects.filter(pk=choice.pk).update(votes=F("votes") + 1)
        choice.refresh_from_db()

        if is_ajax:
            return JsonResponse({
                "success": True,
                "message": "Vote submitted successfully!",
                "choice": choice.choice_text,
                "votes": choice.votes,
            })

        return redirect("polls:results", pk=question.pk)
```

This view supports both:
- AJAX requests, which receive JSON.
- Normal HTML form submissions, which redirect to the results page.

### 12.2 Replace `detail.html` with the AJAX version

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ question.question_text }}</title>
</head>
<body>
    <h1>{{ question.question_text }}</h1>

    <form
        id="vote-form"
        action="{% url 'polls:vote' question.pk %}"
        method="post"
    >
        {% csrf_token %}

        {% for choice in question.choices.all %}
            <div>
                <input
                    type="radio"
                    name="choice"
                    id="choice{{ choice.pk }}"
                    value="{{ choice.pk }}"
                >
                <label for="choice{{ choice.pk }}">
                    {{ choice.choice_text }}
                </label>
            </div>
        {% endfor %}

        <button type="submit" id="vote-button">Vote</button>
    </form>

    <p id="vote-message" role="status" aria-live="polite"></p>
    <p id="vote-count"></p>

    <p><a href="{% url 'polls:results' question.pk %}">View results</a></p>
    <p><a href="{% url 'polls:index' %}">Back to polls</a></p>

    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script>
        $(function () {
            $("#vote-form").on("submit", function (event) {
                event.preventDefault();

                const form = $(this);
                const button = $("#vote-button");
                const message = $("#vote-message");
                const selectedChoice = $('input[name="choice"]:checked').val();

                if (!selectedChoice) {
                    message.text("Please select a choice.");
                    return;
                }

                button.prop("disabled", true);
                message.text("Submitting vote...");

                $.ajax({
                    type: "POST",
                    url: form.attr("action"),
                    data: form.serialize(),
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    },
                    success: function (response) {
                        message.text(response.message);
                        $("#vote-count").text(
                            "Your choice: " + response.choice +
                            " | Current votes for this choice: " + response.votes
                        );
                    },
                    error: function (xhr) {
                        const response = xhr.responseJSON;
                        message.text(
                            response && response.error
                                ? response.error
                                : "Unable to submit your vote. Please try again."
                        );
                    },
                    complete: function () {
                        button.prop("disabled", false);
                    }
                });
            });
        });
    </script>
</body>
</html>
```

### 12.3 Example JSON response

Successful response:

```json
{
  "success": true,
  "message": "Vote submitted successfully!",
  "choice": "Python",
  "votes": 5
}
```

Error response when no choice is selected:

```json
{
  "success": false,
  "error": "Please select a choice."
}
```

### 12.4 AJAX request flow

1. The user selects a choice and submits the form.
2. JavaScript prevents the browser's normal form submission with `event.preventDefault()`.
3. `$.ajax()` sends a POST request to Django.
4. Django validates the question and selected choice.
5. Django updates the vote count in the database.
6. Django returns JSON.
7. JavaScript displays the response without a full page reload.

### 12.5 Important AJAX concepts

- `JsonResponse`: returns a Python dictionary as a JSON HTTP response.
- `serialize()`: serializes form fields, including the CSRF token.
- `X-Requested-With`: a header commonly used to identify AJAX requests.
- `success`: runs when the server returns a successful HTTP status.
- `error`: runs for HTTP errors such as 400 or 404.
- `complete`: runs after the request finishes, whether successful or not.
- `event.preventDefault()`: stops normal form submission.
- `F("votes") + 1`: increments the count inside the database, helping avoid lost updates from concurrent increments.

**Important:** This basic example does not prevent repeat voting. A visitor can submit multiple votes. To restrict voting, design a separate vote-record model and enforce the rule on the server, usually with authentication and a database uniqueness constraint. AJAX is not a security feature by itself.

### 12.6 Troubleshooting AJAX

- **CSRF 403:** ensure `{% csrf_token %}` is inside the form and that `serialize()` is sending it.
- **404:** confirm the vote URL and question ID are correct.
- **405:** make sure the form uses `method="post"` and the view implements `post()`.
- **No JSON in success callback:** inspect the browser's Network tab and Django response.
- **jQuery not loaded:** check the browser console and script URL.
- **Vote count does not update on the results page:** this code updates the message on the detail page. Reload or navigate to the results page to see the full updated results.

---

## 13. Authentication and Permissions

Django provides authentication and permission tools. The correct approach depends on whether voting is public or restricted to logged-in users.

### Require login

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class PrivateView(LoginRequiredMixin, View):
    def get(self, request):
        ...
```

`LoginRequiredMixin` should appear before the view class in the inheritance list.

### Require a permission

```python
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View

class QuestionManagementView(PermissionRequiredMixin, View):
    permission_required = "polls.change_question"

    def get(self, request):
        ...
```

Django's default model permissions include `add`, `change`, `delete`, and `view` permissions for models.

### AJAX and login redirects

If an AJAX request is redirected to a login page, JavaScript may receive HTML instead of JSON. If your endpoint requires login, consider returning a JSON `401` or `403` response for AJAX requests and handling that status in JavaScript.

---

## 14. Security and Good Practices

1. Keep Django CSRF protection enabled for POST requests.
2. Validate submitted IDs on the server; never trust client-side validation alone.
3. Confirm that a selected choice belongs to the question in the URL.
4. Use Django's ORM rather than building SQL strings from user input.
5. Use `F()` expressions for atomic counter increments.
6. Add authentication and a database-backed duplicate-vote rule if required.
7. Do not expose secret keys, passwords, or production credentials in source control.
8. Use environment variables and appropriate production settings for deployment.
9. Add tests for valid votes, missing choices, invalid IDs, and repeat-vote behavior.
10. Keep templates accessible with labels and status messages.

---

## 15. Common Errors and Fixes

| Error | Common cause | Fix |
|---|---|---|
| `TemplateDoesNotExist` | Template is missing or path is wrong | Check `polls/templates/polls/` and the template name |
| `NoReverseMatch` | Wrong URL name or missing argument | Check `app_name`, route name, and `pk` |
| `TypeError` about unexpected keyword argument | URL parameter name and view argument differ | Make both use `pk` or both use `question_id` |
| `405 Method Not Allowed` | Request method is not implemented | Add `get()` or `post()` as needed |
| `403 CSRF verification failed` | Missing or invalid CSRF token | Include `{% csrf_token %}` in the form |
| `DoesNotExist` | A query assumes an object exists | Use `get_object_or_404()` in views |
| `OperationalError: no such table` | Migrations have not been applied | Run `makemigrations` and `migrate` |
| AJAX returns HTML instead of JSON | Request redirected or wrong endpoint | Inspect Network tab and login behavior |
| Vote count loses updates | Read-modify-write race condition | Use `F("votes") + 1` in a database update |

---

## 16. Interview Questions and Answers

### 1. What is a Class-Based View?
A view implemented as a Python class, with request-handling methods such as `get()` and `post()`.

### 2. What does `as_view()` do?
It returns a callable view function that Django can use in URL configuration.

### 3. What is `dispatch()`?
It routes an incoming request to the handler for its HTTP method, such as `get()` or `post()`.

### 4. What is the difference between FBV and CBV?
FBVs use functions; CBVs use classes and methods. CBVs support inheritance and reusable mixins, while FBVs can be simpler for small tasks.

### 5. What is `ListView`?
A generic view for displaying a list of model objects or another queryset.

### 6. What is `DetailView`?
A generic view for displaying a single object.

### 7. Why use `get_object_or_404()`?
It returns the requested object or a 404 response if it does not exist.

### 8. What is a queryset?
A lazy, chainable representation of database queries, commonly created using a model manager such as `Question.objects`.

### 9. What is a `ForeignKey`?
A field representing a many-to-one relationship between models.

### 10. What does `on_delete=models.CASCADE` mean?
Deleting the referenced parent object also deletes related child objects.

### 11. What is the purpose of migrations?
They record and apply database schema changes based on model changes.

### 12. What is CSRF?
Cross-Site Request Forgery is an attack that attempts to make a user's browser submit an unwanted authenticated request. Django provides CSRF protection for unsafe requests.

### 13. What is AJAX?
A browser technique for sending asynchronous requests and updating parts of a page without reloading the whole page.

### 14. What is `JsonResponse`?
A Django response class that serializes data, commonly a dictionary, as JSON.

### 15. Why use `event.preventDefault()`?
To stop the form's normal browser submission so JavaScript can handle it.

### 16. What does jQuery's `serialize()` do?
It serializes successful form controls into URL-encoded form data, including the CSRF field if present.

### 17. Why validate that a choice belongs to the question?
To prevent a client from submitting a valid choice ID that belongs to a different question.

### 18. Why use `F("votes") + 1`?
It performs the increment in the database rather than relying on a potentially stale Python-side value.

### 19. Does AJAX prevent duplicate voting?
No. Duplicate voting must be prevented by server-side rules and, where appropriate, database constraints.

### 20. What is `LoginRequiredMixin`?
A mixin that requires the user to be authenticated before accessing the view.

### 21. What is `PermissionRequiredMixin`?
A mixin that checks whether the user has the specified permission.

### 22. What is the difference between GET and POST?
GET is generally used to retrieve data; POST is commonly used to submit data that changes server state. State-changing actions should not be implemented as GET requests.

### 23. What is the purpose of `context_object_name`?
It defines the name under which a generic view exposes an object or queryset to the template.

### 24. What is `get_queryset()` used for?
It customizes which objects a generic view retrieves, such as filtering results by the current user.

### 25. What is the purpose of `get_context_data()`?
It adds extra context variables to the template context.

---

## 17. Quick Revision

```text
CBV URL registration       → MyView.as_view()
GET handler                → get(self, request, ...)
POST handler               → post(self, request, ...)
Generic list               → ListView
Generic detail             → DetailView
Missing object             → get_object_or_404()
Model relationship         → ForeignKey
Create migration files     → python manage.py makemigrations
Apply migrations           → python manage.py migrate
CSRF form field            → {% csrf_token %}
AJAX JSON response         → JsonResponse({...})
Prevent normal form submit → event.preventDefault()
Serialize form data        → $(form).serialize()
Atomic counter increment   → F("votes") + 1
Require login              → LoginRequiredMixin
Require permission         → PermissionRequiredMixin
```

---

## 18. Practice Roadmap

### Beginner
- [ ] Create a Django project and app.
- [ ] Create `Question` and `Choice` models.
- [ ] Run migrations.
- [ ] Register models in admin.
- [ ] Create an index, detail, and results page.
- [ ] Use CBVs and named URL patterns.

### Intermediate
- [ ] Add form validation and clear error messages.
- [ ] Add AJAX voting with JSON responses.
- [ ] Handle invalid IDs and CSRF errors.
- [ ] Add tests for valid and invalid votes.
- [ ] Add login requirements where appropriate.

### Advanced
- [ ] Prevent duplicate votes using a `Vote` model and a database uniqueness constraint.
- [ ] Add pagination and filtering.
- [ ] Use `ListView`, `DetailView`, `CreateView`, and `UpdateView`.
- [ ] Add API endpoints using Django REST Framework.
- [ ] Deploy with environment variables, secure settings, and a production database.

---

## Final Note

Build the project in stages: first make regular Django form voting work, then add AJAX and JSON, and finally add tests and voting restrictions. The browser is responsible for the AJAX interaction, but all validation and security rules must remain on the Django server.
