# Django Migrations — Complete Notes

## 1. What Are Django Migrations?

**Django Migrations** are Django's mechanism for propagating changes made to models into the database schema.

Whenever you add, modify, or delete a model or field, migrations help apply those changes to the database.

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

Create a migration file:

```bash
python manage.py makemigrations
```

Apply the migration:

```bash
python manage.py migrate
```

**Important:**
- `makemigrations` creates migration files.
- `migrate` applies migrations to the database.

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

Django generates a migration file containing instructions for database changes.

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

## 3. The Four Main Migration Commands

Django provides four important commands for working with migrations.

| Command | Purpose |
|---|---|
| `makemigrations` | Creates migration files |
| `migrate` | Applies or reverses migrations |
| `showmigrations` | Lists migrations and their status |
| `sqlmigrate` | Displays SQL statements for a migration |

### 3.1 makemigrations

The `makemigrations` command detects changes in models and generates migration files.

```bash
python manage.py makemigrations
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

Example output:

```text
Migrations for 'students':
  students/migrations/0002_student_age.py
    + Add field age to student
```

**Note:** This command creates migration files but does not normally apply them to the database.

### 3.2 migrate

The `migrate` command applies migration operations to the database.

```bash
python manage.py migrate
```

Example output:

```text
Operations to perform:
  Apply all migrations: students

Running migrations:
  Applying students.0002_student_age... OK
```

The `OK` message indicates that the migration was applied successfully.

### 3.3 showmigrations

The `showmigrations` command displays migration files and their application status.

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

- `[X]` means the migration has been applied.
- `[ ]` means the migration has not been applied.

### 3.4 sqlmigrate

The `sqlmigrate` command displays the SQL statements Django plans to use for a specific migration.

```bash
python manage.py sqlmigrate students 0001
```

Example SQL for SQLite:

```sql
CREATE TABLE "students_student" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(100) NOT NULL,
    "age" integer NOT NULL
);
```

**Note:** `sqlmigrate` displays SQL; it does not apply the migration.

---

## 4. Migrations as Database Version Control

Migrations can be thought of as a version control system for database schemas.

Git tracks changes to source code, while Django migrations record instructions for evolving the database schema.

Example migration history:

```text
0001_initial.py
        |
        v
0002_student_age.py
        |
        v
0003_student_email.py
```

Each migration represents a set of changes to the database schema.

Migration files should normally be committed to Git along with the corresponding model changes.

This allows other developers and deployment environments to apply the same migration history.

---

## 5. Where Are Migration Files Stored?

Migration files are usually stored in a `migrations` directory inside each Django app.

Example project structure:

```text
myproject/
│
├── manage.py
│
├── myproject/
│   ├── settings.py
│   └── urls.py
│
└── students/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    │
    └── migrations/
        ├── __init__.py
        ├── 0001_initial.py
        └── 0002_student_age.py
```

- `models.py` defines the models.
- `migrations/` stores migration files.
- `0001_initial.py` is usually the first migration.
- `0002_student_age.py` represents a subsequent change.

---

## 6. The Standard Migration Workflow

Whenever you change a model, follow this workflow.

### Step 1: Create or Modify a Model

```python
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
```

### Step 2: Create Migrations

```bash
python manage.py makemigrations
```

### Step 3: Apply Migrations

```bash
python manage.py migrate
```

### Step 4: Add a New Field

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField()
```

### Step 5: Create and Apply the New Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

Django will generate a migration to add the `description` column to the database table.

---

## 7. Migration Dependencies

A migration may depend on another migration that must be applied first.

This is called a **Migration Dependency**.

Consider two apps:

```text
authors/
books/
```

The `authors` app defines an Author model:

```python
class Author(models.Model):
    name = models.CharField(max_length=100)
```

The `books` app defines a Book model:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)

    author = models.ForeignKey(
        "authors.Author",
        on_delete=models.CASCADE
    )
