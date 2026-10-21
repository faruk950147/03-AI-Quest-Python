# Django ORM — Complete Notes

## 1. Aggregation

Definition: Aggregation is used to calculate a summary from multiple database records.

Import:
```python
from django.db.models import Sum, Avg, Max, Min, Count
```

Example:
```python
Product.objects.aggregate(
    total=Sum("price"),
    average=Avg("price"),
    highest=Max("price"),
    lowest=Min("price"),
    count=Count("id")
)
```

Common functions:
- Sum() — Total sum
- Avg() — Average value
- Max() — Maximum value
- Min() — Minimum value
- Count() — Number of records

Note: aggregate() usually returns a dictionary.

## 2. Annotation

Definition: Annotation adds a calculated value or extra information to each record in a QuerySet.

Import:
```python
from django.db.models import F
```

Example:
```python
products = Product.objects.annotate(
    total_value=F("price") * F("stock")
)

for product in products:
    print(product.name, product.total_value)
```

Note: annotate() adds a calculated attribute to each object.

### Aggregation vs Annotation

- Aggregation: Returns a summary result.
- Annotation: Adds calculated values to individual records.
- aggregate() usually returns a dictionary.
- annotate() returns a QuerySet.

## 3. F Expressions

Definition: F() references a database field without retrieving its value into Python first.

Import:
```python
from django.db.models import F
```

Example 1: Increase stock by one.
```python
Product.objects.filter(id=1).update(
    stock=F("stock") + 1
)
```

Example 2: Compare two fields.
```python
Product.objects.filter(
    stock__gt=F("price")
)
```

Uses:
- Compare database fields.
- Perform arithmetic inside the database.
- Reduce race conditions during database updates.

Example 3: without F().
```python
product = Product.objects.get(id=1)

product.stock = product.stock + 1
product.save()
```

## 4. Conditional Expressions

Definition: Conditional expressions generate results based on conditions, similar to if/else.

Import:
```python
from django.db.models import Case, When, Value, CharField
```

Example:
```python
products = Product.objects.annotate(
    status=Case(
        When(stock=0, then=Value("Out")),
        When(stock__lt=5, then=Value("Low")),
        default=Value("Available"),
        output_field=CharField()
    )
)
```

Important components:
- Case() — Defines conditional logic.
- When() — Defines a condition.
- Value() — Represents a literal value.
- default — Result when no condition matches.
- output_field — Specifies the output field type.

## 5. Database Functions

Definition: Database functions perform operations on text, numbers, and dates inside the database.

Import:
```python
from django.db.models.functions import (
    Upper, Lower, Length, Coalesce, Abs, Round, Now
)
```

Example:
```python
products = Product.objects.annotate(
    upper_name=Upper("name"),
    name_length=Length("name")
)
```

Common functions:
- Upper() — Converts text to uppercase.
- Lower() — Converts text to lowercase.
- Length() — Returns text length.
- Abs() — Returns absolute value.
- Round() — Rounds a number.
- Coalesce() — Returns the first non-NULL value.
- Now() — Returns the current date and time.

## 6. Coalesce

Definition: Coalesce() returns the first non-NULL expression.

Import:
```python
from django.db.models import Value
from django.db.models.functions import Coalesce
```

Example:
```python
products = Product.objects.annotate(
    actual_discount=Coalesce(
        "discount",
        Value(0)
    )
)
```

Results:
- discount = 10 → actual_discount = 10
- discount = NULL → actual_discount = 0

Use: Provide a default value when a field is NULL.

## 7. Subquery

Definition: Subquery allows an inner query to provide a value for an outer query.

Import:
```python
from django.db.models import OuterRef, Subquery
```

Example: Get the latest post title for each author.
```python
latest_post = Post.objects.filter(
    author=OuterRef("pk")
).order_by("-id")

authors = Author.objects.annotate(
    latest_title=Subquery(
        latest_post.values("title")[:1]
    )
)
```

Important:
- Subquery() — Uses the result of an inner query.
- OuterRef() — References a field from the outer query.
- [:1] — Limits the inner query to one row.

## 8. Exists

Definition: Exists checks whether a matching record exists and returns a Boolean result.

Import:
```python
from django.db.models import Exists, OuterRef
```

Example: Check whether each author has posts.
```python
posts = Post.objects.filter(
    author=OuterRef("pk")
)

authors = Author.objects.annotate(
    has_posts=Exists(posts)
)
```

Subquery vs Exists:
- Subquery() — Retrieves a value from another query.
- Exists() — Checks whether matching records exist.

## 9. Managers

Definition: A Manager provides the interface for database queries on a Django model.

Default Manager:
```python
Product.objects.all()
Product.objects.filter(price__gt=1000)
```

Custom Manager example:
```python
class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            stock__gt=0
        )
```

Model example:
```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField()

    objects = models.Manager()
    available = AvailableManager()
```

Usage:
```python
Product.objects.all()
Product.available.all()
```

Note: Product.available.all() returns products with stock greater than zero.

## 10. Custom QuerySets

Definition: Custom QuerySets allow developers to create reusable database query methods.

Example:
```python
class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.filter(stock__gt=0)

    def expensive(self):
        return self.filter(price__gte=10000)
```

Model example:
```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    stock = models.IntegerField()

    objects = ProductQuerySet.as_manager()
```

Usage:
```python
Product.objects.available()
Product.objects.expensive()
Product.objects.available().expensive()
```

Note: as_manager() exposes suitable QuerySet methods through the Manager.

## Quick Revision

- Aggregation — Summary calculation.
- Annotation — Calculated values for each record.
- F Expressions — Reference database fields.
- Conditional Expressions — Generate results based on conditions.
- Database Functions — Process text, numbers, and dates.
- Coalesce — Return the first non-NULL value.
- Subquery — Use an inner query's result.
- Exists — Check whether matching records exist.
- Managers — Entry point for model queries.
- Custom QuerySets — Create reusable query methods.

## Recommended Learning Order

1. Aggregation
2. Annotation
3. F Expressions
4. Conditional Expressions
5. Database Functions and Coalesce
6. Subquery and Exists
7. Managers and Custom QuerySets
