# Django Migrations + Django File Management — Complete Notes

# Part 1: Django Migrations

## 1. What Are Django Migrations?

**Django Migrations** are Django's mechanism for propagating changes made to models into the database schema.

Whenever you create, modify, or delete a model or field, migrations help apply those changes to the database.

Examples of model changes:

- Creating a new model.
- Adding a new field.
- Removing a field.
- Modifying a field.
- Deleting a model.
- Changing certain model options.

### Example

`models.py`

```python
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
```

Create migration files:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

**Important:**

- `makemigrations` creates migration files.
- `migrate` applies or reverses migrations.
- Migration files record database operations, not the database itself.

---

## 2. How Do Django Migrations Work?

Django migrations generally follow three steps.

### Step 1: Define a Model

```python
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
```

### Step 2: Create a Migration File

```bash
python manage.py makemigrations
```

Example output:

```text
Migrations for 'students':
  students/migrations/0001_initial.py
    + Create model Student
```

### Step 3: Apply the Migration

```bash
python manage.py migrate
```

Django executes the migration operations and creates the corresponding database table.

### Workflow

```text
models.py
    |
    v
makemigrations
    |
    v
Migration File
    |
    v
migrate
    |
    v
Database Schema
```

---

## 3. Four Main Migration Commands

| Command | Purpose |
|---|---|
| `makemigrations` | Creates migration files |
| `migrate` | Applies or reverses migrations |
| `showmigrations` | Displays migration status |
| `sqlmigrate` | Displays SQL for a migration |

### 3.1 makemigrations

Creates migration files from detected model changes.

```bash
python manage.py makemigrations
```

For a specific app:

```bash
python manage.py makemigrations students
```

Example:

Before:

```python
class Student(models.Model):
    name = models.CharField(max_length=100)
```

After adding a field:

```python
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
```

Run:

```bash
python manage.py makemigrations
```

Django generates a migration to add the `age` field.

**Note:** This command does not normally apply the migration to the database.

### 3.2 migrate

Applies migrations:

```bash
python manage.py migrate
```

Apply migrations for a specific app:

```bash
python manage.py migrate students
```

### 3.3 showmigrations

Displays migration status:

```bash
python manage.py showmigrations
```

Example output:

```text
students
 [X] 0001_initial
 [X] 0002_student_age
 [ ] 0003_student_email
```

- `[X]` means the migration is recorded as applied.
- `[ ]` means the migration is not recorded as applied.

### 3.4 sqlmigrate

Displays the SQL Django plans to use for a migration:

```bash
python manage.py sqlmigrate students 0001
```

**Note:** `sqlmigrate` displays SQL; it does not apply the migration.

The generated SQL depends on the database backend.

---

## 4. Migrations as Database Version Control

Migrations act like version control for database schemas.

Git tracks source code changes, while Django migration files record database schema changes.

Example:

```text
0001_initial.py
       |
       v
0002_student_age.py
       |
       v
0003_student_email.py
```

Each migration represents a set of database operations.

Migration files should normally be committed to Git along with the corresponding model changes. This allows other developers and deployment environments to reproduce the same migration history.

---

## 5. Where Are Migration Files Stored?

Migration files are usually stored in a `migrations` directory inside each Django app.

```text
myproject/
├── manage.py
├── myproject/
│   ├── settings.py
│   └── urls.py
└── students/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    └── migrations/
        ├── __init__.py
        ├── 0001_initial.py
        └── 0002_student_age.py
```

- `models.py` defines models.
- `migrations/` stores migration files.
- `0001_initial.py` commonly represents the initial migration.
- Later files represent subsequent changes.

---

## 6. Standard Migration Workflow

### Step 1: Create a Model

```python
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
```

### Step 2: Create and Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Add a Field

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    description = models.TextField()
```

### Step 4: Create and Apply the New Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

Django generates a migration to add the `description` column.

**Important:** Adding a non-nullable field to a table containing existing records may require a default value or a staged schema-and-data migration.

---

## 7. Migration Dependencies

A migration may depend on another migration that must be applied first.

Example:

```python
# authors/models.py

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
```

```python
# books/models.py

from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        "authors.Author",
        on_delete=models.CASCADE,
    )
