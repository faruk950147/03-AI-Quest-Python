# 1 Django Raw Queries
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
        


# 2. Interview Questions and Answers

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


