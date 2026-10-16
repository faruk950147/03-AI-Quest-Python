
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



## 1. What Are Class-Based Views?

Class-Based Views (CBV) are a way to handle HTTP requests in Django using Python classes instead of functions.

CBVs organize request-handling logic into methods such as `get()` and `post()`.

### Example

```python
from django.http import HttpResponse
from django.views import View


class HomeView(View):
    def get(self, request):
        return HttpResponse("Hello, Django CBV!")
```

### Explanation

- `View` is Django's built-in base class.
- `HomeView` is a custom view class.
- `get()` handles GET requests.
- `post()` handles POST requests.
- `request` contains incoming HTTP request information.
- `HttpResponse()` sends a response to the client.

## 2. FBV vs CBV

### Function-Based View (FBV)

```python
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello from FBV!")
```

### Class-Based View (CBV)

```python
from django.http import HttpResponse
from django.views import View


class HomeView(View):
    def get(self, request):
        return HttpResponse("Hello from CBV!")
```

### Differences

| FBV | CBV |
|---|---|
| Uses functions | Uses classes |
| Defined with `def` | Defined with `class` |
| Often checks `request.method` | Uses methods such as `get()` and `post()` |
| Simple logic can be concise | Supports inheritance and reusable logic |
| Uses function decorators | Supports method decorators and mixins |

Neither approach is always better. Choose according to the task.

## 3. Common HTTP Methods

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

    def patch(self, request):
        return HttpResponse("PATCH request")

    def delete(self, request):
        return HttpResponse("DELETE request")
```

- `get()` — Retrieves information.
- `post()` — Submits data or creates a resource.
- `put()` — Typically replaces a resource.
- `patch()` — Updates part of a resource.
- `delete()` — Deletes a resource.

Unsupported methods generally return HTTP 405.

## 4. URL Configuration and as_view()

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

`as_view()` converts the class into a callable that Django can use in URL configuration.

### Request Flow

Browser → URL Configuration → `as_view()` → `dispatch()` → `get()` or `post()` → Response

## 5. dispatch()

The `dispatch()` method routes requests to the appropriate handler.

- GET → `get()`
- POST → `post()`
- PUT → `put()`
- PATCH → `patch()`
- DELETE → `delete()`

Unsupported methods generally return HTTP 405 Method Not Allowed.

## 6. Important Generic CBVs

### 6.1 ListView

Displays multiple database objects.

```python
from django.views.generic import ListView
from .models import Question