```

The `Book` model references the `Author` model.

A migration in the `books` app may contain:

```python
dependencies = [
    ("authors", "0001_initial"),
]
```

This means the specified migration in the `authors` app must be applied before this migration.

Django uses migration dependencies to determine a valid execution order.

---

## 8. Reversing Migrations

Migrations can be reversed when their operations support reversal.

Suppose the migration history is:

```text
0001_initial
0002_student_age
0003_student_email
```

To return the app to migration `0002`:

```bash
python manage.py migrate students 0002
```

To unapply all migrations for an app:

```bash
python manage.py migrate students zero
```

**Warning:** Reversing migrations may remove tables, columns, or data. Some operations cannot be reversed. Review the consequences and back up important databases before reversing production migrations.

---

## 9. Initial Migrations

An initial migration establishes the initial database schema for an app.

It is commonly named:

```text
0001_initial.py
```

Example:

```python
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100),
                ),
            ],
        ),
    ]
```

Important attributes:

- `initial`: Marks an initial migration.
- `dependencies`: Lists prerequisite migrations.
- `operations`: Contains database operations.
- `CreateModel`: Creates a model's database table.

Django normally generates initial migration files automatically.

---

## 10. Data Migrations

A **Data Migration** transforms existing database records rather than only changing the database schema.

Examples:

- Populating a newly added field.
- Updating existing records.
- Combining values from multiple fields.
- Moving data between models.

Suppose a `Student` model has these fields:

```python
first_name = models.CharField(max_length=100)
last_name = models.CharField(max_length=100)
```

You add:

```python
full_name = models.CharField(
    max_length=201,
    blank=True,
)
```

### Step 1: Create and Apply the Schema Migration

```bash
python manage.py makemigrations students
python manage.py migrate students
```

Assume this creates and applies `0002_student_full_name`.

### Step 2: Create an Empty Migration

```bash
python manage.py makemigrations --empty students
```

Assume the generated migration is `0003_populate_full_name.py`.

### Step 3: Write the Data Migration

```python
from django.db import migrations


def populate_full_name(apps, schema_editor):
    Student = apps.get_model("students", "Student")
    database = schema_editor.connection.alias

    students = Student.objects.using(database).all()

    for student in students.iterator():
        student.full_name = (
            f"{student.first_name} {student.last_name}"
        ).strip()

        student.save(
            using=database,
            update_fields=["full_name"],
        )


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0002_student_full_name"),
    ]

    operations = [
        migrations.RunPython(populate_full_name),
    ]
```

Important concepts:

- `apps.get_model()` retrieves the historical model.
- `migrations.RunPython()` executes Python code during migration.
- `schema_editor.connection.alias` identifies the database being migrated.
- `iterator()` can help process large querysets without caching all objects in memory.

For large tables, consider batching updates or using database-level expressions when appropriate.

### Reversible Data Migrations

A data migration can specify a reverse function:

```python
def reverse_populate_full_name(apps, schema_editor):
    Student = apps.get_model("students", "Student")
    database = schema_editor.connection.alias

    Student.objects.using(database).update(full_name="")
```

Then:

```python
migrations.RunPython(
    populate_full_name,
    reverse_populate_full_name,
)
```

Only use a reverse function if it correctly handles the data and preserves information that should not be lost.

---

## 11. Historical Models

Django migrations operate on historical versions of models.

Use:

```python
Student = apps.get_model("students", "Student")
```

Avoid importing the current model directly inside a migration:

```python
from students.models import Student
```

Direct imports can cause old migrations to break when the current model changes.

Historical models include the fields and relevant model options for that point in migration history. They do not necessarily include custom methods defined on the current model.

---

## 12. Transactions in Migrations

A transaction groups database operations so they can be committed or rolled back together when supported.

Django normally runs migration operations inside a transaction when the database backend supports transactional DDL.

PostgreSQL and SQLite support transactional schema changes. MySQL and Oracle have different transactional guarantees for schema operations.

A migration can disable its default transaction behavior:

```python
from django.db import migrations


class Migration(migrations.Migration):

    atomic = False

    dependencies = []

    operations = []