```

The `Book` model references the `Author` model through a foreign key.

Therefore, the referenced table must exist before the foreign key constraint can be created.

Example dependency:

```python
dependencies = [
    ("authors", "0001_initial"),
]
```

This tells Django that the migration depends on the specified migration in the `authors` app.

Django uses migration dependencies to determine a valid execution order.

---

## 8. Reversing Migrations

Django allows you to reverse migrations when their operations are reversible.

Suppose the migration history is:

```text
0001_initial
0002_student_age
0003_student_email
```

To return the `students` app to migration `0002`, run:

```bash
python manage.py migrate students 0002
```

Django attempts to reverse migrations applied after `0002`.

### Reverse All Migrations for an App

```bash
python manage.py migrate students zero
```

This attempts to unapply all migrations for the `students` app.

**Warning:** Reversing migrations may remove tables, columns, or data. Some migrations are irreversible. Always review the consequences and back up important databases before reversing production migrations.

---

## 9. Initial Migrations

An **Initial Migration** creates the initial database schema for an app.

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
                        serialize=False
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

- `initial`: Identifies the migration as an initial migration.
- `dependencies`: Lists prerequisite migrations.
- `operations`: Contains database change instructions.
- `CreateModel`: Creates a model and its corresponding table.

Django normally generates initial migration files automatically.

---

## 10. Data Migrations

A **Data Migration** changes existing database data rather than only changing the database schema.

Examples:
- Populating a newly added field.
- Combining values from two fields.
- Updating existing records.
- Moving data between models.

### Example

Suppose a Student model has these fields:

```python
first_name = models.CharField(max_length=100)
last_name = models.CharField(max_length=100)
```

You add a new field:

```python
full_name = models.CharField(max_length=201)
```

You want to populate `full_name` using the existing first and last names.

For example:

```text
first_name = "Faruk"
last_name  = "Ahmed"
full_name  = "Faruk Ahmed"
```

### Step 1: Create an Empty Migration

```bash
python manage.py makemigrations --empty students
```

### Step 2: Write the Data Migration

```python
from django.db import migrations


def populate_full_name(apps, schema_editor):
    Student = apps.get_model("students", "Student")

    for student in Student.objects.all():
        student.full_name = (
            f"{student.first_name} {student.last_name}"
        ).strip()

        student.save(update_fields=["full_name"])


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0002_student_full_name"),
    ]

    operations = [
        migrations.RunPython(populate_full_name),
    ]
```

This example assumes that `0002_student_full_name` has already created the `full_name` field.

The migration sequence is:

1. Create the new field through a schema migration.
2. Populate the field through a data migration.
3. Apply the migrations in dependency order.

### Important Concepts

- `apps.get_model()` retrieves the historical version of a model.
- `migrations.RunPython()` executes a Python function during migration.
- `schema_editor` provides access to schema-editing operations.

**Important:** Do not directly import the current model inside a data migration. Use historical models obtained through `apps.get_model()`.

---

## 11. Historical Models

Django migrations operate on historical versions of models.

A historical model represents the fields, relationships, and relevant model options at a particular point in migration history.

Use:

```python
Student = apps.get_model("students", "Student")
```

Avoid directly importing the current model:

```python
from students.models import Student
```

Direct imports can cause old migrations to fail when models change in the future.

Historical models do not necessarily include custom methods defined on the current model, such as custom `save()` methods.

---

## 12. Transactions in Migrations

A database transaction groups operations so that they can be committed or rolled back together when supported.

For databases that support DDL transactions, Django normally runs a migration's operations inside a transaction.

PostgreSQL and SQLite support transactional schema changes, while MySQL and Oracle do not provide the same transactional guarantees for all schema operations.

A migration can disable its default transaction behavior:

```python
from django.db import migrations


class Migration(migrations.Migration):

    atomic = False

    dependencies = []

    operations = []
```

The `atomic = False` setting is useful for certain advanced migration scenarios.

Use it only when you understand the transaction and recovery implications.

---

## 13. Database Backend Support

Django supports migrations across its supported database backends, although their schema alteration capabilities differ.

| Database | Important consideration |
|---|---|
| PostgreSQL | Strong transactional schema support |
| MySQL | Some schema changes cannot be rolled back transactionally |
| SQLite | Some schema changes require creating a replacement table and copying data |
| Oracle | Supports migrations, but transaction behavior differs from PostgreSQL and SQLite |

SQLite may require the following process for certain schema changes:

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

Always consider the capabilities and limitations of your database backend before applying migrations in production.

---

## 14. Migration Conflicts

Migration conflicts can occur when multiple developers create migrations from the same migration state on different branches.

Example:

```text
0001_initial.py
    |
    |----------------|
    v                v