class QuestionListView(ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "questions"
    ordering = ["-pub_date"]
    paginate_by = 10
```

Important attributes:

- `model` — Specifies the model.
- `template_name` — Specifies the template.
- `context_object_name` — Specifies the template variable.
- `ordering` — Defines the ordering.
- `paginate_by` — Sets the number of objects per page.

### 6.2 DetailView

Displays one object's details.

```python
from django.views.generic import DetailView
from .models import Question


class QuestionDetailView(DetailView):
    model = Question
    template_name = "polls/detail.html"
    context_object_name = "question"
```

By default, `DetailView` uses a `pk` URL parameter to retrieve an object.

### 6.3 CreateView

Creates a new object using a form.

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

- `fields` defines the form fields.
- Django handles standard form validation and saving.
- `success_url` specifies the redirect destination.

### 6.4 UpdateView

Updates an existing object.

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

### 6.5 DeleteView

Deletes an existing object.

```python
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import Question


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = "polls/question_confirm_delete.html"
    success_url = reverse_lazy("polls:index")
```

Deletion normally requires a POST request after displaying a confirmation page.

### 6.6 TemplateView

Renders a specified template.

```python
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "about.html"
```

### 6.7 RedirectView

Redirects users to another URL.

```python
from django.views.generic import RedirectView


class GoogleRedirectView(RedirectView):
    url = "https://www.google.com/"
    permanent = False
```

## 7. Important CBV Attributes and Methods

### model

```python
model = Question
```

Specifies the model used by a generic view.

### queryset

```python
queryset = Question.objects.order_by("-pub_date")
```

Specifies the queryset used by the view.

### get_queryset()

Customizes which objects are retrieved.

```python
class QuestionListView(ListView):
    model = Question

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")
```

### get_context_data()

Adds extra data to the template context.

```python
class QuestionListView(ListView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_questions"] = Question.objects.count()
        return context
```

### get_object()

Customizes object retrieval in generic detail and editing views.

### get_template_names()

Customizes which template is rendered.

### form_valid()

Customizes behavior after successful form validation.

```python
def form_valid(self, form):
    return super().form_valid(form)
```

### form_invalid()

Customizes behavior when form validation fails.

### get_form_kwargs()

Passes additional arguments to a form.

### reverse_lazy()

Resolves a named URL lazily.

```python
from django.urls import reverse_lazy

success_url = reverse_lazy("polls:index")
```

## 8. Create a Django Polls Project

### Step 1: Install Django

```bash
pip install django
django-admin startproject mysite
cd mysite
python manage.py startapp polls
```

### Step 2: Register the app

In `mysite/settings.py`, add `"polls"` to `INSTALLED_APPS`.

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

### Step 3: Create Models

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

### Model Explanation

- `Question` stores poll questions.
- `Choice` stores available choices.
- `ForeignKey` connects choices to questions.
- `on_delete=models.CASCADE` deletes related choices when a question is deleted.
- `related_name="choices"` allows `question.choices.all()`.
- `votes` stores the vote count.

### Step 4: Create Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Views

File: `polls/views.py`

```python
from django.db.models import F
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
                    "error_message": "Please select a choice.",
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
            "polls:results",
            pk=question.pk,
        )


class ResultsView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)

        return render(
            request,
            "polls/results.html",
            {"question": question},
        )
```

### Explanation

- `IndexView` displays questions.
- `QuestionDetailView` displays one question.
- `VoteView` handles submitted votes.
- `ResultsView` displays voting results.
- `get_object_or_404()` returns a 404 response if the object does not exist.
- `F("votes") + 1` increments the vote count in the database.
- Filtering by `question=question` ensures that the selected choice belongs to the requested question.

### Step 6: Configure URLs

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
    path("<int:pk>/", QuestionDetailView.as_view(), name="detail"),
    path(
        "<int:question_id>/vote/",
        VoteView.as_view(),
        name="vote",
    ),
    path("<int:pk>/results/", ResultsView.as_view(), name="results"),
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

### Step 7: Create Index Template

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

### Step 8: Create Detail Template

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
                    required
                >
                {{ choice.choice_text }}
            </label>
            <br>
        {% empty %}
            <p>No choices are available.</p>
        {% endfor %}

        {% if question.choices.exists %}
            <button type="submit">Vote</button>
        {% endif %}
    </form>

    <p>
        <a href="{% url 'polls:index' %}">View all questions</a>
    </p>
</body>
</html>
```

### Step 9: Create Results Template

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
                {{ choice.choice_text }} — {{ choice.votes }} votes
            </li>
        {% empty %}
            <li>No choices are available.</li>
        {% endfor %}
    </ul>

    <p>
        <a href="{% url 'polls:detail' question.pk %}">Vote again</a>
    </p>

    <p>
        <a href="{% url 'polls:index' %}">View all questions</a>
    </p>
</body>
</html>
```

### Step 10: Configure Django Admin

File: `polls/admin.py`

```python
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date")
    search_fields = ("question_text",)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "votes")
    list_filter = ("question",)
    search_fields = ("choice_text",)
```

### Step 11: Create Admin User

```bash
python manage.py createsuperuser
```

### Step 12: Run the Project

```bash
python manage.py runserver
```

URLs:

- Polls: `http://127.0.0.1:8000/polls/`
- Admin: `http://127.0.0.1:8000/admin/`

Create a question and choices in Django Admin before testing the voting application.

## 9. Authentication and Permissions

### LoginRequiredMixin

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Question


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
```

Requires the user to be logged in.

### PermissionRequiredMixin

```python
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from .models import Question