```

`atomic = False` is useful for certain advanced scenarios, such as processing large data sets in independently committed batches.

Use it only when you understand the transaction and recovery implications.

---

## 13. Database Backend Considerations

| Database | Important consideration |
|---|---|
| PostgreSQL | Supports transactional schema operations for many changes |
| MySQL | Some schema changes cannot be rolled back transactionally |
| SQLite | Some changes require creating and copying into a replacement table |
| Oracle | Supports migrations, but transaction behavior differs from PostgreSQL and SQLite |

For some SQLite schema changes, Django may need to:

```text
Create a New Table
        |
        v
Copy Existing Data
        |
        v
Drop the Old Table
        |
        v
Rename the New Table
```

This process can be slower for large tables.

Test migrations with the same database backend used in production whenever possible.

---

## 14. Migration Conflicts

Migration conflicts can occur when multiple developers create migrations from the same previous migration state on different branches.

Example:

```text
0001_initial.py
      |
      |----------------|
      v                v
0002_student_age  0002_student_email
```

Django can detect many conflicting migration branches.

When appropriate, create a merge migration:

```bash
python manage.py makemigrations --merge
```

Review the generated migration and its dependencies before applying it.

A merge migration resolves the migration graph structure; it does not automatically resolve logical conflicts between operations.

---

## 15. Migration Squashing

Migration squashing combines multiple migration files into one or a smaller number of files.

Example:

```text
0001_initial.py
0002_add_age.py
0003_add_email.py
0004_add_address.py
```

Command:

```bash
python manage.py squashmigrations students 0004
```

Django attempts to optimize the operations and creates a squashed migration.

Squashing can simplify migration history in long-running projects.

**Important:** Follow Django's recommended transition process. Keep the replaced migration files until all relevant environments have safely moved to the squashed migration history.

---

## 16. The --fake-initial Option

The `--fake-initial` option helps when introducing migrations to an app whose database tables already exist.

First, create an initial migration:

```bash
python manage.py makemigrations students
```

Then run:

```bash
python manage.py migrate --fake-initial
```

Django checks whether the tables or columns associated with certain initial migration operations already exist. If the checks pass, Django can mark the initial migration as applied without recreating those objects.

**Important:** This option does not fully verify that the existing database schema matches the models. Review the existing schema before using it.

---

## 17. Migration Best Practices

1. Create migrations after changing models.
2. Test migrations in development.
3. Commit migration files to version control.
4. Commit model changes and their migrations together.
5. Use historical models in data migrations.
6. Review migration dependencies across apps.
7. Back up important databases before risky changes.
8. Test production migrations in staging when possible.
9. Avoid editing migration files unnecessarily after they have been shared or applied.
10. Review destructive and irreversible operations carefully.
11. Consider table size and database locking during production deployments.
12. Check the generated SQL for important schema changes.

Standard workflow:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

---

## 18. Migration Commands Cheat Sheet

| Task | Command |
|---|---|
| Create migrations | `python manage.py makemigrations` |
| Create migrations for one app | `python manage.py makemigrations students` |
| Apply migrations | `python manage.py migrate` |
| Apply migrations for one app | `python manage.py migrate students` |
| List migration status | `python manage.py showmigrations` |
| Display migration SQL | `python manage.py sqlmigrate students 0001` |
| Create an empty migration | `python manage.py makemigrations --empty students` |
| Create a merge migration | `python manage.py makemigrations --merge` |
| Squash migrations | `python manage.py squashmigrations students 0004` |
| Reverse to a specific migration | `python manage.py migrate students 0002` |
| Unapply all app migrations | `python manage.py migrate students zero` |
| Handle certain existing initial tables | `python manage.py migrate --fake-initial` |

Replace `students` and migration numbers with the values used in your project.

---

## 19. Migration Interview Questions and Answers

### Q1. What are Django migrations?

Migrations record and apply changes to database schemas based on changes to Django models.

### Q2. What is the difference between makemigrations and migrate?

- `makemigrations` creates migration files.
- `migrate` applies or reverses migration operations.

### Q3. What is showmigrations?

It lists migrations and indicates which migrations are recorded as applied.

### Q4. What is sqlmigrate?

It displays the SQL Django plans to use for a specified migration.

### Q5. What is a data migration?

A data migration transforms existing database records using operations such as `RunPython`.

### Q6. What is a migration dependency?

It specifies another migration that must be applied first.

### Q7. What is an initial migration?

It establishes the initial database schema for an app.

### Q8. Can migrations be reversed?

Yes, when their operations support reversal.

```bash
python manage.py migrate students 0002
```

### Q9. What is migration squashing?

It combines multiple migrations into fewer migration files while preserving their intended effects.

### Q10. Why should migration files be committed to Git?

They allow developers and deployment environments to reproduce schema changes consistently.

### Q11. Why use historical models in data migrations?

They ensure migration code uses the model definition appropriate to that point in migration history.

### Q12. What is RunPython?

`RunPython` executes Python code during a migration, commonly for data transformations.

---

## 20. Migration Key Takeaways

1. Models define the database structure.
2. `makemigrations` creates migration files.
3. `migrate` applies or reverses migrations.
4. `showmigrations` displays migration status.
5. `sqlmigrate` displays migration SQL.
6. `RunPython` supports data migrations.
7. Historical models help keep old migrations reliable.
8. Migration files should normally be version-controlled.

### Final Workflow

```text
Modify models.py
       |
       v