0002_student_age.py
0002_student_email.py
```

These two migrations may create separate branches in the migration history.

Django can detect many such conflicts.

To create a merge migration when appropriate, run:

```bash
python manage.py makemigrations --merge
```

Review the generated migration and its dependencies before applying it.

A merge migration resolves the migration graph structure; it does not automatically resolve every possible logical conflict between database operations.

---

## 15. Migration Squashing

**Migration Squashing** combines multiple migrations into one or a smaller number of migration files.

For example:

```text
0001_initial.py
0002_add_age.py
0003_add_email.py
0004_add_address.py
0005_modify_name.py
```

These migrations may be combined into a squashed migration.

Command:

```bash
python manage.py squashmigrations students 0005
```

Here:
- `students` is the app label.
- `0005` is the migration up to which migrations should be squashed.

Django attempts to optimize the migration operations and generates a new migration file.

Squashing can simplify migration history in long-running projects.

**Important:** Follow Django's recommended transition process and keep the replaced migration files until all relevant environments have safely moved to the squashed migration history.

---

## 16. The `--fake-initial` Option

The `--fake-initial` option helps when introducing migrations to an app whose database tables already exist.

First, create an initial migration:

```bash
python manage.py makemigrations students
```

Then run:

```bash
python manage.py migrate --fake-initial
```

Django checks whether the tables or columns associated with certain initial migration operations already exist. If the checks pass, it can mark the initial migration as applied without recreating those objects.

**Important:** This option does not fully verify that the existing database schema matches the models. Review the schema before using it.

---

## 17. Best Practices

Follow these practices when working with Django migrations:

1. Create migrations after changing models.
2. Apply migrations in development and test the result.
3. Commit migration files to version control.
4. Commit model changes and their migrations together.
5. Use historical models in data migrations.
6. Review migration dependencies when working across apps.
7. Back up important databases before risky schema changes.
8. Test production migrations in a staging environment when possible.
9. Avoid editing migration files unnecessarily.
10. Review destructive and irreversible operations carefully.

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
| List one app's migration status | `python manage.py showmigrations students` |
| Display migration SQL | `python manage.py sqlmigrate students 0001` |
| Create an empty migration | `python manage.py makemigrations --empty students` |
| Create a merge migration | `python manage.py makemigrations --merge` |
| Squash migrations | `python manage.py squashmigrations students 0005` |
| Reverse to a specific migration | `python manage.py migrate students 0002` |
| Reverse all app migrations | `python manage.py migrate students zero` |
| Apply initial migrations to existing tables when checks pass | `python manage.py migrate --fake-initial` |

Replace `students` and migration numbers with the appropriate app label and migration identifier for your project.

---

## 19. Interview Questions and Answers

### Q1. What are Django migrations?

Django migrations record and apply changes to database schemas based on changes made to Django models.

### Q2. What is the difference between `makemigrations` and `migrate`?

- `makemigrations` creates migration files.
- `migrate` applies or reverses migration operations.

### Q3. What is `showmigrations`?

It lists migrations and indicates which migrations have been applied.

### Q4. What is `sqlmigrate`?

It displays the SQL statements Django plans to use for a specified migration.

### Q5. What is a data migration?

A data migration changes or transforms existing database records using migration operations such as `RunPython`.

### Q6. What is a migration dependency?

A migration dependency specifies another migration that must be applied first.

### Q7. What is an initial migration?

An initial migration establishes the initial database schema for an app.

### Q8. Can migrations be reversed?

Yes, if the operations support reversal. For example:

```bash
python manage.py migrate students 0002
```

### Q9. What is migration squashing?

It combines multiple migrations into a smaller number of migration files while preserving their intended effects.

### Q10. Why should migration files be committed to Git?

They allow other developers and deployment environments to reproduce the database schema changes consistently.

### Q11. Why should historical models be used in data migrations?

They ensure that migration code uses the model definition appropriate to that point in migration history.

### Q12. What is `RunPython`?

`RunPython` executes Python code as part of a migration, commonly for data transformations.

---

## 20. Key Takeaways

Remember these five essential concepts:

1. **Models:** Define the database structure in `models.py`.
2. **makemigrations:** Creates migration files from model changes.
3. **migrate:** Applies migration operations to the database.
4. **showmigrations:** Shows migration status.
5. **Data migrations:** Transform existing database data.

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

**In one sentence:** Django migrations provide a version-controlled way to manage changes to a database schema and, when needed, transform existing database data.