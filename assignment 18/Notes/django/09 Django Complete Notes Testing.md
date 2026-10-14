# Django Complete Notes: Testing

**Django Version:** 6.0  
**Level:** Beginner to Advanced  
**Topics:** Unit Testing, Models, Views, Forms, APIs, Authentication, Database Testing, Mocking, and Advanced Testing

# Part 1: Introduction to Django Testing

## 1. What Is Testing?

**Testing** is the process of checking whether software behaves as expected.

In Django, testing helps verify that models, views, forms, APIs, authentication, and database operations work correctly.

For example, suppose you build a Student Management API. Tests can check whether:

- A student is created successfully.
- The correct student data is returned.
- Invalid input produces validation errors.
- An unauthenticated user is denied access to a protected endpoint.
- Updating a student changes the correct database record.
- Deleting a student removes the record.

### Why Is Testing Important?

1. Detects bugs early.
2. Prevents existing functionality from breaking.
3. Verifies business logic.
4. Improves code quality.
5. Makes refactoring safer.
6. Helps maintain API reliability.
7. Supports continuous integration and deployment.

## 2. Types of Software Testing

### 2.1 Unit Testing

Unit testing checks a small, isolated part of an application, such as a function or method.

Example:

```python
def add(a, b):
    return a + b
```

Test:

```python
from django.test import SimpleTestCase


class MathTest(SimpleTestCase):

    def test_add(self):
        self.assertEqual(add(10, 20), 30)
```

This test checks whether `add()` returns the expected result.

### 2.2 Integration Testing

Integration testing checks whether multiple parts of an application work together.

Examples:

- A view saves data through a model.
- A form validates input before saving.
- An API endpoint reads data from the database.

### 2.3 Functional Testing

Functional testing checks whether a feature behaves according to its requirements.

For example, testing whether a login endpoint accepts valid credentials and rejects invalid credentials.

### 2.4 Regression Testing

Regression testing ensures that new code changes do not break existing functionality.

For example, after modifying the Student model, previously working student creation and retrieval tests should still pass.

### 2.5 End-to-End Testing

End-to-end testing checks a complete user workflow, potentially through a real browser.

Examples:

- A user opens a login page.
- Enters credentials.
- Logs in successfully.
- Opens the dashboard.

Django's test client is useful for testing requests and responses, while tools such as Selenium are suitable for browser-level testing.

## 3. Django Testing Framework

Django provides a built-in testing framework based on Python's `unittest` module.

Important tools include:

| Tool | Purpose |
|---|---|
| `SimpleTestCase` | Tests that do not need database access |
| `TestCase` | Tests application behavior involving the database |
| `TransactionTestCase` | Tests transaction behavior and database commits |
| `Client` | Simulates HTTP requests to a Django application |
| `RequestFactory` | Creates request objects for direct view testing |
| `AsyncClient` | Makes asynchronous test requests |
| `override_settings` | Temporarily overrides Django settings |
| `mock` | Replaces dependencies with controlled test objects |

Official documentation:

- [Django Testing Overview](https://docs.djangoproject.com/en/6.0/topics/testing/overview/)
- [Django Testing Tools](https://docs.djangoproject.com/en/6.0/topics/testing/tools/)
- [Advanced Testing Topics](https://docs.djangoproject.com/en/6.0/topics/testing/advanced/)

# Part 2: Writing and Running Tests

## 4. Where Should Tests Be Written?

Django discovers test files whose names match the default pattern `test*.py`.

For a small application, you can write tests in `tests.py`.

Example project structure:

```text
myproject/
├── manage.py
├── myproject/
│   ├── settings.py
│   └── urls.py
└── students/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── tests.py
    └── migrations/
```

For a larger application, you can organize tests into a directory:

```text
students/
├── models.py
├── views.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_forms.py
│   └── test_api.py
```

Each test module should contain relevant test classes and functions.

## 5. Writing Your First Test

Create `students/tests.py`:

```python
from django.test import SimpleTestCase


class MathTestCase(SimpleTestCase):

    def test_addition(self):
        result = 10 + 20

        self.assertEqual(result, 30)

    def test_subtraction(self):
        result = 20 - 10

        self.assertEqual(result, 10)
```

Run the tests:

```bash
python manage.py test
```

Run tests for a specific application:

```bash
python manage.py test students
```

Run a particular test class:

```bash
python manage.py test students.tests.MathTestCase
```

Run a particular test method:

```bash
python manage.py test students.tests.MathTestCase.test_addition
```

### Example Output

```text
Found 2 test(s).
System check identified no issues.
..
Ran 2 tests
OK
```

The dots indicate successful tests.

If a test fails, Django reports the assertion failure or error.

**Important:** A passing test indicates that the tested behavior met its assertions. It does not prove that the entire application is bug-free.

## 6. Test Method Naming

Test methods should normally begin with `test_`.

Correct:

```python
def test_student_creation(self):
    ...
```

Incorrect for automatic test discovery:

```python
def student_creation(self):
    ...
```

The `test_` prefix helps Django and Python's test discovery identify test methods.

## 7. Assertions

Assertions compare actual results with expected results.

Common assertions include:

| Assertion | Purpose |
|---|---|
| `assertEqual(a, b)` | Checks whether values are equal |
| `assertNotEqual(a, b)` | Checks whether values differ |
| `assertTrue(x)` | Checks whether a value is truthy |
| `assertFalse(x)` | Checks whether a value is falsy |
| `assertIsNone(x)` | Checks whether a value is `None` |
| `assertIsNotNone(x)` | Checks whether a value is not `None` |
| `assertIn(a, b)` | Checks whether `a` is in `b` |
| `assertNotIn(a, b)` | Checks whether `a` is not in `b` |
| `assertRaises(Error)` | Checks whether an exception is raised |
| `assertContains(response, text)` | Checks whether a response contains content |
| `assertRedirects(response, url)` | Checks whether a response redirects correctly |
| `assertTemplateUsed(response, template)` | Checks whether a template was used |

Example:

```python
from django.test import SimpleTestCase


class AssertionTestCase(SimpleTestCase):

    def test_assertions(self):
        self.assertEqual(10 + 5, 15)
        self.assertNotEqual(10, 20)
        self.assertTrue(5 > 2)
        self.assertFalse(5 < 2)
        self.assertIsNone(None)
        self.assertIn("Django", "Learn Django Testing")
```

Testing an exception:

```python
def divide(a, b):
    return a / b


class DivisionTestCase(SimpleTestCase):

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)
```

## 8. setUp() and tearDown()

`setUp()` runs before each test method.

`tearDown()` runs after a test method finishes, including when the test fails, provided setup completed far enough for teardown to run.

Example:

```python
from django.test import SimpleTestCase


class ExampleTestCase(SimpleTestCase):

    def setUp(self):
        self.name = "Omar"

    def test_name(self):
        self.assertEqual(self.name, "Omar")

    def test_name_type(self):
        self.assertIsInstance(self.name, str)

    def tearDown(self):
        pass
```

Each test receives a fresh value initialized by `setUp()`.

Use `tearDown()` when cleanup is necessary. For resources that support context managers, `addCleanup()` can also be useful.

## 9. setUpTestData()

`setUpTestData()` is available on Django's database-aware test case classes, including `TestCase`.

It creates class-level test data once for the test class, rather than repeating the same database setup for every test method.

Example:

```python
from django.test import TestCase
from students.models import Student


class StudentTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.student = Student.objects.create(
            name="Omar",
            age=22,
        )

    def test_student_name(self):
        self.assertEqual(self.student.name, "Omar")

    def test_student_age(self):
        self.assertEqual(self.student.age, 22)
```

Use `setUpTestData()` for shared database data that does not need to be recreated before every test.

Use `setUp()` when each test needs fresh mutable objects or individual setup behavior.

# Part 3: Testing Models

## 10. What Is Model Testing?

Model testing verifies database-backed model behavior.

Examples:

- Creating records.
- Checking field values.
- Testing model methods.
- Checking default values.
- Testing relationships.
- Testing database constraints.

Suppose `students/models.py` contains:

```python
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def is_adult(self):
        return self.age >= 18

    def __str__(self):
        return self.name
```

### Test the Model

Create `students/tests.py`:

```python
from django.test import TestCase
from students.models import Student


class StudentModelTestCase(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            name="Omar",
            age=22,
        )

    def test_student_creation(self):
        self.assertEqual(Student.objects.count(), 1)

    def test_student_name(self):
        self.assertEqual(self.student.name, "Omar")

    def test_student_age(self):
        self.assertEqual(self.student.age, 22)

    def test_student_is_adult(self):
        self.assertTrue(self.student.is_adult())

    def test_student_string_representation(self):
        self.assertEqual(str(self.student), "Omar")
```

Run:

```bash
python manage.py test students
```

**Note:** This example assumes the `Student` model is defined in the `students` app and its migrations are available.

## 11. Why Use TestCase for Models?

`TestCase` supports database operations and isolates test data.

Django creates a separate test database for the test run when needed. It does not normally run these tests against your regular development database.

At the end of each test, Django rolls back the test transaction to restore database isolation.

Do not use `SimpleTestCase` for tests that query or modify the database. It disallows database access by default.

# Part 4: Testing Views and URLs

## 12. What Is View Testing?

View testing verifies whether a Django view responds correctly to an HTTP request.

It can check:

- HTTP status codes.
- Response content.
- Redirects.
- Templates.
- Context data.
- Authentication requirements.
- Database changes caused by a request.

Suppose `students/views.py` contains:

```python
from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to Django")
```

And `students/urls.py` contains:

```python
from django.urls import path
from .views import home

urlpatterns = [
    path("", home, name="home"),
]
```

The project's main `urls.py` should include the app URLs:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("students/", include("students.urls")),
]
```

### Test the View

```python
from django.test import TestCase
from django.urls import reverse


class HomeViewTestCase(TestCase):

    def test_home_page(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Django")
```

The URL configuration must make the `home` URL name available for `reverse("home")`. If it is namespaced, use its full name, such as `students:home`.

## 13. Common HTTP Status Codes

| Status code | Meaning |
|---|---|
| `200` | OK |
| `201` | Created |
| `204` | No Content |
| `301` | Permanent Redirect |
| `302` | Temporary Redirect |
| `400` | Bad Request |
| `401` | Unauthorized |
| `403` | Forbidden |
| `404` | Not Found |
| `405` | Method Not Allowed |
| `409` | Conflict |
| `500` | Internal Server Error |

The correct status code depends on the application's behavior and API design.

## 14. Testing Redirects

Suppose a view redirects to another URL.

```python
from django.shortcuts import redirect


def dashboard(request):
    return redirect("home")
```

Test:

```python
def test_dashboard_redirect(self):
    response = self.client.get("/dashboard/")

    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, "/students/")
```

This example assumes `/dashboard/` redirects to the URL configured for `home`, which is `/students/`.

`assertRedirects()` also checks the destination response by default. Its behavior can be adjusted when testing external or non-followable destinations.

## 15. Testing Templates

Suppose a view renders a template:

```python
from django.shortcuts import render


def student_page(request):
    return render(
        request,
        "students/student.html",
        {"name": "Omar"},
    )
```

Test:

```python
def test_student_template(self):
    response = self.client.get("/students/profile/")

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(
        response,
        "students/student.html",
    )
    self.assertEqual(response.context["name"], "Omar")
```

The test assumes the corresponding URL and template exist.

# Part 5: Django Test Client

## 16. What Is the Test Client?

`django.test.Client` acts like a lightweight, programmatic browser for testing Django applications.

It sends requests through Django's request-handling machinery without requiring a running web server.

Django's `TestCase` provides a ready-to-use client through `self.client`.

Example:

```python
response = self.client.get("/students/")

print(response.status_code)
print(response.content)
```

Common client methods:

| Method | Purpose |
|---|---|
| `get()` | Sends a GET request |
| `post()` | Sends a POST request |
| `put()` | Sends a PUT request |
| `patch()` | Sends a PATCH request |
| `delete()` | Sends a DELETE request |
| `head()` | Sends a HEAD request |
| `options()` | Sends an OPTIONS request |

Use URL paths, such as `/students/`, rather than complete external website URLs.

## 17. Testing GET Requests

```python
def test_get_students(self):
    response = self.client.get("/students/")

    self.assertEqual(response.status_code, 200)
```

A GET request commonly retrieves information.

## 18. Testing POST Requests

Suppose a view accepts a form submission.

```python
response = self.client.post(
    "/students/create/",
    {
        "name": "Omar",
        "age": 22,
    },
)
```

You can verify the response:

```python
self.assertIn(response.status_code, [200, 302])
```

However, tests should ideally assert the exact expected status code based on the view's documented behavior.

For example, if successful submission redirects, assert `302` and the redirect destination.

## 19. Testing JSON Responses

Suppose an API returns JSON:

```python
from django.http import JsonResponse


def student_api(request):
    return JsonResponse({
        "name": "Omar",
        "age": 22,
    })
```

Test:

```python
def test_student_json(self):
    response = self.client.get("/api/student/")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(
        response.json(),
        {"name": "Omar", "age": 22},
    )
```

`response.json()` parses a JSON response into Python objects.

## 20. Following Redirects

The test client can follow redirects:

```python
response = self.client.get(
    "/dashboard/",
    follow=True,
)
```

Then inspect:

```python
self.assertEqual(response.status_code, 200)
```

When `follow=True` is used, `response.redirect_chain` contains redirect information.

# Part 6: Testing Forms

## 21. What Is Form Testing?

Form testing verifies:

- Required fields.
- Input validation.
- Invalid data handling.
- Custom validation methods.
- Cleaned data.
- Error messages.

Example form in `students/forms.py`:

```python
from django import forms


class StudentForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(min_value=1, max_value=120)
```

### Test Valid Data

```python
from django.test import SimpleTestCase
from students.forms import StudentForm


class StudentFormTestCase(SimpleTestCase):

    def test_valid_form(self):
        form = StudentForm(data={
            "name": "Omar",
            "age": 22,
        })

        self.assertTrue(form.is_valid())
```

### Test Invalid Data

```python
def test_invalid_age(self):
    form = StudentForm(data={
        "name": "Omar",
        "age": -5,
    })

    self.assertFalse(form.is_valid())
    self.assertIn("age", form.errors)
```

### Test Missing Required Fields

```python
def test_missing_name(self):
    form = StudentForm(data={
        "age": 22,
    })

    self.assertFalse(form.is_valid())
    self.assertIn("name", form.errors)
```

Use `SimpleTestCase` for forms that do not query the database. Use a database-aware test case if form validation depends on database queries.

# Part 7: Testing Authentication and Permissions

## 22. Creating a Test User

Django provides helpers for creating users during tests.

```python
from django.contrib.auth.models import User
from django.test import TestCase


class AuthenticationTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="omar",
            password="test-password-123",
        )
```

Use `create_user()` rather than directly assigning a plain-text password.

## 23. Testing Login

```python
def test_login(self):
    logged_in = self.client.login(
        username="omar",
        password="test-password-123",
    )

    self.assertTrue(logged_in)
```

`client.login()` tests Django's authentication system and establishes the client's authenticated session when successful.

## 24. Testing a Protected View

Suppose the view requires login:

```python
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def dashboard(request):
    return HttpResponse("Private dashboard")
```

Test anonymous access:

```python
def test_anonymous_user_redirected(self):
    response = self.client.get("/dashboard/")

    self.assertEqual(response.status_code, 302)
```

Test authenticated access:

```python
def test_authenticated_user_can_access(self):
    self.client.force_login(self.user)

    response = self.client.get("/dashboard/")

    self.assertEqual(response.status_code, 200)
```

`force_login()` is useful when the test needs an authenticated user without testing the login credential flow itself.

## 25. Testing Permissions

Authentication asks whether a user is logged in.

Authorization asks whether that user is allowed to perform an action.

Tests should verify both where relevant:

- Anonymous users cannot access protected resources.
- Authenticated users without permission are denied.
- Authorized users can perform permitted actions.

For a permission-protected view, the expected response may be `403 Forbidden` or a redirect, depending on the implementation.

# Part 8: Testing APIs

## 26. Testing a Django REST Framework API

If your project uses Django REST Framework (DRF), it provides additional testing tools, including `APIClient` and `APITestCase`.

Install DRF if your project needs it:

```bash
pip install djangorestframework
```

A basic API test can look like this:

```python
from rest_framework.test import APITestCase
from rest_framework import status


class StudentAPITestCase(APITestCase):

    def test_api_endpoint(self):
        response = self.client.get("/api/students/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
```

This example assumes the endpoint exists and permits anonymous access.

For a DRF-specific client:

```python
from rest_framework.test import APIClient

client = APIClient()
response = client.get("/api/students/")
```

DRF's `APIClient` supports API-oriented request formats, including JSON.

## 27. Testing API POST Requests

Example:

```python
response = self.client.post(
    "/api/students/",
    {
        "name": "Omar",
        "age": 22,
    },
    format="json",
)
```

Check the result:

```python
self.assertEqual(response.status_code, 201)
```

Use `format="json"` with DRF's test client when the endpoint expects JSON. This example assumes the API creates a resource and returns `201 Created`.

## 28. Testing API Validation

Test invalid input:

```python
response = self.client.post(
    "/api/students/",
    {
        "name": "",
        "age": -1,
    },
    format="json",
)

self.assertEqual(response.status_code, 400)
```

This expects the API serializer to reject an empty name and negative age. The exact response depends on the serializer and validation rules.

## 29. Testing API Authentication

DRF's `APIClient` supports methods such as:

```python
self.client.force_authenticate(user=self.user)
```

Example:

```python
def test_authenticated_api_access(self):
    self.client.force_authenticate(user=self.user)

    response = self.client.get("/api/private/")

    self.assertEqual(response.status_code, 200)
```

This assumes the endpoint allows the test user to access it.

`force_authenticate()` bypasses the normal authentication mechanism for the test. Use separate tests for actual authentication mechanisms, such as session or token authentication.

# Part 9: Testing File Uploads

## 30. Testing File Uploads

Django's test client can submit uploaded files.

For example, if a form accepts a file:

```python
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class FileUploadTestCase(TestCase):

    def test_upload_text_file(self):
        uploaded_file = SimpleUploadedFile(
            "hello.txt",
            b"Hello Django",
            content_type="text/plain",
        )

        response = self.client.post(
            "/upload/",
            {"file": uploaded_file},
        )

        self.assertIn(response.status_code, [200, 302])
```

The endpoint must exist and accept the `file` field. In a real test, assert the exact expected response and verify the saved file or database record.

**Important:** The supplied `content_type` is only a declaration; it does not prove that the uploaded file's contents are safe.

For image uploads, Django also provides `SimpleUploadedFile`. A valid image fixture should contain actual image data if the application validates image contents.

# Part 10: Testing Tools and Advanced Concepts

## 31. TestCase vs SimpleTestCase vs TransactionTestCase

| Class | Database access | Main purpose |
|---|---|---|
| `SimpleTestCase` | Disallowed by default | Tests without database access |
| `TestCase` | Supported | Most model and view tests |
| `TransactionTestCase` | Supported | Tests involving actual transaction behavior |

### SimpleTestCase

Use for pure logic, basic form validation, and other tests that do not need the database.

### TestCase

Use for most Django tests that create, read, update, or delete database records.

Django uses transactions to provide isolation and improve performance.

### TransactionTestCase

Use when you need to observe actual commit and rollback behavior or test certain transaction-sensitive database features.

It resets database state differently from `TestCase`, so it is usually slower.

## 32. RequestFactory

`RequestFactory` creates request objects for directly testing views.

Unlike the test client, it does not run the full middleware and URL-routing process.

Example:

```python
from django.test import RequestFactory, TestCase
from students.views import home


class RequestFactoryTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_home_view(self):
        request = self.factory.get("/")

        response = home(request)

        self.assertEqual(response.status_code, 200)
```

Use `RequestFactory` when you want to test a view directly.

If the view depends on middleware-provided attributes, such as `request.user`, you may need to supply them manually.

## 33. Client vs RequestFactory

| Feature | Client | RequestFactory |
|---|---|---|
| Simulates HTTP requests | Yes | Creates request objects |
| Runs URL routing | Yes | No |
| Runs middleware | Yes | No |
| Useful for end-to-end request handling within Django | Yes | No |
| Calls a view directly | Indirectly | Yes |
| Supports response and redirect checks | Yes | Yes, after invoking the view |

For most application-level view tests, start with `self.client`. Use `RequestFactory` when direct view testing is more appropriate.

## 34. Testing with Fixtures

A **fixture** is a collection of serialized data that Django can load into a database.

Fixtures are useful when tests need a predefined set of records.

Example:

```python
from django.test import TestCase


class StudentFixtureTestCase(TestCase):

    fixtures = ["students.json"]

    def test_fixture_data(self):
        ...
```

The fixture must exist in a location Django recognizes, and its contents must match the model structure.

For many tests, creating objects through `setUpTestData()` is easier to read and maintain than relying on large fixture files.

## 35. Mocking in Tests

**Mocking** replaces a dependency with a controlled object so a test can focus on the behavior being tested.

It is useful for:

- External API calls.
- Email delivery.
- Payment gateways.
- Slow or unreliable services.
- Time-dependent logic.

Example:

```python
from unittest.mock import patch
from django.test import SimpleTestCase


class EmailTestCase(SimpleTestCase):

    @patch("students.services.send_email")
    def test_email_service(self, mock_send_email):
        from students.services import notify_student

        notify_student("omar@example.com")

        mock_send_email.assert_called_once()
```

This example assumes `notify_student()` calls `send_email` inside `students.services`.

**Important:** Patch the name where the code under test looks it up, not necessarily the module where the original function was first defined.

## 36. override_settings

`override_settings` temporarily changes Django settings for a test.

Example:

```python
from django.test import SimpleTestCase, override_settings


@override_settings(DEBUG=False)
class SettingsTestCase(SimpleTestCase):

    def test_debug_disabled(self):
        from django.conf import settings

        self.assertFalse(settings.DEBUG)
```

It can also be applied to individual test methods.

Use it to test behavior under different configuration values without permanently changing project settings.

## 37. Testing Emails

Django's test environment provides an in-memory email outbox for the configured test email backend.

Example:

```python
from django.core import mail
from django.test import TestCase


class EmailTestCase(TestCase):

    def test_send_email(self):
        mail.send_mail(
            subject="Welcome",
            message="Welcome to Django",
            from_email="noreply@example.com",
            recipient_list=["omar@example.com"],
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "Welcome",
        )
```

This checks that the email was generated by Django's test email backend. It does not verify delivery by an external email provider.

## 38. Testing Asynchronous Code

Django supports testing asynchronous views and code.

For asynchronous test methods, use `async def`. Django detects these methods and runs them in an asynchronous test context.

Example:

```python
from django.test import TestCase


class AsyncTestCase(TestCase):

    async def test_async_request(self):
        response = await self.async_client.get("/")

        self.assertEqual(response.status_code, 200)
```

`self.async_client` is Django's asynchronous test client.

Use `AsyncClient` when you need to make requests from asynchronous test code.

Be mindful of whether the code under test is synchronous or asynchronous and whether its dependencies support the chosen execution context.

# Part 11: Database Testing

## 39. Test Database

Django normally creates a separate test database when running database-backed tests.

The test runner prepares the database schema and required test data, executes the tests, and cleans up afterward.

Do not assume your development database is the database being modified by ordinary Django test runs.

## 40. Testing Database Records

Example:

```python
from django.test import TestCase
from students.models import Student


class StudentDatabaseTestCase(TestCase):

    def test_create_student(self):
        student = Student.objects.create(
            name="Omar",
            age=22,
        )

        self.assertTrue(
            Student.objects.filter(pk=student.pk).exists()
        )
```

This test verifies that the record exists in the test database.

## 41. Testing Updates

```python
def test_update_student(self):
    student = Student.objects.create(
        name="Omar",
        age=22,
    )

    student.age = 23
    student.save()

    student.refresh_from_db()

    self.assertEqual(student.age, 23)
```

`refresh_from_db()` reloads the object's field values from the database.

## 42. Testing Deletions

```python
def test_delete_student(self):
    student = Student.objects.create(
        name="Omar",
        age=22,
    )

    student.delete()

    self.assertFalse(
        Student.objects.filter(pk=student.pk).exists()
    )
```

This verifies that the database record has been deleted.

## 43. Testing Multiple Databases

Django supports applications that use more than one database.

Advanced tests may declare the databases they are permitted to access using the test case's `databases` attribute.

Example:

```python
from django.test import TestCase


class MultiDatabaseTestCase(TestCase):
    databases = {"default", "other"}

    def test_database_access(self):
        ...
```

This example assumes both database aliases are configured in `DATABASES`.

Multi-database tests should be designed carefully because routers, transactions, and test database setup can differ between database configurations.

# Part 12: Test Runner and Useful Commands

## 44. Running Tests

Run all discovered tests:

```bash
python manage.py test
```

Run tests for one application:

```bash
python manage.py test students
```

Run one test module:

```bash
python manage.py test students.tests.test_models
```

Run one test class:

```bash
python manage.py test students.tests.test_models.StudentModelTestCase
```

Run one method:

```bash
python manage.py test students.tests.test_models.StudentModelTestCase.test_student_creation
```

The exact test label depends on your test file structure.

## 45. Useful Test Runner Options

### Verbose Output

```bash
python manage.py test --verbosity 2
```

Higher verbosity displays more detail about test discovery and execution.

### Keep the Test Database

```bash
python manage.py test --keepdb
```

This asks Django to preserve the test database between runs when possible, reducing setup time.

### Stop After the First Failure

```bash
python manage.py test --failfast
```

### Run Tests in Parallel

```bash
python manage.py test --parallel
```

Parallel execution can improve performance, but tests must be designed to work safely under parallel execution. Some projects or database configurations may need additional setup.

### Reverse Test Order

```bash
python manage.py test --reverse
```

This can help reveal tests that incorrectly depend on execution order.

### Display SQL Queries

```bash
python manage.py test --debug-sql
```

This is useful for diagnosing unexpected database queries and related failures.

# Part 13: Best Practices

## 46. Django Testing Best Practices

1. Write tests for important business logic.
2. Give test methods descriptive names.
3. Test successful and unsuccessful cases.
4. Use `SimpleTestCase` when database access is unnecessary.
5. Use `TestCase` for most database-backed tests.
6. Use `TransactionTestCase` only when transaction behavior needs to be tested.
7. Use `setUpTestData()` for shared database setup.
8. Keep each test focused on a clear behavior.
9. Test permissions as well as authentication.
10. Validate API response status codes and response data.
11. Avoid depending on external APIs during ordinary unit tests.
12. Use mocks for external services when appropriate.
13. Keep test data predictable and independent.
14. Do not rely on test execution order.
15. Test invalid inputs and edge cases.
16. Keep secrets and real credentials out of test files.
17. Run tests before committing important changes.
18. Run tests against the same database backend used in production when practical.
19. Include tests in continuous integration.
20. Remember that passing tests do not guarantee the absence of every bug.

## 47. Common Testing Mistakes

### Mistake 1: Forgetting the `test_` Prefix

Incorrect:

```python
def student_creation(self):
    ...
```

Correct:

```python
def test_student_creation(self):
    ...
```

### Mistake 2: Using SimpleTestCase for Database Queries

Incorrect:

```python
from django.test import SimpleTestCase
from students.models import Student


class StudentTest(SimpleTestCase):

    def test_students(self):
        Student.objects.count()
```

Use `TestCase` instead when the test needs database access.

### Mistake 3: Testing Only Successful Inputs

A robust suite should also test invalid data, missing fields, unauthorized requests, and other relevant failure cases.

### Mistake 4: Making Real External API Calls

Ordinary unit tests should generally avoid real network dependencies because external services can be slow, unavailable, or costly.

Use mocks or controlled test services where appropriate.

### Mistake 5: Depending on Test Order

Each test should establish its own required state rather than depending on another test having run first.

# Part 14: Django Testing Interview Questions and Answers

## Q1. What is testing in Django?

Testing is the process of verifying that Django application components behave as expected.

## Q2. Which testing framework does Django use by default?

Django's built-in test framework is based on Python's `unittest` framework.

## Q3. What is TestCase?

`TestCase` is a Django test class designed for database-backed tests. It provides database isolation and a test client.

## Q4. What is SimpleTestCase?

`SimpleTestCase` is suitable for tests that do not require database access. Database queries are disallowed by default.

## Q5. What is TransactionTestCase?

`TransactionTestCase` is used when tests need to observe actual transaction and commit behavior that cannot be tested normally inside `TestCase`.

## Q6. What is the Django test client?

The test client simulates HTTP requests to a Django application without requiring a running web server.

## Q7. What is RequestFactory?

`RequestFactory` creates request objects for directly invoking and testing views. It does not run middleware or URL routing.

## Q8. What is the difference between Client and RequestFactory?

`Client` exercises Django's request-handling process, including URL routing and middleware. `RequestFactory` creates a request for direct view testing.

## Q9. How do you run Django tests?

```bash
python manage.py test
```

## Q10. How do you run tests for a specific app?

```bash
python manage.py test students
```

## Q11. What is an assertion?

An assertion checks whether an actual value or behavior matches the expected result.

## Q12. What is setUp()?

`setUp()` runs before each test method and is commonly used to initialize test-specific data.

## Q13. What is setUpTestData()?

`setUpTestData()` creates shared class-level test data once for a Django database-aware test class.

## Q14. What is mocking?

Mocking replaces a dependency with a controlled test object, allowing code to be tested without relying on the real dependency.

## Q15. What is override_settings?

`override_settings` temporarily changes Django settings for a test or test class.

## Q16. How do you test a JSON response?

Use the test client and inspect `response.json()`:

```python
response = self.client.get("/api/students/")

self.assertEqual(response.status_code, 200)
self.assertEqual(response.json()["name"], "Omar")
```

This assumes the endpoint returns the specified JSON structure.

## Q17. How do you test authentication?

Use `self.client.login()` to test login credentials or `self.client.force_login(user)` to establish an authenticated session without testing the login flow.

## Q18. How do you test Django REST Framework APIs?

Use tools such as `APITestCase` and `APIClient` from `rest_framework.test`.

## Q19. What is a fixture?

A fixture is serialized data that Django can load into a database for tests or other supported workflows.

## Q20. Why should tests be independent?

Independent tests produce predictable results, are easier to debug, and do not fail merely because the execution order changes.

## Q21. What is regression testing?

Regression testing checks that code changes have not broken existing functionality.

## Q22. How can you test an asynchronous view?

Use Django's asynchronous test client, `AsyncClient`, or `self.async_client` in asynchronous test methods.

## Q23. What does `--keepdb` do?

It asks Django to preserve the test database between runs when possible, which can reduce repeated database setup time.

## Q24. How do you test email sending?

Use Django's test email backend and inspect `django.core.mail.outbox` to verify generated messages.

## Q25. Does a passing test guarantee that the application is bug-free?

No. Tests only verify the behavior covered by their assertions and scenarios.

# Part 15: Quick Revision Cheat Sheet

## Important Imports

```python
from django.test import (
    TestCase,
    SimpleTestCase,
    TransactionTestCase,
    Client,
    RequestFactory,
    override_settings,
)

from django.core import mail
from unittest.mock import patch
```

## Important Commands

```bash
# Run all tests
python manage.py test

# Run one app's tests
python manage.py test students

# Run one test module
python manage.py test students.tests.test_models

# Increase verbosity
python manage.py test --verbosity 2

# Preserve the test database
python manage.py test --keepdb

# Stop after the first failure
python manage.py test --failfast

# Run tests in parallel
python manage.py test --parallel

# Display SQL queries
python manage.py test --debug-sql
```

## Important Concepts

| Concept | Meaning |
|---|---|
| Unit testing | Tests an individual function or component |
| Integration testing | Tests interactions between components |
| Regression testing | Checks that existing behavior still works |
| `TestCase` | Database-backed testing with transaction-based isolation |
| `SimpleTestCase` | Testing without database access by default |
| `TransactionTestCase` | Testing actual transaction behavior |
| `Client` | Simulates HTTP requests |
| `RequestFactory` | Creates request objects for direct view testing |
| `AsyncClient` | Makes asynchronous requests |
| `setUp()` | Runs before each test method |
| `setUpTestData()` | Creates shared test data once per test class |
| Assertions | Verify expected outcomes |
| Mocking | Replaces dependencies with controlled objects |
| Fixtures | Load predefined serialized data |
| `override_settings` | Temporarily changes settings |

# Final Summary

Django testing helps developers verify application behavior and detect regressions before code reaches production.

Remember these key points:

1. Write tests in discoverable `test*.py` files.
2. Use `TestCase` for most tests involving the database.
3. Use `SimpleTestCase` for tests that do not need database access.
4. Use `TransactionTestCase` for transaction-sensitive tests.
5. Use `Client` to test requests and responses.
6. Use `RequestFactory` to test views directly.
7. Test models, forms, APIs, authentication, and permissions.
8. Use mocks to isolate external dependencies.
9. Test valid inputs, invalid inputs, and important edge cases.
10. Run tests with `python manage.py test` before deploying changes.

**In one sentence:** Django testing provides a structured way to verify application behavior, protect existing functionality, and build more reliable web applications.