makemigrations
       |
       v
Migration File
       |
       v
migrate
       |
       v
Updated Database Schema
```

**In one sentence:** Django migrations provide a version-controlled way to manage database schema changes and transform existing database data.

---

# Part 2: Django File Management

## 21. What Is File Management in Django?

Django File Management provides APIs for handling files uploaded by users, such as images, PDFs, documents, and other files.

Django allows you to:

- Upload files through forms and APIs.
- Store files locally or in remote storage.
- Access file names, paths, URLs, and sizes.
- Open, read, write, and delete files.
- Configure custom storage backends.

**Media files** and **static files** are different:

- **Media files:** User-uploaded images, documents, videos, and other files.
- **Static files:** CSS, JavaScript, application images, and other assets used by the application.

---

## 22. Configuring Media Files

Configure `MEDIA_ROOT` and `MEDIA_URL` in `settings.py`.

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

### Explanation

- `MEDIA_ROOT`: Filesystem location where uploaded files are stored.
- `MEDIA_URL`: URL prefix used to generate media URLs.

Example project structure:

```text
project/
├── manage.py
├── media/
│   └── cars/
│       └── chevy.jpg
└── myproject/
    └── settings.py
```

The file might have this URL:

```text
/media/cars/chevy.jpg
```

The URL does not guarantee that the file is publicly accessible. Access depends on how the application and media server are configured.

### Serving Media During Development

In the project's `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    # Application URL patterns
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
```

This helper is intended for development, not production deployment.

In production, configure an appropriate web server or storage backend to serve media files.

---

## 23. Using Files in Django Models

Django provides two important model fields for file handling.

### 23.1 FileField

`FileField` handles general file uploads.

```python
from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="documents/")
```

Here:

- `title` stores the document title.
- `file` stores a reference to the uploaded file.
- `upload_to="documents/"` specifies a path relative to the storage location.

Example storage structure:

```text
media/
└── documents/
    ├── report.pdf
    └── notes.txt
```

The database stores the file name or relative storage name, not normally the complete file contents.

### 23.2 ImageField

`ImageField` is designed for image uploads.

```python
from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    photo = models.ImageField(upload_to="cars/")
```

`ImageField` requires Pillow.

Install it using:

```bash
pip install Pillow
```

The image is stored using the configured storage backend, while the database stores its file reference.

---

## 24. Accessing Files Through Model Instances

Consider this model:

```python
class Car(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="cars/")
    specs = models.FileField(upload_to="specs/")
```

Retrieve an object:

```python
car = Car.objects.get(name="57 Chevy")
```

### File Name

```python
car.photo.name
```

Example:

```text
cars/chevy.jpg
```

This is the stored name relative to the storage system.

### File Path

```python
car.photo.path
```

Example:

```text
/home/user/project/media/cars/chevy.jpg
```

**Important:** `.path` is not supported by every storage backend. Remote storage systems may not expose a local filesystem path.

### File URL

```python
car.photo.url
```

Example:

```text
/media/cars/chevy.jpg
```

The generated URL depends on the storage backend and its configuration.

**Important:** A URL does not necessarily mean that the file is publicly accessible.

---

## 25. Changing a File Name

Changing the file name stored in a model field does not automatically rename the physical file.

For example:

```python
car = Car.objects.get(name="57 Chevy")