class QuestionListView(PermissionRequiredMixin, ListView):
    model = Question
    permission_required = "polls.view_question"
```

Requires the specified permission.

Important security practices:

- Validate submitted data on the server.
- Use CSRF tokens in POST forms.
- Apply authentication where needed.
- Check object-level permissions.
- Prevent unauthorized edits and deletions.
- Implement duplicate-vote prevention if the application requires it.

## 10. Common Errors

| Error | Possible cause |
|---|---|
| `TemplateDoesNotExist` | Incorrect template path |
| `NoReverseMatch` | Incorrect URL name or arguments |
| `TypeError` | Mismatched method parameters |
| `Http404` | Object not found |
| `405 Method Not Allowed` | Unsupported HTTP method |
| `ImproperlyConfigured` | Missing generic view configuration |
| CSRF verification failed | Missing or invalid CSRF token |

## 11. Interview Questions and Answers

**Q1. What is a CBV?**

A Django view implemented using a Python class and its methods.

**Q2. What does `as_view()` do?**

Converts a CBV into a callable for URL configuration.

**Q3. What is the difference between FBV and CBV?**

FBV uses a function; CBV uses a class and methods.

**Q4. What is `dispatch()`?**

Routes a request to the appropriate HTTP handler.

**Q5. What is `ListView`?**

A generic view for displaying multiple objects.

**Q6. What is `DetailView`?**

A generic view for displaying a single object.

**Q7. What is `CreateView`?**

A generic view for creating objects through forms.

**Q8. What is `UpdateView`?**

A generic view for updating existing objects.

**Q9. What is `DeleteView`?**

A generic view for deleting existing objects.

**Q10. What is `TemplateView`?**

A generic view for rendering a template.

**Q11. What is `context_object_name`?**

The variable name used to access the object or queryset in a template.

**Q12. What is `get_queryset()`?**

A method for customizing the objects retrieved by a generic view.

**Q13. What is `get_context_data()`?**

A method for adding extra template context.

**Q14. What is `reverse_lazy()`?**

A function that resolves a named URL lazily.

**Q15. What is `form_valid()`?**

A method for customizing successful form submission.

**Q16. What is `LoginRequiredMixin`?**

A mixin that restricts access to authenticated users.

**Q17. What is `get_object_or_404()`?**

Retrieves an object or returns an HTTP 404 response.

**Q18. What is an `F()` expression?**

It allows database operations to reference existing field values directly.

**Q19. Does `F()` prevent duplicate voting?**

No. It helps with atomic database updates but does not prevent repeated votes.

**Q20. When should FBV be used?**

FBV is often suitable for simple, straightforward request-handling logic.

## 12. Quick Revision

| CBV | Purpose |
|---|---|
| `View` | Custom request handling |
| `ListView` | List objects |
| `DetailView` | Display one object |
| `CreateView` | Create objects |
| `UpdateView` | Update objects |
| `DeleteView` | Delete objects |
| `TemplateView` | Render templates |
| `RedirectView` | Redirect |
| `get_queryset()` | Customize queries |
| `get_context_data()` | Add context |
| `get_object()` | Customize object retrieval |
| `form_valid()` | Handle valid forms |
| `reverse_lazy()` | Lazy URL resolution |
| `LoginRequiredMixin` | Require login |
| `PermissionRequiredMixin` | Require permissions |
| `F()` | Database field operations |

## 13. Practice Roadmap

1. Build a Home page using `View`.
2. Practice `get()` and `post()`.
3. Create a Blog using `ListView` and `DetailView`.
4. Add `CreateView`, `UpdateView`, and `DeleteView`.
5. Add authentication and permissions.
6. Implement search and pagination.
7. Build a complete Blog CRUD application.
8. Practice explaining each concept in an interview.

## Final Note

First master `View`, `as_view()`, `dispatch()`, `get()`, and `post()`. Then learn `ListView`, `DetailView`, `CreateView`, `UpdateView`, and `DeleteView`.

These concepts are useful for building maintainable Django applications and preparing for backend developer interviews.
