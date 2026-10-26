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
        
# Django CRUD + Class-Based Views + AJAX Polls
## Complete Advanced Notes — বাংলা ব্যাখ্যা ও English Code

**Topics:** Django CRUD, ORM, Raw SQL, CBV, Generic Views, Polls, AJAX, JSON, Authentication, Permissions, CSRF, Duplicate Vote Prevention, Testing, Security, Interview Questions.

---

## Table of Contents

1. [Django CRUD কী?](#1-django-crud-কী)
2. [Project Setup](#2-project-setup)
3. [Student Model](#3-student-model)
4. [Django ORM বনাম Raw SQL](#4-django-orm-বনাম-raw-sql)
5. [Function-Based CRUD](#5-function-based-crud)
6. [Class-Based Views](#6-class-based-views)
7. [Generic Views](#7-generic-views)
8. [Student CRUD with CBV](#8-student-crud-with-cbv)
9. [Polls Models](#9-polls-models)
10. [Polls URLs and Views](#10-polls-urls-and-views)
11. [Templates](#11-templates)
12. [AJAX and JSON](#12-ajax-and-json)
13. [AJAX Voting Implementation](#13-ajax-voting-implementation)
14. [Authentication and Permissions](#14-authentication-and-permissions)
15. [Duplicate Vote Prevention](#15-duplicate-vote-prevention)
16. [Transactions and F Expressions](#16-transactions-and-f-expressions)
17. [Security Best Practices](#17-security-best-practices)
18. [Admin Configuration](#18-admin-configuration)
19. [Automated Testing](#19-automated-testing)
20. [Common Errors and Solutions](#20-common-errors-and-solutions)
21. [Interview Questions and Answers](#21-interview-questions-and-answers)
22. [Quick Revision](#22-quick-revision)
23. [Practice Roadmap](#23-practice-roadmap)

---

# 1. Django CRUD কী?

CRUD হলো database operation-এর চারটি মৌলিক ধরন।

| Operation | অর্থ | HTTP Method | উদাহরণ |
|---|---|---|---|
| Create | নতুন data তৈরি | POST | নতুন Student তৈরি |
| Read | Data দেখা | GET | Student list |
| Update | Data পরিবর্তন | POST বা PATCH | Student-এর তথ্য পরিবর্তন |
| Delete | Data মুছে ফেলা | POST বা DELETE | Student মুছে ফেলা |

Django-তে CRUD বাস্তবায়নের জন্য সাধারণত তিনটি অংশ ব্যবহৃত হয়:

- **Model:** Database structure ও data access।
- **View:** Request process করে response তৈরি করে।
- **Template:** HTML page দেখায়।

### Django request flow

```text
Browser
   |
   v
URL Dispatcher
   |
   v
View
   |
   v
Model / ORM
   |
   v
Database
   |
   v
View
   |
   v
Template / JSON Response
   |
   v
Browser
```

---

# 2. Project Setup

## 2.1 Create virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

## 2.2 Install Django

```bash
python -m pip install django
```

## 2.3 Create project and apps

```bash
django-admin startproject config .
python manage.py startapp students
python manage.py startapp polls
```

## 2.4 Register apps

`config/settings.py`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "students",
    "polls",
]
```

## 2.5 Recommended structure

```text
project/
├── manage.py
├── config/
│   ├── settings.py
│   └── urls.py
├── students/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
├── polls/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
└── templates/
    ├── registration/
    │   └── login.html
    └── students/
        ├── student_list.html
        ├── student_form.html
        └── student_confirm_delete.html
```

## 2.6 Template configuration

Project-level `templates` folder ব্যবহার করতে `TEMPLATES` setting-এর `DIRS`-এ যোগ করুন:

```python
"DIRS": [BASE_DIR / "templates"],
```

Login settings:

```python
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "polls:index"
LOGOUT_REDIRECT_URL = "login"
```

---

# 3. Student Model

`students/models.py`:

```python
from django.db import models


class Student(models.Model):
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    classroom = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.firstname} {self.surname}"
```

## Model field explanation

- `CharField`: Short text সংরক্ষণ করে।
- `PositiveSmallIntegerField`: Non-negative integer সংরক্ষণ করে।
- `max_length`: Text-এর সর্বোচ্চ দৈর্ঘ্য।
- `__str__()`: Admin ও debugging-এ readable representation দেয়।

## Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

`makemigrations` migration file তৈরি করে।

`migrate` database schema-তে পরিবর্তন প্রয়োগ করে।

---

# 4. Django ORM বনাম Raw SQL

Django ORM database query-কে Python syntax-এ লেখার সুবিধা দেয়।

## Read using ORM

```python
students = Student.objects.all()
```

## Read using Raw SQL

```python
from django.db import connection

sql = "SELECT * FROM students_student"

with connection.cursor() as cursor:
    cursor.execute(sql)
    rows = cursor.fetchall()
```

এখানে `students_student` default table name, যদি model-এর `db_table` আলাদাভাবে নির্ধারণ না করা হয়।

## Raw query with parameters

```python
sql = """
    SELECT * FROM students_student
    WHERE id = %s
"""

with connection.cursor() as cursor:
    cursor.execute(sql, [student_id])
    row = cursor.fetchone()
```

**গুরুত্বপূর্ণ:** User input সরাসরি SQL string-এর মধ্যে concatenate করবেন না। Query parameters ব্যবহার করুন।

## Why prefer ORM?

```python
Student.objects.filter(id=student_id)
```

ORM সুবিধা:

- Database portability।
- Query composition।
- Model object পাওয়া যায়।
- Parameterized query handling।
- Related object ও relationship support।

`Model.objects.raw()` ব্যবহার করলে model-এর primary key query result-এ থাকতে হয় এবং সাধারণত raw SQL-এর জন্য প্রয়োজনীয় অতিরিক্ত সতর্কতা বজায় রাখতে হয়।

---

# 5. Function-Based CRUD

Function-Based View বা FBV হলো Python function দিয়ে request handle করা।

## 5.1 Create

```python
from django.shortcuts import render, redirect
from .models import Student


def student_create(request):
    if request.method == "POST":
        Student.objects.create(
            firstname=request.POST.get("firstname", ""),
            surname=request.POST.get("surname", ""),
            age=request.POST.get("age", ""),
            classroom=request.POST.get("classroom", ""),
        )

        return redirect("student_list")

    return render(request, "create.html")
```

শিক্ষামূলক উদাহরণ হিসেবে এটি দেখানো হয়েছে। Production application-এ সরাসরি `request.POST` থেকে model তৈরি করার বদলে `ModelForm` দিয়ে validation করা উত্তম।

## 5.2 Read all

```python
def student_list(request):
    students = Student.objects.all()

    return render(
        request,
        "output.html",
        {"data": students},
    )
```

## 5.3 Read single

```python
from django.shortcuts import get_object_or_404


def student_detail(request, id):
    student = get_object_or_404(Student, pk=id)

    return render(
        request,
        "detail.html",
        {"student": student},
    )
```

## 5.4 Update

```python
def student_update(request, id):
    student = get_object_or_404(Student, pk=id)

    if request.method == "POST":
        student.firstname = request.POST.get(
            "firstname",
            student.firstname,
        )
        student.surname = request.POST.get(
            "surname",
            student.surname,
        )
        student.save()

        return redirect("student_list")

    return render(
        request,
        "update.html",
        {"student": student},
    )
```

এটি শুধু সংক্ষিপ্ত শিক্ষামূলক উদাহরণ। বাস্তব CRUD-এ age ও classroom-সহ সব field-এর validation করতে `ModelForm` ব্যবহার করুন।

## 5.5 Delete

```python
def student_delete(request, id):
    if request.method != "POST":
        return HttpResponse(
            "POST required",
            status=405,
        )

    student = get_object_or_404(Student, pk=id)
    student.delete()

    return redirect("student_list")
```

Import:

```python
from django.http import HttpResponse
```

Delete operation GET request দিয়ে করা উচিত নয়।

---

# 6. Class-Based Views

Class-Based View বা CBV-তে request handling একটি class-এর method-এ সাজানো হয়।

## FBV example

```python
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello Django")
```

## CBV example

```python
from django.http import HttpResponse
from django.views import View


class HomeView(View):
    def get(self, request):
        return HttpResponse("Hello Django")
```

## URL registration

```python
from django.urls import path
from .views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
```

`as_view()` class-কে Django URL configuration-এর উপযোগী callable view-তে রূপান্তর করে।

## Important CBV methods

| Method | কাজ |
|---|---|
| `as_view()` | Class-কে URL-callable view-তে রূপান্তর |
| `setup()` | Request ও URL arguments সংযুক্ত করে |
| `dispatch()` | HTTP method অনুযায়ী handler নির্বাচন |
| `get()` | GET request handle |
| `post()` | POST request handle |
| `get_queryset()` | Generic view-এর queryset নির্ধারণ |
| `get_context_data()` | Template context বাড়ানো |
| `get_object()` | একটি object retrieve করা |
| `form_valid()` | Valid form process করা |
| `form_invalid()` | Invalid form দেখানো |

যে request method-এর handler নেই, Django সাধারণত `405 Method Not Allowed` ফেরত দেয়।

---

# 7. Generic Views

Django-এর generic views সাধারণ web application-এর repetitive code কমায়।

| Generic View | কাজ |
|---|---|
| `TemplateView` | Template render |
| `ListView` | Object list |
| `DetailView` | একটি object |
| `CreateView` | নতুন object |
| `UpdateView` | Object update |
| `DeleteView` | Object delete |
| `FormView` | Form handling |

## TemplateView

```python
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "about.html"
```

## ListView

```python
from django.views.generic import ListView
from .models import Student


class StudentListView(ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"
    ordering = ["id"]
```

## DetailView

```python
from django.views.generic import DetailView
from .models import Student


class StudentDetailView(DetailView):
    model = Student
    template_name = "students/student_detail.html"
    context_object_name = "student"
```

`DetailView` defaultভাবে URL-এর `pk` বা `slug` ব্যবহার করে object retrieve করতে পারে, যদি configuration সেই অনুযায়ী থাকে।

---

# 8. Student CRUD with CBV

## 8.1 ModelForm

`students/forms.py`:

```python
from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "firstname",
            "surname",
            "age",
            "classroom",
        ]

    def clean_age(self):
        age = self.cleaned_data["age"]

        if not 1 <= age <= 120:
            raise forms.ValidationError(
                "Age must be between 1 and 120."
            )

        return age
```

## 8.2 Views

`students/views.py`:

```python
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Student
from .forms import StudentForm


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"


class StudentCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    permission_required = "students.add_student"
    success_url = reverse_lazy("students:list")


class StudentUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    permission_required = "students.change_student"
    success_url = reverse_lazy("students:list")


class StudentDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = Student
    template_name = "students/student_confirm_delete.html"
    permission_required = "students.delete_student"
    success_url = reverse_lazy("students:list")
```

## 8.3 URLs

`students/urls.py`:

```python
from django.urls import path

from .views import (
    StudentListView,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView,
)

app_name = "students"

urlpatterns = [
    path("", StudentListView.as_view(), name="list"),
    path("create/", StudentCreateView.as_view(), name="create"),
    path("<int:pk>/update/", StudentUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", StudentDeleteView.as_view(), name="delete"),
]
```

## 8.4 Student list template

`templates/students/student_list.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Students</title>
</head>
<body>
    <h1>Student List</h1>

    <a href="{% url 'students:create' %}">Add Student</a>

    <ul>
        {% for student in students %}
            <li>
                {{ student.firstname }}
                {{ student.surname }}
                — {{ student.age }}
                — {{ student.classroom }}

                <a href="{% url 'students:update' student.pk %}">
                    Edit
                </a>

                <a href="{% url 'students:delete' student.pk %}">
                    Delete
                </a>
            </li>
        {% empty %}
            <li>No students found.</li>
        {% endfor %}
    </ul>
</body>
</html>
```

## 8.5 Student form template

`templates/students/student_form.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student Form</title>
</head>
<body>
    <h1>Student Form</h1>

    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}

        <button type="submit">Save</button>
    </form>

    <a href="{% url 'students:list' %}">Back</a>
</body>
</html>
```

## 8.6 Delete confirmation template

`templates/students/student_confirm_delete.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Delete Student</title>
</head>
<body>
    <h1>Confirm Delete</h1>

    <p>
        Delete {{ object.firstname }} {{ object.surname }}?
    </p>

    <form method="post">
        {% csrf_token %}
        <button type="submit">Confirm Delete</button>
    </form>

    <a href="{% url 'students:list' %}">Cancel</a>
</body>
</html>
```

## 8.7 Root URLs

`config/urls.py`:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("students/", include("students.urls")),
    path("polls/", include("polls.urls")),
]
```

---

# 9. Polls Models

Polls application-এ দুটি মূল entity থাকে:

- `Question`: প্রশ্ন সংরক্ষণ করে।
- `Choice`: প্রশ্নের উত্তর বা option সংরক্ষণ করে।

Advanced implementation-এ `Vote` model ব্যবহার করে কে কোন প্রশ্নে ভোট দিয়েছেন তা সংরক্ষণ করা হয়।

`polls/models.py`:

```python
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)

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


class Vote(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="vote_records",
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name="vote_records",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="poll_votes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["question", "user"],
                name="unique_user_vote_per_question",
            ),
        ]

    def clean(self):
        if (
            self.question_id
            and self.choice_id
            and self.choice.question_id != self.question_id
        ):
            raise ValidationError(
                "Choice must belong to the selected question."
            )

    def __str__(self):
        return f"{self.user} - {self.question}"
```

## Model relationships

```text
Question 1 ------ * Choice
Question 1 ------ * Vote
User     1 ------ * Vote
Choice   1 ------ * Vote
```

`ForeignKey` many-to-one relationship তৈরি করে।

`on_delete=models.CASCADE` parent object delete হলে related object-গুলোও delete করে।

`related_name="choices"` ব্যবহার করলে:

```python
question.choices.all()
```

লেখা যায়।

`related_name="vote_records"` ব্যবহার করলে:

```python
question.vote_records.all()
choice.vote_records.all()
```

লেখা যায়।

## Important validation note

`clean()` model validation method; সাধারণ `save()` call নিজে থেকে `full_clean()` চালায় না। তাই voting view-তে choice-question relation অবশ্যই যাচাই করতে হবে। Database uniqueness constraint একই user-এর duplicate vote record প্রতিরোধ করে।

---

# 10. Polls URLs and Views

## 10.1 URLs

`polls/urls.py`:

```python
from django.urls import path

from .views import (
    IndexView,
    QuestionDetailView,
    ResultsView,
    VoteView,
)

app_name = "polls"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:pk>/", QuestionDetailView.as_view(), name="detail"),
    path("<int:pk>/vote/", VoteView.as_view(), name="vote"),
    path("<int:pk>/results/", ResultsView.as_view(), name="results"),
]
```

URL-এর `pk` view method-এর argument-এর সঙ্গে মিলতে হবে:

```python
def get(self, request, pk):
    ...
```

## 10.2 IndexView

```python
from django.views.generic import ListView
from .models import Question


class IndexView(ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "questions"
    ordering = ["-pub_date"]
```

## 10.3 DetailView

```python
from django.shortcuts import get_object_or_404, render
from django.views import View

from .models import Question, Vote


class QuestionDetailView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)

        has_voted = (
            request.user.is_authenticated
            and Vote.objects.filter(
                question=question,
                user=request.user,
            ).exists()
        )

        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "has_voted": has_voted,
            },
        )
```

## 10.4 ResultsView

```python
class ResultsView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)

        return render(
            request,
            "polls/results.html",
            {"question": question},
        )
```

`get_object_or_404()` object না পেলে HTTP 404 response দেয়।

---

# 11. Templates

## 11.1 Poll index

`polls/templates/polls/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Polls</title>
</head>
<body>
    <h1>Available Questions</h1>

    {% for question in questions %}
        <p>
            <a href="{% url 'polls:detail' question.pk %}">
                {{ question.question_text }}
            </a>
        </p>
    {% empty %}
        <p>No polls are available.</p>
    {% endfor %}
</body>
</html>
```

## 11.2 Poll detail

`polls/templates/polls/detail.html`:

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
        <p role="alert">{{ error_message }}</p>
    {% endif %}

    {% if user.is_authenticated %}
        {% if has_voted %}
            <p>You have already voted.</p>
        {% else %}
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
                {% empty %}
                    <p>No choices available.</p>
                {% endfor %}

                <button type="submit" id="vote-button">
                    Vote
                </button>
            </form>

            <p id="vote-message" role="status" aria-live="polite"></p>
            <p id="vote-count"></p>
        {% endif %}
    {% else %}
        <p>Please log in to vote.</p>
    {% endif %}

    <a href="{% url 'polls:results' question.pk %}">
        View results
    </a>
</body>
</html>
```

## 11.3 Poll results

`polls/templates/polls/results.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Poll Results</title>
</head>
<body>
    <h1>{{ question.question_text }}</h1>
    <h2>Results</h2>

    <ul>
        {% for choice in question.choices.all %}
            <li>
                {{ choice.choice_text }} —
                {{ choice.votes }} vote{{ choice.votes|pluralize }}
            </li>
        {% empty %}
            <li>No choices available.</li>
        {% endfor %}
    </ul>

    <a href="{% url 'polls:index' %}">Back to polls</a>
</body>
</html>
```

---

# 12. AJAX and JSON

AJAX হলো browser থেকে asynchronous HTTP request পাঠিয়ে page-এর একটি অংশ update করার পদ্ধতি।

AJAX-এর জন্য পুরো page reload করা প্রয়োজন হয় না।

## Traditional form submission

```text
Submit Form
    |
    v
Browser sends POST
    |
    v
Django processes request
    |
    v
Redirect to new page
```

## AJAX submission

```text
Submit Form
    |
    v
JavaScript intercepts form
    |
    v
Fetch / AJAX POST request
    |
    v
Django validates data
    |
    v
Django returns JSON
    |
    v
JavaScript updates the page
```

## JSON example

```json
{
  "success": true,
  "message": "Vote submitted successfully!",
  "choice": "Python",
  "votes": 5
}
```

## JsonResponse

```python
from django.http import JsonResponse


def example_api(request):
    return JsonResponse({
        "success": True,
        "message": "Hello from Django",
    })
```

`JsonResponse` Python dictionary-কে JSON response-এ রূপান্তর করে।

## AJAX detection

```python
def is_ajax_request(request):
    return (
        request.headers.get("X-Requested-With")
        == "XMLHttpRequest"
    )
```

Django-এর পুরোনো `request.is_ajax()` method deprecated হয়েছিল এবং Django 4.0-তে সরানো হয়। তাই header নিজে পরীক্ষা করা যেতে পারে।

এই header authentication বা security প্রমাণ করে না; client এটি পরিবর্তন করতে পারে।

---

# 13. AJAX Voting Implementation

## 13.1 Secure VoteView

`polls/views.py`:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import Choice, Question, Vote


def is_ajax_request(request):
    return (
        request.headers.get("X-Requested-With")
        == "XMLHttpRequest"
    )


class VoteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        ajax = is_ajax_request(request)

        def error_response(message, status):
            if ajax:
                return JsonResponse(
                    {
                        "success": False,
                        "error": message,
                    },
                    status=status,
                )

            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "has_voted": Vote.objects.filter(
                        question=question,
                        user=request.user,
                    ).exists(),
                    "error_message": message,
                },
                status=status,
            )

        choice_id = request.POST.get("choice")

        if not choice_id:
            return error_response(
                "Please select a choice.",
                400,
            )

        choice = Choice.objects.filter(
            pk=choice_id,
            question=question,
        ).first()

        if choice is None:
            return error_response(
                "Invalid choice for this question.",
                400,
            )

        try:
            with transaction.atomic():
                Vote.objects.create(
                    question=question,
                    choice=choice,
                    user=request.user,
                )

                Choice.objects.filter(pk=choice.pk).update(
                    votes=F("votes") + 1
                )

        except IntegrityError:
            return error_response(
                "You have already voted on this question.",
                409,
            )

        if ajax:
            choice.refresh_from_db()

            return JsonResponse({
                "success": True,
                "message": "Vote submitted successfully!",
                "choice": choice.choice_text,
                "votes": choice.votes,
            })

        return redirect(
            "polls:results",
            pk=question.pk,
        )
```

### How the view works

1. `LoginRequiredMixin` authentication নিশ্চিত করে।
2. `get_object_or_404()` question retrieve করে।
3. `request.POST.get("choice")` selected choice ID নেয়।
4. `Choice.objects.filter(pk=choice_id, question=question)` নিশ্চিত করে choice-টি সঠিক question-এর।
5. `transaction.atomic()` vote record ও counter update এক transaction-এ রাখে।
6. `Vote.objects.create()` vote record তৈরি করে।
7. `F("votes") + 1` database-এ counter বাড়ায়।
8. `IntegrityError` duplicate-vote constraint failure সামলায়।
9. AJAX request-এ JSON এবং normal form request-এ redirect ফেরত আসে।

**Note:** এই implementation-এর vote counter বজায় রাখতে সব vote ও vote-removal operation একই transaction-এ counter update করবে। অন্য code path সরাসরি `Vote` create/delete করলে counter mismatch হতে পারে। Alternative হিসেবে results page-এ vote record থেকে count aggregate করা যায়।

## 13.2 JavaScript AJAX

`detail.html`-এর form-এর পরে এই script যোগ করুন:

```html
<script>
    const form = document.getElementById("vote-form");

    if (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            const button = document.getElementById("vote-button");
            const message = document.getElementById("vote-message");
            const count = document.getElementById("vote-count");

            const selected = form.querySelector(
                'input[name="choice"]:checked'
            );

            if (!selected) {
                message.textContent = "Please select a choice.";
                return;
            }

            button.disabled = true;
            message.textContent = "Submitting vote...";

            try {
                const response = await fetch(form.action, {
                    method: "POST",
                    body: new FormData(form),
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    },
                    credentials: "same-origin"
                });

                const data = await response.json();

                if (!response.ok) {
                    message.textContent =
                        data.error || "Unable to submit vote.";
                    return;
                }

                message.textContent = data.message;
                count.textContent =
                    "Your choice: " + data.choice +
                    " | Total votes: " + data.votes;

                form.remove();
            } catch (error) {
                message.textContent =
                    "Network error. Please try again.";
            } finally {
                if (button.isConnected) {
                    button.disabled = false;
                }
            }
        });
    }
</script>
```

### JavaScript concepts

| Code | কাজ |
|---|---|
| `preventDefault()` | Default form submission বন্ধ করে |
| `fetch()` | HTTP request পাঠায় |
| `FormData(form)` | Form fields ও CSRF token পাঠায় |
| `response.json()` | JSON parse করে |
| `response.ok` | HTTP success status পরীক্ষা করে |
| `textContent` | Text update করে |
| `button.disabled` | Duplicate click-এর সম্ভাবনা কমায় |
| `try/catch` | Network বা parsing error handle করে |

Frontend button disable করা শুধু user experience উন্নত করে। Duplicate voting বন্ধ করার আসল ব্যবস্থা server-side database constraint।

---

# 14. Authentication and Permissions

Django authentication system user login ও permission management দেয়।

## LoginRequiredMixin

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class PrivateView(LoginRequiredMixin, View):
    def get(self, request):
        ...
```

Login না থাকলে Django সাধারণত login page-এ redirect করে।

## PermissionRequiredMixin

```python
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View


class StudentManagementView(
    PermissionRequiredMixin,
    View,
):
    permission_required = "students.change_student"

    def get(self, request):
        ...
```

Django defaultভাবে model-এর জন্য `add`, `change`, `delete` ও `view` permission তৈরি করে।

## Login template

`templates/registration/login.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>

    {% if form.errors %}
        <p>Invalid username or password.</p>
    {% endif %}

    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Login</button>
    </form>
</body>
</html>
```

## Root URLs with authentication

```python
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    path("students/", include("students.urls")),
    path("polls/", include("polls.urls")),
]
```

Logout-এর জন্য POST form ব্যবহার করুন:

```html
<form method="post" action="{% url 'logout' %}">
    {% csrf_token %}
    <button type="submit">Logout</button>
</form>
```

---

# 15. Duplicate Vote Prevention

শুধু `Choice.votes` integer field রাখলে কে ভোট দিয়েছে তা জানা যায় না।

তাই `Vote` model দরকার।

## UniqueConstraint

```python
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=["question", "user"],
            name="unique_user_vote_per_question",
        ),
    ]
```

এটি একই user-এর জন্য একই question-এ একাধিক vote record প্রতিরোধ করে।

## কেন শুধু view-level check যথেষ্ট নয়?

নিচের code একা নির্ভরযোগ্য নয়:

```python
if not Vote.objects.filter(
    question=question,
    user=request.user,
).exists():
    Vote.objects.create(
        question=question,
        choice=choice,
        user=request.user,
    )
```

দুটি concurrent request একই সময়ে `exists()`-এ false পেতে পারে। তারপর দুটিই vote তৈরি করার চেষ্টা করবে।

সঠিক সমাধান:

- Database uniqueness constraint।
- `transaction.atomic()`।
- `IntegrityError` handling।

## Database constraint-এর গুরুত্বপূর্ণ সীমা

Unique constraint নিশ্চিত করে একই question ও user-এর জন্য একাধিক vote row তৈরি হবে না। কিন্তু constraint নিজে নিশ্চিত করে না যে `choice.question_id` এবং `question_id` সবসময় একই হবে।

তাই view-তে এই validation অপরিহার্য:

```python
choice = Choice.objects.filter(
    pk=choice_id,
    question=question,
).first()

if choice is None:
    # Reject the request.
    ...
```

অধিক কঠোর database-level enforcement চাইলে schema-তে উপযুক্ত composite foreign key বা database-specific constraint বিবেচনা করা যায়।

---

# 16. Transactions and F Expressions

## F expression

```python
from django.db.models import F

Choice.objects.filter(pk=choice.pk).update(
    votes=F("votes") + 1
)
```

এটি Python-এ পুরোনো vote count পড়ে পরিবর্তন করার বদলে database-কে সরাসরি increment করতে বলে।

## Race condition example

ধরা যাক, count হলো 10।

দুটি request একসঙ্গে count পড়ে 10 এবং দুইটিই 11 save করে। একটি increment হারিয়ে যায়।

Database-side update:

```python
Choice.objects.filter(pk=choice.pk).update(
    votes=F("votes") + 1
)
```

দুটি increment-ই database-এ প্রয়োগ হয়।

## transaction.atomic()

```python
from django.db import transaction

with transaction.atomic():
    Vote.objects.create(
        question=question,
        choice=choice,
        user=request.user,
    )

    Choice.objects.filter(pk=choice.pk).update(
        votes=F("votes") + 1
    )
```

দুটি operation একই transaction-এ থাকে। Exception হলে transaction rollback হয়।

---

# 17. Security Best Practices

1. **CSRF:** সব state-changing HTML form-এ `{% csrf_token %}` রাখুন।
2. **Authentication:** প্রয়োজনীয় endpoint-এ login বাধ্যতামূলক করুন।
3. **Authorization:** User-এর permission server-side যাচাই করুন।
4. **Input validation:** ModelForm বা Django forms ব্যবহার করুন।
5. **SQL injection:** Parameterized SQL বা ORM ব্যবহার করুন।
6. **Object validation:** Choice সংশ্লিষ্ট question-এর কি না যাচাই করুন।
7. **Duplicate voting:** Database `UniqueConstraint` ব্যবহার করুন।
8. **Atomic operations:** Vote record ও counter update একই transaction-এ রাখুন।
9. **GET requests:** Delete বা vote-এর মতো state-changing operation GET-এ করবেন না।
10. **Secrets:** `SECRET_KEY`, database password ও API keys source control-এ রাখবেন না।
11. **Production:** `DEBUG=False`, সঠিক `ALLOWED_HOSTS`, HTTPS ও secure cookie settings ব্যবহার করুন।
12. **Error handling:** Sensitive traceback বা credentials user-কে দেখাবেন না।
13. **Testing:** Valid input, invalid IDs, anonymous user ও duplicate requests পরীক্ষা করুন।
14. **Authorization scope:** User শুধু নিজের অনুমোদিত object পরিবর্তন করতে পারছেন কি না যাচাই করুন।
15. **Vote integrity:** Vote count ও vote records-এর মধ্যে consistency বজায় রাখুন।

---

# 18. Admin Configuration

`polls/admin.py`:

```python
from django.contrib import admin
from .models import Choice, Question, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date"]
    search_fields = ["question_text"]
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "question", "votes"]
    list_filter = ["question"]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["user", "question", "choice", "created_at"]
    readonly_fields = ["user", "question", "choice", "created_at"]
```

`students/admin.py`:

```python
from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "firstname",
        "surname",
        "age",
        "classroom",
    ]
    search_fields = ["firstname", "surname"]
    list_filter = ["classroom"]
```

Create superuser:

```bash
python manage.py createsuperuser
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

---

# 19. Automated Testing

Django-এর `TestCase` দিয়ে database operations, views, URLs এবং permissions পরীক্ষা করা যায়।

## 19.1 Polls tests

`polls/tests.py`:

```python
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .models import Choice, Question, Vote

User = get_user_model()


class PollVotingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            password="StrongTestPassword123!",
        )

        self.question = Question.objects.create(
            question_text="Which language do you prefer?"
        )

        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Python",
        )

        self.other_question = Question.objects.create(
            question_text="Which framework do you prefer?"
        )

        self.other_choice = Choice.objects.create(
            question=self.other_question,
            choice_text="Django",
        )

        self.vote_url = reverse(
            "polls:vote",
            args=[self.question.pk],
        )

    def test_authenticated_user_can_vote(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.vote_url,
            {"choice": self.choice.pk},
        )

        self.assertEqual(response.status_code, 302)

        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)

        self.assertEqual(
            Vote.objects.filter(
                question=self.question,
                user=self.user,
            ).count(),
            1,
        )

    def test_duplicate_vote_returns_conflict(self):
        self.client.force_login(self.user)

        self.client.post(
            self.vote_url,
            {"choice": self.choice.pk},
        )

        response = self.client.post(
            self.vote_url,
            {"choice": self.choice.pk},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 409)
        self.assertFalse(response.json()["success"])

        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)

    def test_invalid_choice_is_rejected(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.vote_url,
            {"choice": self.other_choice.pk},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Vote.objects.count(), 0)

    def test_missing_choice_is_rejected(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.vote_url,
            {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 400)

    def test_anonymous_user_cannot_vote(self):
        response = self.client.post(
            self.vote_url,
            {"choice": self.choice.pk},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Vote.objects.count(), 0)

    def test_database_unique_constraint(self):
        Vote.objects.create(
            question=self.question,
            choice=self.choice,
            user=self.user,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vote.objects.create(
                    question=self.question,
                    choice=self.choice,
                    user=self.user,
                )
```

## 19.2 Run tests

```bash
python manage.py test polls
python manage.py test students
python manage.py test
```

**Note:** Database uniqueness constraint test transaction-aware database backend-এ চালানো উচিত। Production database-এ concurrency behaviour যাচাই করতে integration test প্রয়োজন হতে পারে।

---

# 20. Common Errors and Solutions

| Error | কারণ | সমাধান |
|---|---|---|
| `TemplateDoesNotExist` | Template path ভুল | Template location ও `template_name` পরীক্ষা করুন |
| `NoReverseMatch` | URL name বা argument ভুল | `app_name`, route name এবং `pk` পরীক্ষা করুন |
| `TypeError: unexpected keyword argument` | URL parameter ও view argument mismatch | URL ও method-এর argument একই করুন |
| `405 Method Not Allowed` | Unsupported HTTP method | সঠিক method ব্যবহার করুন |
| `403 CSRF verification failed` | CSRF token অনুপস্থিত বা invalid | Form-এ `{% csrf_token %}` রাখুন |
| `404 Not Found` | Object বা URL পাওয়া যায়নি | URL ও primary key পরীক্ষা করুন |
| `OperationalError: no such table` | Migration প্রয়োগ করা হয়নি | `makemigrations` ও `migrate` চালান |
| `NameError: is_ajax` | Variable define করা হয়নি | Request header পরীক্ষা করে `ajax` variable তৈরি করুন |
| `IntegrityError` | Duplicate vote constraint | Error handle করে conflict response দিন |
| AJAX HTML response পাচ্ছে | Redirect বা error page এসেছে | Network tab ও response status পরীক্ষা করুন |
| `403 Permission Denied` | প্রয়োজনীয় permission নেই | User-কে উপযুক্ত permission দিন |
| Vote count mismatch | Counter ও vote records inconsistent | Atomic updates বা aggregate count ব্যবহার করুন |

---

# 21. Interview Questions and Answers

### 1. What is Django CRUD?

CRUD means Create, Read, Update and Delete. These are the four basic operations for managing database records.

### 2. What is a Class-Based View?

A Class-Based View is a Django view implemented using a Python class, with request handlers such as `get()` and `post()`.

### 3. What does `as_view()` do?

It returns a callable view function that Django can register in URL configuration.

### 4. What is `dispatch()`?

It routes a request to the appropriate handler based on the HTTP method.

### 5. What is the difference between FBV and CBV?

FBVs use functions, while CBVs use classes. CBVs support inheritance, mixins and reusable generic views.

### 6. What is `ListView`?

A generic view for displaying a collection of objects.

### 7. What is `DetailView`?

A generic view for displaying one object.

### 8. What is `ModelForm`?

A form automatically generated from a Django model. It supports field validation and model instance creation or update.

### 9. What is `get_object_or_404()`?

It returns an object if found; otherwise, it raises an HTTP 404 response.

### 10. What is a QuerySet?

A QuerySet represents a collection of database objects and supports filtering, ordering and other query operations.

### 11. What is a ForeignKey?

A field that represents a many-to-one relationship between models.

### 12. What does `on_delete=models.CASCADE` mean?

Deleting the referenced object also deletes related objects that use this deletion rule.

### 13. What are migrations?

Migrations describe and apply changes to a database schema.

### 14. What is AJAX?

AJAX is a technique for sending asynchronous requests and updating part of a web page without a full reload.

### 15. What is `JsonResponse`?

A Django response class that serializes Python data, commonly a dictionary, into JSON.

### 16. Why use `event.preventDefault()`?

It prevents the browser's default form submission so JavaScript can send the request.

### 17. What does `FormData` do?

It collects form fields into a format suitable for HTTP submission.

### 18. What is CSRF?

Cross-Site Request Forgery is an attack that attempts to make a browser submit an unwanted authenticated request.

### 19. Does AJAX prevent duplicate voting?

No. AJAX is a communication technique, not a duplicate-voting security mechanism.

### 20. Why use `UniqueConstraint`?

It enforces uniqueness at the database level, including when multiple requests race to create duplicate records.

### 21. Why use `transaction.atomic()`?

It groups database operations so they commit together or roll back together on failure.

### 22. Why use `F("votes") + 1`?

It performs the increment in the database, reducing lost-update problems caused by stale Python-side values.

### 23. Why validate a choice against a question?

To prevent a client from submitting a valid choice ID belonging to a different question.

### 24. What is `LoginRequiredMixin`?

A mixin that requires a user to be authenticated before accessing a view.

### 25. What is `PermissionRequiredMixin`?

A mixin that checks whether the user has specified Django permissions.

### 26. Why should delete actions not use GET?

GET should retrieve information without changing server state. Delete operations should use a state-changing method such as POST or DELETE.

### 27. What is the difference between authentication and authorization?

Authentication establishes who the user is. Authorization determines what the user is allowed to do.

### 28. Why use automated tests?

Automated tests detect regressions and verify that views, validation, permissions and database constraints behave as intended.

### 29. What is the difference between `raw()` and ORM queries?

`raw()` executes raw SQL and maps rows to model instances. ORM queries use Django's query API and are preferable for most ordinary application queries.

### 30. How can vote-count consistency be maintained?

Update vote records and counters in the same transaction, or derive the count from vote records using database aggregation.

---

# 22. Quick Revision

```text
Django project           -> django-admin startproject
Django app               -> python manage.py startapp
Create migration         -> python manage.py makemigrations
Apply migration          -> python manage.py migrate
Run development server   -> python manage.py runserver

CBV URL registration     -> MyView.as_view()
GET handler              -> get(self, request, ...)
POST handler             -> post(self, request, ...)

Generic list             -> ListView
Generic detail           -> DetailView
Generic create           -> CreateView
Generic update           -> UpdateView
Generic delete           -> DeleteView

Form validation          -> ModelForm
Missing object           -> get_object_or_404()
Login protection         -> LoginRequiredMixin
Permission checking      -> PermissionRequiredMixin

JSON response            -> JsonResponse(...)
AJAX request             -> fetch()
Form submission control  -> event.preventDefault()
Database increment       -> F("votes") + 1
Transaction              -> transaction.atomic()
Duplicate vote prevention-> UniqueConstraint
Database tests           -> TestCase
```

---

# 23. Practice Roadmap

## Beginner

- [ ] Create a Django project and app.
- [ ] Create the `Student` model.
- [ ] Run migrations.
- [ ] Implement FBV-based CRUD.
- [ ] Create templates and named URLs.
- [ ] Learn the Django ORM.

## Intermediate

- [ ] Convert Student CRUD to CBVs.
- [ ] Use `ModelForm` for validation.
- [ ] Implement `ListView`, `DetailView`, `CreateView` and `UpdateView`.
- [ ] Create `Question` and `Choice` models.
- [ ] Implement Poll index, detail and results pages.
- [ ] Add AJAX voting with JSON responses.
- [ ] Handle CSRF, invalid IDs and HTTP errors.

## Advanced

- [ ] Add authentication and permissions.
- [ ] Create a `Vote` model.
- [ ] Enforce duplicate-vote prevention using `UniqueConstraint`.
- [ ] Use `transaction.atomic()` and `F()` expressions.
- [ ] Write automated tests for valid and invalid requests.
- [ ] Add pagination and filtering.
- [ ] Use PostgreSQL and test concurrency behaviour.
- [ ] Add Django REST Framework API endpoints.
- [ ] Deploy with production security settings.

---

## Final Summary

এই project-এ Django CRUD, ORM, CBV, Generic Views, Polls, AJAX, JSON, authentication, permissions এবং database-level duplicate-vote prevention একসঙ্গে শেখা যাবে।

সবচেয়ে গুরুত্বপূর্ণ ধারণাগুলো হলো:

1. সাধারণ CRUD-এর জন্য ORM ও `ModelForm` ব্যবহার করুন।
2. Reusable request handling-এর জন্য CBV ও generic views শিখুন।
3. AJAX-এর মাধ্যমে page reload ছাড়াই server-এর সঙ্গে যোগাযোগ করুন।
4. Authentication, authorization ও CSRF সুরক্ষা server-side-এ প্রয়োগ করুন।
5. Duplicate voting প্রতিরোধে শুধু JavaScript নয়, database constraints ব্যবহার করুন।
6. Vote record ও vote counter-এর consistency বজায় রাখতে transaction এবং সঠিক testing ব্যবহার করুন।

**প্রস্তাবিত শেখার ক্রম:** প্রথমে Student CRUD সম্পূর্ণ করুন, এরপর Polls application তৈরি করুন, তারপর AJAX যোগ করুন এবং সবশেষে authentication, duplicate-vote prevention ও automated testing বাস্তবায়ন করুন।