car.photo.name = "cars/chevy_ii.jpg"
car.save(update_fields=["photo"])
```

This changes the name stored in the database field. It does not, by itself, move or rename the existing file in storage.

If you need to rename a file physically, use the storage API or suitable filesystem operations and update the model reference carefully.

### Important Distinction

- `car.photo.name`: Stored file name.
- `car.photo.path`: Local filesystem path, if supported.
- `car.photo.url`: URL generated by the storage backend.

These values serve different purposes.

---

## 26. Saving an Existing File to a FileField

You can attach an existing file to a model's `FileField`.

```python
from pathlib import Path
from django.core.files import File

path = Path("/some/external/specs.pdf")

car = Car.objects.get(name="57 Chevy")

with path.open("rb") as f:
    car.specs.save(
        path.name,
        File(f),
        save=True,
    )
```

### Explanation

- `Path` represents a filesystem path.
- `open("rb")` opens the file in binary read mode.
- `File(f)` wraps the Python file object in Django's file API.
- `car.specs.save()` saves the file through the configured storage backend.
- `save=True` saves the model instance after assigning the file.

Django may generate a different stored name if a file with the requested name already exists.

---

## 27. The Django File Object

Django provides `django.core.files.File` to wrap file-like objects.

```python
from django.core.files import File

with open("hello.txt", "rb") as f:
    myfile = File(f)
    content = myfile.read()

    print(content)
```

### Common Attributes

| Attribute | Description |
|---|---|
| `name` | Name of the file |
| `size` | File size in bytes |
| `closed` | Whether the file is closed |
| `file` | Underlying file object |

### Common Methods

| Method | Description |
|---|---|
| `open()` | Opens or reopens the file |
| `read()` | Reads file contents |
| `write()` | Writes content |
| `close()` | Closes the file |
| `chunks()` | Reads the file in chunks |

Using a context manager helps ensure that the underlying file is closed after processing.

---

## 28. Working with ImageField

`ImageField` provides image-related information.

```python
car = Car.objects.get(name="57 Chevy")

print(car.photo.width)
print(car.photo.height)
print(car.photo.size)
```

The results depend on the uploaded image.

- `width`: Image width in pixels.
- `height`: Image height in pixels.
- `size`: File size in bytes.

### Opening an Image with Pillow

```python
from PIL import Image

car = Car.objects.get(name="57 Chevy")

with car.photo.open("rb") as f:
    image = Image.open(f)
    image.load()

    print(image.size)
```

Example output:

```text
(191, 287)
```

The output represents `(width, height)`.

Calling `image.load()` inside the context manager ensures that image data is loaded before the file is closed.

---

## 29. Closing Files Properly

Closing files releases system resources.

Example:

```python
with open("hello.txt", "rb") as f:
    content = f.read()
