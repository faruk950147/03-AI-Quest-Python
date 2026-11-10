# Professional Business Inventory Management System

## Complete Project Documentation

**Backend:** Django 5.2  
**API:** Django REST Framework  
**Database:** PostgreSQL  
**Frontend:** Django Templates + Bootstrap 5  
**Authentication:** Django Authentication + JWT  
**Language:** Python  
**Timezone:** Asia/Dhaka

---

# Table of Contents

1. [Project Overview](#1-project-overview)
2. [Main Features](#2-main-features)
3. [Technology Stack](#3-technology-stack)
4. [Project Architecture](#4-project-architecture)
5. [Installation](#5-installation)
6. [Requirements](#6-requirements)
7. [Environment Configuration](#7-environment-configuration)
8. [Django Settings](#8-django-settings)
9. [Database Architecture](#9-database-architecture)
10. [Custom User Model](#10-custom-user-model)
11. [Company and Branch Management](#11-company-and-branch-management)
12. [Role-Based Access Control](#12-role-based-access-control)
13. [Product and Category Management](#13-product-and-category-management)
14. [Authentication](#14-authentication)
15. [API Architecture](#15-api-architecture)
16. [Inventory Management](#16-inventory-management)
17. [Purchase Management](#17-purchase-management)
18. [Sales Management](#18-sales-management)
19. [Supplier and Customer Management](#19-supplier-and-customer-management)
20. [Expense Management](#20-expense-management)
21. [Reports and Dashboard](#21-reports-and-dashboard)
22. [Frontend Architecture](#22-frontend-architecture)
23. [Security](#23-security)
24. [Testing](#24-testing)
25. [Migration and Development Commands](#25-migration-and-development-commands)
26. [Development Roadmap](#26-development-roadmap)

---

# 1. Project Overview

Professional Business Inventory Management System একটি Multi-Company এবং Multi-Branch Inventory Management Software।

এই সফটওয়্যারের মাধ্যমে একাধিক কোম্পানি তাদের ব্যবসার Product, Purchase, Sales, Stock, Supplier, Customer, Expense এবং Financial Reports পরিচালনা করতে পারবে।

প্রতিটি কোম্পানির ডেটা আলাদা থাকবে।

একজন User একাধিক কোম্পানিতে বিভিন্ন Role নিয়ে কাজ করতে পারবে।

## Project Objectives

- Business inventory management.
- Multiple company management.
- Multiple branch management.
- Product and category management.
- Supplier and customer management.
- Purchase invoice management.
- Sales invoice management.
- Stock management.
- Payment management.
- Expense management.
- Profit and loss calculation.
- Business analytics.
- REST API integration.

---

# 2. Main Features

## Authentication

- User registration.
- User login.
- User logout.
- Password change.
- Password reset.
- JWT authentication.
- Session authentication.

## Company Management

- Create company.
- Update company.
- Company profile.
- Company selection.
- Multiple companies per user.

## Branch Management

- Create branch.
- Update branch.
- Branch selection.
- Branch-specific inventory.
- Branch-specific sales.
- Branch-specific purchases.

## User Management

- Owner.
- Admin.
- Manager.
- Staff.
- Sales person.
- Inventory manager.

## Product Management

- Create product.
- Update product.
- Archive product.
- Product image.
- SKU.
- Barcode.
- Purchase price.
- Selling price.
- Product category.
- Product search.

## Inventory Management

- Stock in.
- Stock out.
- Stock adjustment.
- Stock transfer.
- Stock history.
- Low-stock alerts.
- Branch-wise stock.

## Purchase Management

- Create purchase invoice.
- Add purchase items.
- Receive purchase.
- Supplier payment.
- Partial payment.
- Purchase history.

## Sales Management

- Create sales invoice.
- Add sales items.
- Complete sale.
- Customer payment.
- Partial payment.
- Sales history.
- Sales return.

## Financial Management

- Expense tracking.
- Supplier payable.
- Customer receivable.
- Profit calculation.
- Loss calculation.
- Financial reports.

---

# 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django 5.2 | Web framework |
| Django REST Framework | REST APIs |
| PostgreSQL | Relational database |
| Bootstrap 5 | Frontend UI |
| Django Templates | HTML rendering |
| Simple JWT | Token authentication |
| django-filter | API filtering |
| Pillow | Image processing |
| python-decouple | Environment configuration |

---

# 4. Project Architecture

```text
business_inventory/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/
│   ├── accounts/
│   ├── companies/
│   ├── products/
│   ├── suppliers/
│   ├── customers/
│   ├── inventory/
│   ├── purchases/
│   ├── sales/
│   ├── expenses/
│   └── reports/
│
├── templates/
│   ├── base.html
│   ├── accounts/
│   ├── companies/
│   ├── dashboard/
│   ├── products/
│   ├── suppliers/
│   ├── customers/
│   ├── inventory/
│   ├── purchases/
│   ├── sales/
│   ├── expenses/
│   └── reports/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
├── manage.py
├── requirements.txt
├── .env
└── .gitignore
```

## Application Responsibilities

| App | Responsibility |
|---|---|
| accounts | User authentication |
| companies | Company, branch and membership |
| products | Product and category |
| suppliers | Supplier management |
| customers | Customer management |
| inventory | Stock and transactions |
| purchases | Purchase invoices |
| sales | Sales invoices |
| expenses | Business expenses |
| reports | Reports and analytics |

---

# 5. Installation

## Step 1: Create project directory

```bash
mkdir business_inventory
cd business_inventory
```

## Step 2: Create virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

## Step 3: Install Django

```bash
pip install django==5.2
```

## Step 4: Install dependencies

```bash
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-filter
pip install "psycopg[binary]"
pip install Pillow
pip install python-decouple
```

## Step 5: Create Django project

```bash
django-admin startproject config .
```

## Step 6: Create applications

```bash
mkdir apps
```

```bash
python manage.py startapp accounts apps/accounts
python manage.py startapp companies apps/companies
python manage.py startapp products apps/products
python manage.py startapp suppliers apps/suppliers
python manage.py startapp customers apps/customers
python manage.py startapp inventory apps/inventory
python manage.py startapp purchases apps/purchases
python manage.py startapp sales apps/sales
python manage.py startapp expenses apps/expenses
```

প্রতিটি App-এর `apps.py`-তে `name` সঠিকভাবে `apps.accounts`, `apps.companies` ইত্যাদি সেট করতে হবে।

---

# 6. Requirements

`requirements.txt`

```text
Django==5.2
djangorestframework
djangorestframework-simplejwt
django-filter
psycopg[binary]
Pillow
python-decouple
```

Install:

```bash
pip install -r requirements.txt
```

---

# 7. Environment Configuration

Project root-এ `.env` ফাইল তৈরি করুন।

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=business_inventory
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Production environment-এ `DEBUG=False` রাখতে হবে এবং শক্তিশালী secret key ব্যবহার করতে হবে।

---

# 8. Django Settings

`config/settings.py`

```python
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1"
).split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",

    "apps.accounts",
    "apps.companies",
    "apps.products",
    "apps.suppliers",
    "apps.customers",
    "apps.inventory",
    "apps.purchases",
    "apps.sales",
    "apps.expenses",
]

AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "company-list"
LOGOUT_REDIRECT_URL = "login"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "30/minute",
        "user": "300/minute",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

---

# 9. Database Architecture

প্রধান database relationships:

```text
User
  |
  |---- CompanyMembership
              |
              |---- Company
              |
              |---- BranchMembership
                          |
                          |---- Branch

Company
  |
  |---- Category
  |
  |---- Product
  |
  |---- Supplier
  |
  |---- Customer
  |
  |---- Branch
  |
  |---- Purchase
  |
  |---- Sale
```

## Important Database Rules

1. প্রতিটি business record-এর Company reference থাকতে হবে।
2. Branch অবশ্যই নির্দিষ্ট Company-এর অধীনে থাকবে।
3. Product-এর SKU একটি Company-এর মধ্যে unique হবে।
4. Purchase-এর Product একই Company-এর হতে হবে।
5. Sales-এর Product একই Company-এর হতে হবে।
6. Stock হবে Branch এবং Product অনুযায়ী।
7. Financial amount-এর জন্য `DecimalField` ব্যবহার করতে হবে।
8. Stock পরিবর্তনের জন্য transaction service ব্যবহার করতে হবে।

---

# 10. Custom User Model

`apps/accounts/models.py`

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return self.username
```

`settings.py`

```python
AUTH_USER_MODEL = "accounts.User"
```

**Important:** Custom User Model অবশ্যই প্রথম migration-এর আগে configure করতে হবে।

---

# 11. Company and Branch Management

`apps/companies/models.py`

```python
from django.conf import settings
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    tax_number = models.CharField(max_length=100, blank=True)

    logo = models.ImageField(
        upload_to="companies/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Branch(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="branches"
    )

    name = models.CharField(max_length=150)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_branch_name_per_company"
            )
        ]

    def __str__(self):
        return f"{self.company.name} - {self.name}"


class CompanyMembership(models.Model):

    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("staff", "Staff"),
        ("sales", "Sales Person"),
        ("inventory", "Inventory Manager"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_memberships"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="staff"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "user"],
                name="unique_company_user_membership"
            )
        ]


class BranchMembership(models.Model):

    membership = models.ForeignKey(
        CompanyMembership,
        on_delete=models.CASCADE,
        related_name="branch_memberships"
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["membership", "branch"],
                name="unique_membership_branch"
            )
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.membership.company_id != self.branch.company_id:
            raise ValidationError(
                "Branch must belong to the membership company."
            )
```

## Company Service

`apps/companies/services.py`

```python
from django.db import transaction

from apps.companies.models import (
    Company,
    Branch,
    CompanyMembership,
    BranchMembership,
)


@transaction.atomic
def create_company_with_owner(
    user,
    name,
    phone,
    email=""
):
    company = Company.objects.create(
        name=name,
        phone=phone,
        email=email
    )

    membership = CompanyMembership.objects.create(
        company=company,
        user=user,
        role="owner"
    )

    return company, membership


@transaction.atomic
def create_branch(
    membership,
    name,
    address="",
    phone=""
):
    if not membership.is_active:
        raise ValueError("Inactive membership.")

    if membership.role not in ("owner", "admin"):
        raise ValueError("You cannot create branches.")

    branch = Branch.objects.create(
        company=membership.company,
        name=name,
        address=address,
        phone=phone
    )

    BranchMembership.objects.create(
        membership=membership,
        branch=branch
    )

    return branch


def assign_user_to_branch(membership, branch):

    if not membership.is_active:
        raise ValueError("Inactive membership.")

    if membership.company_id != branch.company_id:
        raise ValueError("Branch belongs to another company.")

    return BranchMembership.objects.get_or_create(
        membership=membership,
        branch=branch
    )
```

---

# 12. Role-Based Access Control

`apps/companies/permissions.py`

```python
ROLE_PERMISSIONS = {

    "owner": {
        "product_view",
        "product_add",
        "product_change",
        "product_delete",
        "branch_manage",
        "sales_manage",
        "purchase_manage",
        "inventory_manage",
        "report_view",
        "user_manage",
    },

    "admin": {
        "product_view",
        "product_add",
        "product_change",
        "product_delete",
        "branch_manage",
        "sales_manage",
        "purchase_manage",
        "inventory_manage",
        "report_view",
        "user_manage",
    },

    "manager": {
        "product_view",
        "product_add",
        "product_change",
        "sales_manage",
        "purchase_manage",
        "inventory_manage",
        "report_view",
    },

    "staff": {
        "product_view",
    },

    "sales": {
        "product_view",
        "sales_manage",
    },

    "inventory": {
        "product_view",
        "inventory_manage",
    },
}


def get_membership(user, company):

    return company.memberships.filter(
        user=user,
        is_active=True
    ).first()


def has_company_permission(
    user,
    company,
    permission
):

    membership = get_membership(
        user,
        company
    )

    if not membership:
        return False

    return permission in ROLE_PERMISSIONS.get(
        membership.role,
        set()
    )
```

**Security rule:** Client থেকে পাঠানো Company ID কখনো access permission-এর প্রমাণ নয়। Server-এ User-এর active membership যাচাই করতে হবে।

---

# 13. Product and Category Management

`apps/products/models.py`

```python
from django.db import models
from apps.companies.models import Company


class Category(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="categories"
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_category_per_company"
            )
        ]

    def __str__(self):
        return self.name


class Product(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100)
    barcode = models.CharField(
        max_length=100,
        blank=True
    )

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    unit = models.CharField(
        max_length=30,
        default="pcs"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-id"]

        constraints = [
            models.UniqueConstraint(
                fields=["company", "sku"],
                name="unique_company_product_sku"
            )
        ]

    def __str__(self):
        return self.name
```

## Product Service

`apps/products/services.py`

```python
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.products.models import Product


@transaction.atomic
def create_product(
    membership,
    category,
    name,
    sku,
    purchase_price,
    selling_price,
    barcode="",
    unit="pcs",
    image=None,
    is_active=True
):

    if not membership.is_active:
        raise ValidationError("Inactive membership.")

    if category.company_id != membership.company_id:
        raise ValidationError("Invalid category.")

    if membership.role not in (
        "owner",
        "admin",
        "manager"
    ):
        raise ValidationError(
            "You cannot create products."
        )

    if purchase_price < 0 or selling_price < 0:
        raise ValidationError(
            "Price cannot be negative."
        )

    if Product.objects.filter(
        company=membership.company,
        sku=sku
    ).exists():
        raise ValidationError(
            "SKU already exists."
        )

    return Product.objects.create(
        company=membership.company,
        category=category,
        name=name,
        sku=sku,
        purchase_price=purchase_price,
        selling_price=selling_price,
        barcode=barcode,
        unit=unit,
        image=image,
        is_active=is_active
    )
```

## Product Business Rules

- SKU must be unique within a company.
- Category must belong to the same company.
- Product prices cannot be negative.
- Archived products should not appear in normal product lists.
- Historical purchase and sales records must preserve their product references.
- Product deletion should normally be soft deletion using `is_active=False`.

---

# 14. Authentication

Authentication system-এর প্রধান features:

- Login.
- Logout.
- Password validation.
- JWT access token.
- JWT refresh token.
- Authenticated page protection.

Logout অবশ্যই POST request হতে হবে।

Custom user model migration-এর পর authentication implementation করতে হবে।

---

# 15. API Architecture

API endpoints:

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/token/` | Login |
| POST | `/api/auth/refresh/` | Refresh JWT |
| GET | `/api/products/` | Product list |
| POST | `/api/products/` | Create product |
| GET | `/api/products/{id}/` | Product detail |
| PUT | `/api/products/{id}/` | Update product |
| PATCH | `/api/products/{id}/` | Partial update |
| DELETE | `/api/products/{id}/` | Archive product |

## API Authentication Header

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
X-Company-ID: 1
```

`X-Company-ID` শুধু active company context নির্বাচন করবে। User ওই company-এর active member কি না, সেটি backend-এ যাচাই করতে হবে।

---

# 16. Inventory Management

Inventory system হলো এই project-এর সবচেয়ে গুরুত্বপূর্ণ অংশগুলোর একটি।

## Stock Model Design

`apps/inventory/models.py`-এর জন্য প্রয়োজনীয় fields:

### Stock

- company
- branch
- product
- quantity
- updated_at

### StockTransaction

- company
- branch
- product
- transaction_type
- quantity
- reference_type
- reference_id
- note
- created_by
- created_at

## Transaction Types

| Type | Meaning |
|---|---|
| purchase | Stock in |
| sale | Stock out |
| adjustment_in | Manual stock increase |
| adjustment_out | Manual stock decrease |
| transfer_in | Branch stock received |
| transfer_out | Branch stock sent |
| sales_return | Returned sales stock |
| purchase_return | Returned purchase stock |

## Inventory Rules

1. Stock কখনো negative হবে না।
2. Purchase receive হলে stock বাড়বে।
3. Sale complete হলে stock কমবে।
4. Draft purchase stock পরিবর্তন করবে না।
5. Draft sale stock পরিবর্তন করবে না।
6. Cancelled invoice stock পরিবর্তন করবে না।
7. প্রতিটি stock movement-এর transaction history থাকতে হবে।
8. একই invoice একাধিকবার process করা যাবে না।
9. Stock update atomic database transaction-এর মধ্যে করতে হবে।
10. Branch এবং Product একই Company-এর হতে হবে।

---

# 17. Purchase Management

Purchase management supplier থেকে পণ্য কেনার প্রক্রিয়া পরিচালনা করবে।

## Purchase Model

প্রস্তাবিত fields:

- company
- branch
- supplier
- invoice_number
- purchase_date
- subtotal
- discount
- tax
- grand_total
- paid_amount
- due_amount
- status
- created_by
- created_at

## PurchaseItem Model

- purchase
- product
- quantity
- unit_price
- discount
- tax
- line_total

## Purchase Status

| Status | Meaning |
|---|---|
| draft | Invoice তৈরি হয়েছে |
| received | Stock receive হয়েছে |
| cancelled | Invoice বাতিল |

## Purchase Workflow

```text
Create Purchase
       |
       v
Add Purchase Items
       |
       v
Calculate Total
       |
       v
Save as Draft
       |
       v
Receive Purchase
       |
       v
Update Stock
       |
       v
Create Stock Transactions
```

## Important Purchase Rules

- Purchase product অবশ্যই একই company-এর হতে হবে।
- Supplier একই company-এর হতে হবে।
- Branch একই company-এর হতে হবে।
- Draft purchase stock বাড়াবে না।
- Receive করার সময় stock বাড়বে।
- Invoice number company অনুযায়ী unique হবে।
- Partial payment support থাকতে হবে।
- Purchase receive operation idempotent হতে হবে।

---

# 18. Sales Management

Sales management customer-এর কাছে পণ্য বিক্রির প্রক্রিয়া পরিচালনা করবে।

## Sale Model

প্রস্তাবিত fields:

- company
- branch
- customer
- invoice_number
- sale_date
- subtotal
- discount
- tax
- grand_total
- paid_amount
- due_amount
- status
- created_by
- created_at

## SaleItem Model

- sale
- product
- quantity
- unit_price
- discount
- tax
- line_total

## Sale Status

| Status | Meaning |
|---|---|
| draft | Invoice draft |
| completed | Sale completed |
| cancelled | Sale cancelled |

## Sales Workflow

```text
Create Sale
     |
     v
Add Products
     |
     v
Check Stock
     |
     v
Calculate Invoice
     |
     v
Save Draft
     |
     v
Complete Sale
     |
     v
Deduct Stock
     |
     v
Create Stock Transactions
```

## Important Sales Rules

- Sale product অবশ্যই একই company-এর হতে হবে।
- Sale branch একই company-এর হতে হবে।
- Available stock-এর বেশি বিক্রি করা যাবে না।
- Sale complete হলে stock কমবে।
- Draft sale stock কমাবে না।
- Invoice number company অনুযায়ী unique হবে।
- Sale complete একাধিকবার করা যাবে না।
- Partial payment এবং due amount support থাকতে হবে।

---

# 19. Supplier and Customer Management

## Supplier Model

প্রস্তাবিত fields:

- company
- name
- contact_person
- email
- phone
- address
- opening_balance
- is_active
- created_at

## Customer Model

প্রস্তাবিত fields:

- company
- name
- email
- phone
- address
- opening_balance
- is_active
- created_at

## Supplier Features

- Supplier create.
- Supplier update.
- Supplier archive.
- Purchase history.
- Payment history.
- Supplier payable report.

## Customer Features

- Customer create.
- Customer update.
- Customer archive.
- Sales history.
- Payment history.
- Customer receivable report.

---

# 20. Expense Management

Expense management দিয়ে business-এর অন্যান্য খরচ track করা হবে।

## ExpenseCategory

- company
- name
- description

## Expense

- company
- branch
- category
- title
- amount
- expense_date
- note
- attachment
- created_by

## Example Expenses

- Rent.
- Electricity bill.
- Internet bill.
- Transport.
- Employee salary.
- Maintenance.
- Office supplies.

## Expense Rules

- Expense amount negative হতে পারবে না।
- Expense category একই company-এর হতে হবে।
- Expense branch একই company-এর হতে হবে।
- Expense record-এর creator track করতে হবে।

---

# 21. Reports and Dashboard

## Dashboard Cards

- Total Products.
- Total Stock Value.
- Today's Sales.
- Today's Purchase.
- Total Customers.
- Total Suppliers.
- Total Expenses.
- Outstanding Receivables.
- Outstanding Payables.

## Reports

### Sales Reports

- Daily sales.
- Weekly sales.
- Monthly sales.
- Yearly sales.
- Product-wise sales.
- Branch-wise sales.

### Purchase Reports

- Daily purchase.
- Monthly purchase.
- Supplier-wise purchase.
- Branch-wise purchase.

### Inventory Reports

- Current stock.
- Low stock.
- Out-of-stock products.
- Stock movement.
- Stock valuation.

### Financial Reports

- Revenue.
- Cost of Goods Sold.
- Gross Profit.
- Expenses.
- Net Profit.
- Customer receivables.
- Supplier payables.

## Profit Calculation

```text
Gross Profit = Sales Revenue - Cost of Goods Sold

Net Profit = Gross Profit - Operating Expenses
```

একটি সঠিক financial report তৈরির জন্য stock valuation method, discounts, taxes, returns এবং payment accounting-এর নিয়ম আগে নির্ধারণ করতে হবে।

---

# 22. Frontend Architecture

Frontend-এর জন্য Django Templates এবং Bootstrap 5 ব্যবহার করা হবে।

## Base Template

`templates/base.html`

এতে থাকবে:

- Navbar.
- Sidebar.
- Main content.
- Footer.
- Bootstrap CSS.
- Bootstrap JavaScript.
- Message alerts.

## Dashboard

`templates/dashboard/index.html`

এতে থাকবে:

- Summary cards.
- Sales chart.
- Purchase chart.
- Low-stock products.
- Recent sales.
- Recent purchases.

## Product Pages

```text
templates/products/
    list.html
    form.html
    detail.html
    confirm_delete.html
```

## Purchase Pages

```text
templates/purchases/
    list.html
    form.html
    detail.html
    receive_confirm.html
```

## Sales Pages

```text
templates/sales/
    list.html
    form.html
    detail.html
    invoice.html
```

---

# 23. Security

এই project-এ security অত্যন্ত গুরুত্বপূর্ণ।

## Multi-Tenant Security

- Every query must be company-scoped.
- Every branch must belong to the active company.
- User membership must be checked on the server.
- Client-supplied company ID must never be trusted.
- Object-level access must be checked.
- API list endpoints must filter by company.

## Database Security

- Use database constraints.
- Use `transaction.atomic()`.
- Use `select_for_update()` for critical stock updates.
- Prevent duplicate invoice processing.
- Use `DecimalField` for financial values.
- Validate foreign-key ownership.

## Web Security

- CSRF protection.
- Secure password hashing.
- Login protection.
- Permission checks.
- File upload validation.
- Environment-based secrets.
- HTTPS in production.

---

# 24. Testing

প্রতিটি app-এর জন্য tests লিখতে হবে।

## Accounts Tests

- User login.
- Invalid password.
- Logout.
- Password validation.

## Company Tests

- Company creation.
- Membership creation.
- Branch creation.
- Cross-company branch rejection.
- Unauthorized company access.

## Product Tests

- Product creation.
- Duplicate SKU rejection.
- Negative price rejection.
- Cross-company category rejection.
- Product archive.

## Inventory Tests

- Purchase increases stock.
- Sale decreases stock.
- Negative stock prevention.
- Duplicate transaction prevention.
- Branch isolation.

## Purchase Tests

- Draft purchase does not update stock.
- Receive purchase updates stock.
- Duplicate receive prevention.
- Invalid company product rejection.

## Sales Tests

- Draft sale does not update stock.
- Complete sale decreases stock.
- Insufficient stock rejection.
- Duplicate completion prevention.

Run tests:

```bash
python manage.py test
```

---

# 25. Migration and Development Commands

## Make migrations

```bash
python manage.py makemigrations
```

## Apply migrations

```bash
python manage.py migrate
```

## Create superuser

```bash
python manage.py createsuperuser
```

## Run development server

```bash
python manage.py runserver
```

## Run tests

```bash
python manage.py test
```

## Collect static files

```bash
python manage.py collectstatic
```

## Check project configuration

```bash
python manage.py check
```

---

# 26. Development Roadmap

| Part | Module | Status |
|---|---|---|
| 1 | Project setup and architecture | Planned |
| 2 | Authentication, company, branch, RBAC, products | Initial notes prepared |
| 3 | Suppliers and customers | Pending |
| 4 | Inventory and stock transactions | Pending |
| 5 | Purchase management | Pending |
| 6 | Sales management | Pending |
| 7 | Payment management | Pending |
| 8 | Expense management | Pending |
| 9 | Dashboard and reports | Pending |
| 10 | Complete frontend | Pending |
| 11 | Testing and security | Pending |
| 12 | Production deployment | Pending |

---

# Important Development Notes

1. প্রথমে Custom User Model configure করতে হবে।
2. তারপর Company এবং Membership তৈরি করতে হবে।
3. Product ও অন্যান্য business data company-scoped হতে হবে।
4. Purchase এবং Sales-এর জন্য service layer ব্যবহার করতে হবে।
5. Stock update সরাসরি views থেকে করা যাবে না।
6. Financial calculation-এর জন্য Decimal ব্যবহার করতে হবে।
7. Invoice receive/complete operation atomic হতে হবে।
8. Duplicate stock movement প্রতিরোধ করতে হবে।
9. Product delete না করে archive করতে হবে।
10. Production deployment-এর আগে সব tests চালাতে হবে।

---

## Project Completion Checklist

- [ ] Project setup
- [ ] PostgreSQL configuration
- [ ] Custom User model
- [ ] Authentication
- [ ] Company management
- [ ] Branch management
- [ ] Membership and RBAC
- [ ] Product CRUD
- [ ] Supplier CRUD
- [ ] Customer CRUD
- [ ] Inventory management
- [ ] Stock transactions
- [ ] Purchase management
- [ ] Sales management
- [ ] Payment management
- [ ] Expense management
- [ ] Dashboard
- [ ] Reports
- [ ] REST API
- [ ] Bootstrap frontend
- [ ] Automated tests
- [ ] Security review
- [ ] Production deployment

---

**Documentation Note:** এটি পুরো project-এর architecture, database design, business rules, implementation roadmap এবং Part 1–2-এর প্রধান code reference। এটি সম্পূর্ণ executable source code নয়। প্রতিটি pending module-এর models, services, serializers, views, URLs, templates এবং tests আলাদাভাবে implement ও verify করতে হবে।