```

Python automatically closes the file when the `with` block finishes.

When processing many uploaded files, close files appropriately to avoid exhausting available file descriptors.

---

## 30. File Storage in Django

Django delegates file operations to a storage backend.

A storage backend determines how files are saved, opened, deleted, and accessed.

Django's built-in local filesystem backend is:

```python
django.core.files.storage.FileSystemStorage
```

In Django 6.0, the `STORAGES` setting configures storage backends.

Example:

```python
STORAGES = {
    "default": {
        "BACKEND": (
            "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    },
}
```

- `default`: Storage for uploaded files.
- `staticfiles`: Storage for static files.

You can customize storage options using an `OPTIONS` dictionary.

Django also supports custom storage backends for remote and cloud storage services.

---

## 31. Using the Default Storage System

You can work with files without attaching them to model instances.

```python
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
```

### Save a File

```python
path = default_storage.save(
    "documents/hello.txt",
    ContentFile(b"Hello World"),
)

print(path)
```

The returned name may differ from the requested name if a naming conflict occurs.

### Check File Size

```python
size = default_storage.size(path)
print(size)
```

For a file containing `Hello World`, the size is 11 bytes.

### Read File Contents

```python
with default_storage.open(path, "rb") as f:
    content = f.read()

print(content)
```

Output:

```text
b'Hello World'
```

### Check Whether a File Exists

```python
exists = default_storage.exists(path)
print(exists)
```

Output:

```text
True
```

### Delete a File

```python
default_storage.delete(path)
```

This deletes the stored file. Use this operation carefully, especially with files that must be retained.

---

## 32. FileSystemStorage

`FileSystemStorage` stores files on the local filesystem.

Example:

```python
from django.core.files.storage import FileSystemStorage
from django.db import models

photo_storage = FileSystemStorage(
    location="/var/app/media/photos",
)


class Car(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(
        upload_to="cars/",
        storage=photo_storage,
    )
```

Here, the storage location is the base directory, while `upload_to` adds a relative path.

Example:

```text
/var/app/media/photos/cars/chevy.jpg
```

Configure the location appropriately for the operating system and deployment environment.

---

## 33. Custom Storage Systems

Django allows custom storage backends for:

- Cloud object storage.
- Remote file servers.
- Specialized filesystem locations.
- Testing environments.

A storage instance can be passed to a `FileField` or `ImageField`.

```python
class Document(models.Model):
    file = models.FileField(
        upload_to="documents/",
        storage=my_custom_storage,
    )
```

`my_custom_storage` must be a valid storage instance.

A custom storage backend should implement the required storage API or inherit from an appropriate Django storage class.

---

## 34. Using a Callable for Storage

A callable can be supplied as the `storage` argument to select a storage backend.

```python
from django.conf import settings
from django.db import models

from .storages import MyLocalStorage, MyRemoteStorage


def select_storage():
    if settings.DEBUG:
        return MyLocalStorage()

    return MyRemoteStorage()


class MyModel(models.Model):
    upload = models.FileField(
        upload_to="uploads/",
        storage=select_storage,
    )
```

Both storage classes must be implemented correctly.

**Important:** Storage selection is associated with model initialization and field configuration. Do not assume that changing `settings.DEBUG` later automatically replaces the storage object. Test storage configuration carefully when overriding settings.

---

## 35. Accessing Configured Storage Backends

Django provides the `storages` registry for accessing configured storage backends.

```python
from django.core.files.storage import storages

storage = storages["default"]
```

The selected backend comes from the `STORAGES` setting.

For a model field that needs callable storage selection:

```python
def select_storage():
    return storages["default"]
```

A callable is useful when storage selection needs to be resolved at an appropriate time rather than creating a storage instance directly in the model definition.

---

## 36. File Uploads Through Forms

Django forms can handle uploaded files using `FileField` and `ImageField`.

Example form:

```python
from django import forms


class DocumentForm(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()
```

The HTML form must use `multipart/form-data`:

```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
</form>
```

The `multipart/form-data` encoding is required for browser-based file uploads.

### Handling Uploads in a View

```python
from django.shortcuts import render, redirect

from .forms import DocumentForm
from .models import Document


def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            Document.objects.create(
                title=form.cleaned_data["title"],
                file=form.cleaned_data["file"],
            )

            return redirect("upload_document")

    else:
        form = DocumentForm()

    return render(
        request,
        "upload.html",
        {"form": form},
    )
```

This example assumes that the `Document` model contains `title` and `file` fields and that `upload_document` is configured as a URL name.

**Important:** Validate uploaded content, file sizes, and access permissions. Do not trust a filename or extension as proof that a file is safe.

---

## 37. FileField vs ImageField

| Feature | FileField | ImageField |
|---|---|---|
| Purpose | General file uploads | Image uploads |
| PDF support | Yes | No, not as an image |
| Image dimensions | Not provided by the field | Provides width and height |
| Pillow required | No | Yes |
| `upload_to` support | Yes | Yes |
| Storage backend support | Yes | Yes |

Use `FileField` for PDFs, documents, and other general files.

Use `ImageField` when the field is intended to contain images.

---

## 38. File Management Best Practices

1. Configure `MEDIA_ROOT` and `MEDIA_URL` correctly.
2. Use `FileField` for general files and `ImageField` for images.
3. Install Pillow when using `ImageField`.
4. Use storage APIs instead of assuming all files are local.
5. Do not assume `.path` works with remote storage.
6. Close files properly.
7. Validate file sizes, file types, and uploaded content.
8. Avoid trusting filenames supplied by users.
9. Restrict access to private documents.
10. Use appropriate cloud or object storage when needed.
11. Remember that deleting a database record does not automatically guarantee that its associated file is deleted.
12. Configure backups and retention policies for important uploaded files.
13. Avoid serving untrusted uploads as executable content.
14. Do not rely on the development media-serving helper in production.

---

## 39. Important File Management Concepts

| Concept | Meaning |
|---|---|
| `MEDIA_ROOT` | Filesystem location for uploaded files |
| `MEDIA_URL` | URL prefix for media files |
| `FileField` | Model field for general files |
| `ImageField` | Model field for images |
| `upload_to` | Specifies the upload directory or path callable |
| `File` | Django wrapper for file objects |
| `FileSystemStorage` | Local filesystem storage backend |
| `default_storage` | Default configured storage instance |
| `storages` | Registry of configured storage backends |
| `name` | Stored file name |
| `path` | Local filesystem path, when supported |
| `url` | URL provided by the storage backend |
| `size` | File size in bytes |

---

## 40. File Management Interview Questions and Answers

### Q1. What is Django file management?

It provides APIs for uploading, storing, accessing, and managing files.

### Q2. What is the difference between MEDIA_ROOT and MEDIA_URL?

`MEDIA_ROOT` specifies where files are stored on the filesystem, while `MEDIA_URL` defines the URL prefix used to access media files.

### Q3. What is the difference between FileField and ImageField?

`FileField` handles general files, while `ImageField` is designed for images and provides image-specific information.

### Q4. What is upload_to?

It specifies the directory or path-generation callable used to determine where uploaded files are stored.

### Q5. What is FileSystemStorage?

It is Django's built-in storage backend for saving files to a local filesystem.

### Q6. What is default_storage?

It provides access to Django's configured default file storage backend.

### Q7. What is the purpose of the File object?

It wraps a file-like object and provides Django's file-handling API.

### Q8. Does changing a FileField name rename the physical file?

No. Changing the stored name does not automatically rename or move the existing physical file.

### Q9. Can Django use cloud storage?

Yes. Custom storage backends can integrate remote and cloud storage services.

### Q10. Why is closing files important?

Closing files releases system resources and helps prevent file descriptor exhaustion.

### Q11. Why is Pillow required for ImageField?

Pillow provides image-processing functionality used by Django to validate images and obtain image information.

### Q12. Does deleting a model instance always delete its associated file?

No. Deleting a model instance does not automatically guarantee that its associated physical file is removed.

---

## 41. Final File Management Takeaways

1. `MEDIA_ROOT` and `MEDIA_URL` configure uploaded media.
2. `FileField` handles general file uploads.
3. `ImageField` handles image uploads.
4. `File` provides an API for working with file objects.
5. `FileSystemStorage` stores files locally.
6. `default_storage` accesses the default storage backend.
7. `storages` provides access to configured storage backends.
8. Custom storage backends allow remote or specialized file storage.
9. File validation and access control are essential for secure uploads.

**In one sentence:** Django file management provides a flexible API for handling uploaded files independently of the underlying storage system.

---

# Final Quick Revision

## Django Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py sqlmigrate students 0001
```

- `makemigrations`: Creates migration files.
- `migrate`: Applies or reverses migrations.
- `showmigrations`: Displays migration status.
- `sqlmigrate`: Displays migration SQL.
- `RunPython`: Performs data migrations.
- `apps.get_model()`: Retrieves historical models.

## Django File Management

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

- `FileField`: General file uploads.
- `ImageField`: Image uploads.
- `File`: Wraps file-like objects.
- `FileSystemStorage`: Stores files locally.
- `default_storage`: Accesses the default storage backend.
- `storages`: Accesses configured storage backends.
- `request.FILES`: Contains uploaded files in a Django request.

**Final Summary:** Django migrations manage database schema and data changes, while Django file management handles uploaded files through model fields, file APIs, and configurable storage backends.