# Django with AJAX — Complete Notes

## Table of Contents

1. What is AJAX?
2. How AJAX works with Django
3. Different ways to use AJAX
4. Django project setup
5. Fetch API with Django
6. Fetch API with POST and JSON
7. XMLHttpRequest
8. jQuery AJAX
9. Axios
10. Django Forms with AJAX
11. AJAX CRUD operations
12. AJAX live search
13. AJAX pagination
14. AJAX file uploads
15. Class-Based Views with AJAX
16. Returning HTML partials
17. Django with HTMX
18. Django REST Framework with AJAX
19. CSRF protection
20. AJAX authentication
21. Background tasks and real-time updates
22. Common errors and solutions
23. Production best practices
24. Method comparison
25. Practice roadmap

---

## 1. What is AJAX?

AJAX stands for **Asynchronous JavaScript and XML**.

It allows JavaScript to send HTTP requests to a server and update part of a webpage without reloading the entire page.

Modern AJAX applications commonly use JSON instead of XML.

### Benefits

- Update webpage content without refreshing.
- Submit forms asynchronously.
- Implement live search and autocomplete.
- Create, read, update, and delete records.
- Upload files without a full-page reload.
- Build interactive dashboards and notifications.
- Improve user experience.

## 2. How AJAX Works with Django

The typical request flow is:

1. The user performs an action.
2. JavaScript sends an HTTP request.
3. Django receives the request through a URL.
4. A Django view processes the request.
5. The view validates input and interacts with models if necessary.
6. Django returns JSON or HTML.
7. JavaScript updates the webpage.

```text
Browser
   |
   | JavaScript AJAX request
   v
Django URL
   |
   v
Django View
   |
   v
Form / Serializer / Model
   |
   v
Database
   |
   v
JSON or HTML response
   |
   v
JavaScript updates the page
```

AJAX is a communication technique, not a Django-specific feature.

## 3. Different Ways to Use AJAX

| Method | Best use |
|---|---|
| Fetch API | Modern JavaScript applications |
| XMLHttpRequest | Legacy projects and upload progress |
| jQuery AJAX | Existing jQuery projects |
| Axios | JavaScript applications needing HTTP-client features |
| Django Forms + AJAX | Server-side form validation |
| JSON + Fetch | CRUD operations and APIs |
| HTML partials | Django template applications |
| HTMX | Interactive pages with minimal JavaScript |
| Django REST Framework | Reusable REST APIs |
| WebSockets | Real-time, two-way communication |

---

## 4. Django Project Setup

Install Django:

```bash
pip install django
```

Create a project and application:

```bash
django-admin startproject config .
python manage.py startapp products
python manage.py migrate
python manage.py runserver
```

Add the application to `config/settings.py`:

```python
INSTALLED_APPS = [
    # Default Django apps
    "products",
]
```

### Project structure

```text
project/
├── config/
│   ├── settings.py
│   └── urls.py
├── products/
│   ├── migrations/
│   ├── templates/
│   │   └── products/
│   │       └── list.html
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
└── manage.py
```

### Create a model

`products/models.py`

```python
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Configure project URLs

`config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("products/", include("products.urls")),
]
```

Create `products/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
]
```

---

## 5. Method 1 — Fetch API with Django

Fetch is a built-in JavaScript API for making HTTP requests.

### Django view

`products/views.py`

```python
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product


def product_list(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        products = list(
            Product.objects.values("id", "name", "price")
        )
        return JsonResponse({"products": products})

    return render(request, "products/list.html")
```

### HTML template

`products/templates/products/list.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Products</title>
</head>
<body>
    <h1>Product List</h1>

    <button id="load-products">Load Products</button>
    <ul id="product-list"></ul>

    <script>
        document.getElementById("load-products")
            .addEventListener("click", async () => {
                try {
                    const response = await fetch(
                        "{% url 'product_list' %}",
                        {
                            headers: {
                                "X-Requested-With": "XMLHttpRequest"
                            }
                        }
                    );

                    if (!response.ok) {
                        throw new Error("Request failed");
                    }

                    const data = await response.json();
                    const list = document.getElementById("product-list");

                    list.replaceChildren();

                    data.products.forEach(product => {
                        const li = document.createElement("li");

                        li.textContent =
                            `${product.name} - ${product.price}`;

                        list.appendChild(li);
                    });
                } catch (error) {
                    console.error(error);
                    alert("Unable to load products.");
                }
            });
    </script>
</body>
</html>
```

### How it works

1. The user clicks the button.
2. JavaScript sends a GET request.
3. Django retrieves products.
4. Django returns JSON.
5. JavaScript renders the results without reloading the page.

**Important:** `X-Requested-With` identifies a request conventionally, but it is not a security mechanism.

Fetch does not automatically reject HTTP errors such as 404 or 500. Check `response.ok`.

---

## 6. Method 2 — Fetch API with POST and JSON

Use JSON requests when JavaScript sends structured data to Django.

### Django view

```python
import json
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Product


@require_POST
def create_product(request):
    if request.content_type != "application/json":
        return JsonResponse(
            {"error": "Expected application/json"},
            status=415,
        )

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    name = data.get("name", "")
    price_value = data.get("price")

    if not isinstance(name, str) or not name.strip():
        return JsonResponse(
            {"error": "Name is required"},
            status=400,
        )

    if price_value is None:
        return JsonResponse(
            {"error": "Price is required"},
            status=400,
        )

    try:
        price = Decimal(str(price_value))

        if not price.is_finite() or price < 0:
            raise InvalidOperation

    except (InvalidOperation, ValueError):
        return JsonResponse(
            {"error": "Invalid price"},
            status=400,
        )

    product = Product.objects.create(
        name=name.strip(),
        price=price,
    )

    return JsonResponse(
        {
            "message": "Product created successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "price": str(product.price),
            },
        },
        status=201,
    )
```

### URL

```python
path("create/", views.create_product, name="create_product"),
```

### HTML and JavaScript

```html
<form id="product-form">
    {% csrf_token %}

    <input name="name" placeholder="Product name" required>
    <input
        name="price"
        type="number"
        min="0"
        step="0.01"
        placeholder="Price"
        required
    >

    <button type="submit">Save</button>
</form>

<p id="message"></p>

<script>
    const form = document.getElementById("product-form");
    const message = document.getElementById("message");

    form.addEventListener("submit", async event => {
        event.preventDefault();

        const csrfToken = form.querySelector(
            "[name=csrfmiddlewaretoken]"
        ).value;

        const formData = new FormData(form);

        try {
            const response = await fetch(
                "{% url 'create_product' %}",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken
                    },
                    body: JSON.stringify({
                        name: formData.get("name"),
                        price: formData.get("price")
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Request failed");
            }

            message.textContent = data.message;
            form.reset();

        } catch (error) {
            message.textContent = error.message;
        }
    });
</script>
```

### Important concepts

- `JSON.stringify()` converts a JavaScript object into JSON text.
- `Content-Type: application/json` identifies the request body.
- `request.body` contains the raw request body.
- `json.loads()` parses the JSON in a standard Django view.
- `JsonResponse()` returns a JSON response.
- `201 Created` indicates successful resource creation.

`request.POST` does not parse JSON request bodies.

---

## 7. Method 3 — XMLHttpRequest

XMLHttpRequest is the traditional AJAX API.

### GET request

```javascript
const xhr = new XMLHttpRequest();

xhr.open("GET", "/products/", true);

xhr.setRequestHeader(
    "X-Requested-With",
    "XMLHttpRequest"
);

xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
        const data = JSON.parse(xhr.responseText);
        console.log(data);
    } else {
        console.error("HTTP error:", xhr.status);
    }
};

xhr.onerror = function () {
    console.error("Network error");
};

xhr.send();
```

### POST request

```javascript
const xhr = new XMLHttpRequest();

xhr.open("POST", "/products/create/", true);

xhr.setRequestHeader("Content-Type", "application/json");
xhr.setRequestHeader("X-CSRFToken", csrfToken);

xhr.onload = function () {
    const data = JSON.parse(xhr.responseText);

    if (xhr.status >= 200 && xhr.status < 300) {
        console.log(data);
    } else {
        console.error(data);
    }
};

xhr.onerror = function () {
    console.error("Network error");
};

xhr.send(JSON.stringify({
    name: "Mouse",
    price: 500
}));
```

Use XMLHttpRequest when maintaining older applications or when event-based upload progress is needed.

---

## 8. Method 4 — jQuery AJAX

jQuery AJAX is useful in applications that already use jQuery.

Load jQuery before using `$`.

### GET request

```javascript
$.ajax({
    url: "/products/",
    type: "GET",
    dataType: "json",

    success: function (data) {
        console.log(data);
    },

    error: function (xhr) {
        console.error(xhr.responseJSON || xhr.statusText);
    }
});
```

### POST request with JSON

```javascript
$.ajax({
    url: "/products/create/",
    type: "POST",
    contentType: "application/json",
    dataType: "json",

    headers: {
        "X-CSRFToken": csrfToken
    },

    data: JSON.stringify({
        name: "Monitor",
        price: 12000
    }),

    success: function (data) {
        console.log(data.message);
    },

    error: function (xhr) {
        console.error(xhr.responseJSON || xhr.statusText);
    }
});
```

### POST request with form data

```javascript
$.ajax({
    url: "/products/create-form/",
    type: "POST",

    headers: {
        "X-CSRFToken": csrfToken
    },

    data: {
        name: "Headphones",
        price: "2500"
    },

    success: function (data) {
        console.log(data);
    }
});
```

When sending an ordinary object through jQuery's `data` option, jQuery normally uses form encoding. Django reads this data through `request.POST`.

### Important options

- `url`: Request endpoint.
- `type`: HTTP method.
- `data`: Request payload.
- `contentType`: Request content type.
- `dataType`: Expected response type.
- `headers`: Additional HTTP headers.
- `success`: Success callback.
- `error`: Error callback.

---

## 9. Method 5 — Axios

Axios is a third-party HTTP client.

Install it:

```bash
npm install axios
```

### GET request

```javascript
const response = await axios.get("/products/");
console.log(response.data);
```

### POST request

```javascript
const response = await axios.post(
    "/products/create/",
    {
        name: "Laptop",
        price: 65000
    },
    {
        headers: {
            "X-CSRFToken": csrfToken
        }
    }
);

console.log(response.data);
```

### Error handling

```javascript
try {
    const response = await axios.post(
        "/products/create/",
        {
            name: "Laptop",
            price: 65000
        },
        {
            headers: {
                "X-CSRFToken": csrfToken
            }
        }
    );

    console.log(response.data);

} catch (error) {
    if (error.response) {
        console.error(
            error.response.status,
            error.response.data
        );
    } else {
        console.error(error.message);
    }
}
```

Axios typically serializes ordinary JavaScript objects as JSON and parses JSON responses automatically.

---

## 10. Method 6 — Django Forms with AJAX

Django Forms and ModelForms are useful for server-side validation.

### Create a ModelForm

`products/forms.py`

```python
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price"]

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price < 0:
            raise forms.ValidationError(
                "Price cannot be negative."
            )

        return price
```

### Django view

```python
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import ProductForm


@require_http_methods(["GET", "POST"])
def product_create_form(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save()

            return JsonResponse({
                "success": True,
                "message": "Product created successfully",
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": str(product.price),
                },
            }, status=201)

        return JsonResponse({
            "success": False,
            "errors": form.errors.get_json_data(),
        }, status=400)

    return render(
        request,
        "products/form.html",
        {"form": ProductForm()},
    )
```

### Template

```html
<form id="product-form" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save Product</button>
</form>

<div id="form-errors"></div>
<p id="form-success"></p>

<script>
    const form = document.getElementById("product-form");
    const errorsBox = document.getElementById("form-errors");
    const successBox = document.getElementById("form-success");

    form.addEventListener("submit", async event => {
        event.preventDefault();

        errorsBox.replaceChildren();
        successBox.textContent = "";

        try {
            const response = await fetch(form.action || location.href, {
                method: "POST",
                headers: {
                    "X-CSRFToken": form.querySelector(
                        "[name=csrfmiddlewaretoken]"
                    ).value,
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: new FormData(form)
            });

            const data = await response.json();

            if (!response.ok) {
                Object.entries(data.errors || {}).forEach(
                    ([field, messages]) => {
                        const p = document.createElement("p");

                        p.textContent = field + ": " +
                            messages.map(item => item.message).join(", ");

                        errorsBox.appendChild(p);
                    }
                );

                if (!data.errors) {
                    errorsBox.textContent =
                        data.message || "Unable to save product.";
                }

                return;
            }

            successBox.textContent = data.message;
            form.reset();

        } catch (error) {
            errorsBox.textContent = "A network error occurred.";
        }
    });
</script>
```

### Benefits of ModelForm

- Generates fields from model definitions.
- Performs field validation.
- Supports custom validation.
- Reduces duplicate validation logic.
- Integrates with Django's model-saving workflow.

When sending `FormData`, do not manually set the multipart `Content-Type` header. The browser generates the required boundary.

---

## 11. Method 7 — AJAX CRUD Operations

CRUD means:

- Create
- Read
- Update
- Delete

| Operation | HTTP method |
|---|---|
| Create | POST |
| Read | GET |
| Update | PATCH or PUT |
| Delete | DELETE |

### Django views

The following example uses a single endpoint for listing and creating products and a detail endpoint for updating or deleting them.

```python
import json
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Product


def parse_json(request):
    try:
        return json.loads(request.body), None
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )


def product_data(product):
    return {
        "id": product.id,
        "name": product.name,
        "price": str(product.price),
    }


@require_http_methods(["GET", "POST"])
def products_api(request):
    if request.method == "GET":
        products = Product.objects.all().order_by("-id")

        return JsonResponse({
            "products": [
                product_data(product)
                for product in products
            ]
        })

    data, error = parse_json(request)

    if error:
        return error

    name = data.get("name", "")
    price_value = data.get("price")

    if not isinstance(name, str) or not name.strip():
        return JsonResponse(
            {"error": "Name is required"},
            status=400,
        )

    if price_value is None:
        return JsonResponse(
            {"error": "Price is required"},
            status=400,
        )

    try:
        price = Decimal(str(price_value))

        if not price.is_finite() or price < 0:
            raise InvalidOperation

    except (InvalidOperation, ValueError):
        return JsonResponse(
            {"error": "Invalid price"},
            status=400,
        )

    product = Product.objects.create(
        name=name.strip(),
        price=price,
    )

    return JsonResponse(
        {"product": product_data(product)},
        status=201,
    )


@require_http_methods(["PATCH", "PUT", "DELETE"])
def product_detail_api(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "DELETE":
        product.delete()

        return JsonResponse({
            "message": "Product deleted successfully"
        })

    data, error = parse_json(request)

    if error:
        return error

    if not isinstance(data, dict):
        return JsonResponse(
            {"error": "Expected a JSON object"},
            status=400,
        )

    if request.method == "PUT":
        if "name" not in data or "price" not in data:
            return JsonResponse(
                {"error": "PUT requires name and price"},
                status=400,
            )

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return JsonResponse(
                {"error": "Name cannot be empty"},
                status=400,
            )

        product.name = data["name"].strip()

    if "price" in data:
        try:
            price = Decimal(str(data["price"]))

            if not price.is_finite() or price < 0:
                raise InvalidOperation

            product.price = price

        except (InvalidOperation, ValueError):
            return JsonResponse(
                {"error": "Invalid price"},
                status=400,
            )

    product.save()

    return JsonResponse({
        "product": product_data(product)
    })
```

### URLs

```python
from django.urls import path
from . import views

urlpatterns = [
    path("api/", views.products_api, name="products_api"),
    path(
        "api/<int:pk>/",
        views.product_detail_api,
        name="product_detail_api",
    ),
]
```

### JavaScript CRUD functions

```javascript
const csrfToken = document.querySelector(
    "[name=csrfmiddlewaretoken]"
).value;

async function requestJSON(url, method = "GET", body = undefined) {
    const headers = {
        "X-CSRFToken": csrfToken
    };

    const options = {
        method,
        headers
    };

    if (body !== undefined) {
        headers["Content-Type"] = "application/json";
        options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);

    const data = response.status === 204
        ? null
        : await response.json();

    if (!response.ok) {
        throw new Error(data?.error || "Request failed");
    }

    return data;
}

// READ
async function getProducts() {
    return await requestJSON("/products/api/");
}

// CREATE
async function createProduct(name, price) {
    return await requestJSON("/products/api/", "POST", {
        name,
        price
    });
}

// UPDATE
async function updateProduct(id, fields) {
    return await requestJSON(
        `/products/api/${id}/`,
        "PATCH",
        fields
    );
}

// DELETE
async function deleteProduct(id) {
    return await requestJSON(
        `/products/api/${id}/`,
        "DELETE"
    );
}
```

### Usage

```javascript
const result = await createProduct("Keyboard", "1500");

console.log(result.product);

await updateProduct(result.product.id, {
    price: "1800"
});

await deleteProduct(result.product.id);
```

**Production note:** Add authentication, object-level authorization, field-length limits, and robust validation. The example is intended to teach AJAX CRUD, not serve as a complete production API.

---

## 12. Method 8 — AJAX Live Search

Live search requests data while the user types.

### Django view

```python
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Product


@require_GET
def product_search(request):
    query = request.GET.get("q", "").strip()

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query)
        )

    products = products.order_by("name")[:20]

    return JsonResponse({
        "products": [
            {
                "id": product.id,
                "name": product.name,
                "price": str(product.price),
            }
            for product in products
        ]
    })
```

### URL

```python
path("search/", views.product_search, name="product_search"),
```

### HTML and JavaScript

```html
<input id="search-input" placeholder="Search products...">
<ul id="results"></ul>

<script>
    const input = document.getElementById("search-input");
    const results = document.getElementById("results");

    let timer;
    let controller;

    input.addEventListener("input", () => {
        clearTimeout(timer);

        timer = setTimeout(async () => {
            if (controller) {
                controller.abort();
            }

            controller = new AbortController();

            try {
                const url = new URL(
                    "{% url 'product_search' %}",
                    window.location.origin
                );

                url.searchParams.set("q", input.value);

                const response = await fetch(url, {
                    signal: controller.signal
                });

                if (!response.ok) {
                    throw new Error("Search failed");
                }

                const data = await response.json();

                results.replaceChildren();

                data.products.forEach(product => {
                    const li = document.createElement("li");

                    li.textContent =
                        `${product.name} - ${product.price}`;

                    results.appendChild(li);
                });

            } catch (error) {
                if (error.name !== "AbortError") {
                    console.error(error);
                }
            }
        }, 300);
    });
</script>
```

### Important concepts

- **Debouncing:** Delays a request until the user pauses typing.
- **AbortController:** Cancels an outdated request.
- **`icontains`:** Performs case-insensitive partial matching.
- **URLSearchParams:** Encodes query parameters safely.

For large datasets, use pagination and optimize database queries.

---

## 13. Method 9 — AJAX Pagination

Django's `Paginator` can provide paginated JSON results.

### Django view

```python
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage,
)
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Product


@require_GET
def product_pagination(request):
    paginator = Paginator(
        Product.objects.order_by("id"),
        10,
    )

    try:
        page = paginator.page(request.GET.get("page", 1))

    except (PageNotAnInteger, EmptyPage):
        return JsonResponse(
            {"error": "Invalid page number"},
            status=400,
        )

    return JsonResponse({
        "products": [
            {
                "id": product.id,
                "name": product.name,
                "price": str(product.price),
            }
            for product in page.object_list
        ],
        "current_page": page.number,
        "num_pages": paginator.num_pages,
        "has_next": page.has_next(),
        "has_previous": page.has_previous(),
    })
```

### JavaScript

```javascript
async function loadPage(page = 1) {
    const response = await fetch(
        `/products/paginated/?page=${page}`
    );

    if (!response.ok) {
        throw new Error("Unable to load page");
    }

    const data = await response.json();

    console.log("Products:", data.products);
    console.log("Current page:", data.current_page);
    console.log("Total pages:", data.num_pages);
    console.log("Has next:", data.has_next);
    console.log("Has previous:", data.has_previous);

    // Render products and update pagination controls.
}
```

Call `loadPage(1)` initially, then `loadPage(2)` when the user clicks Next.

---

## 14. Method 10 — AJAX File Upload

Use `FormData` to upload files without a full-page reload.

Install Pillow:

```bash
pip install Pillow
```

### Django model

```python
from django.db import models


class ProductImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="products/")
```

### Media settings

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

### Django view

```python
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import ProductImage


@require_POST
def upload_image(request):
    title = request.POST.get("title", "").strip()
    image = request.FILES.get("image")

    if not title or not image:
        return JsonResponse(
            {"error": "Title and image are required"},
            status=400,
        )

    # Add file-size, content-type, file-format,
    # and authorization checks before saving.
    obj = ProductImage.objects.create(
        title=title,
        image=image,
    )

    return JsonResponse({
        "message": "Upload successful",
        "id": obj.id,
        "title": obj.title,
    }, status=201)
```

### HTML and JavaScript

```html
<form id="upload-form" enctype="multipart/form-data">
    {% csrf_token %}

    <input type="text" name="title" required>

    <input
        type="file"
        name="image"
        accept="image/*"
        required
    >

    <button type="submit">Upload</button>
</form>

<p id="upload-message"></p>

<script>
    const uploadForm = document.getElementById("upload-form");

    uploadForm.addEventListener("submit", async event => {
        event.preventDefault();

        const formData = new FormData(uploadForm);

        const csrfToken = uploadForm.querySelector(
            "[name=csrfmiddlewaretoken]"
        ).value;

        try {
            const response = await fetch(
                "{% url 'upload_image' %}",
                {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken
                    },
                    body: formData
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Upload failed");
            }

            document.getElementById("upload-message").textContent =
                data.message;

            uploadForm.reset();

        } catch (error) {
            document.getElementById("upload-message").textContent =
                error.message;
        }
    });
</script>
```

### Important points

- Files arrive in `request.FILES`.
- Text fields arrive in `request.POST`.
- `FormData` sends multipart form data.
- Do not manually set `Content-Type` when sending `FormData`.
- Validate file sizes, content, formats, and permissions.
- Configure production media storage appropriately.

---

## 15. Method 11 — Class-Based Views with AJAX

Django class-based views can handle AJAX requests just like function-based views.

```python
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from .forms import ProductForm


@method_decorator(csrf_protect, name="dispatch")
class ProductCreateView(View):

    def get(self, request):
        return render(
            request,
            "products/form.html",
            {"form": ProductForm()},
        )

    def post(self, request):
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save()

            return JsonResponse({
                "success": True,
                "id": product.id,
                "name": product.name,
            }, status=201)

        return JsonResponse({
            "success": False,
            "errors": form.errors.get_json_data(),
        }, status=400)
```

### URL

```python
path(
    "class-based-create/",
    views.ProductCreateView.as_view(),
    name="product_create_cbv",
),
```

Use CBVs when reusable behavior and inheritance help organize your application. Function-based views can be simpler for small endpoints.

---

## 16. Method 12 — Returning HTML Partials

AJAX can return rendered HTML instead of JSON.

This approach is useful when Django templates should handle rendering.

### Django view

```python
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Product


@require_GET
def product_list_partial(request):
    products = Product.objects.all().order_by("name")

    return render(
        request,
        "products/_product_list.html",
        {"products": products},
    )
```

### Partial template

`products/templates/products/_product_list.html`

```html
<ul>
    {% for product in products %}
        <li>
            {{ product.name|escape }} - {{ product.price }}
        </li>
    {% empty %}
        <li>No products found.</li>
    {% endfor %}
</ul>
```

### Main template

```html
<div id="product-container"></div>

<button id="refresh-products">Refresh</button>

<script>
    document.getElementById("refresh-products")
        .addEventListener("click", async () => {
            const response = await fetch(
                "{% url 'product_list_partial' %}"
            );

            if (!response.ok) {
                throw new Error("Unable to load products");
            }

            const html = await response.text();

            document.getElementById("product-container")
                .innerHTML = html;
        });
</script>
```

### JSON versus HTML

- Use JSON when JavaScript needs structured data.
- Use HTML partials when Django should render the interface.
- Avoid inserting untrusted user-generated HTML directly into the DOM.
- Use `textContent` for untrusted text.

---

## 17. Method 13 — Django with HTMX

HTMX allows HTML attributes to trigger AJAX requests and replace parts of a page with HTML returned by Django.

### Example

```html
<script src="https://unpkg.com/htmx.org@2.0.4"></script>

<button
    hx-get="{% url 'product_list_partial' %}"
    hx-target="#products"
    hx-swap="innerHTML">
    Load Products
</button>

<div id="products">
    Click the button to load products.
</div>
```

The Django view can use the `product_list_partial` example from the previous section.

### Benefits

- Minimal custom JavaScript.
- HTML-driven requests.
- Simple partial-page updates.
- Natural integration with Django templates.

HTMX is useful for dashboards, admin interfaces, search results, and pagination.

For production, pin and maintain an appropriate HTMX version, preferably self-hosted or loaded from a trusted source.

---

## 18. Method 14 — Django REST Framework with AJAX

DRF is useful for reusable APIs consumed by websites, mobile applications, or third-party clients.

Install:

```bash
pip install djangorestframework
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "rest_framework",
]
```

### Serializer

`products/serializers.py`

```python
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
```

### API views

`products/api_views.py`

```python
from rest_framework import generics, permissions

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
```

### URLs

```python
from django.urls import path
from . import api_views

urlpatterns = [
    path(
        "api/v1/products/",
        api_views.ProductListCreateAPIView.as_view(),
        name="api_product_list",
    ),
    path(
        "api/v1/products/<int:pk>/",
        api_views.ProductDetailAPIView.as_view(),
        name="api_product_detail",
    ),
]
```

### Fetch GET request

```javascript
const response = await fetch("/products/api/v1/products/");

if (!response.ok) {
    throw new Error("Failed to retrieve products");
}

const products = await response.json();

console.log(products);
```

### Fetch POST request

For session-authenticated writes, include the CSRF token:

```javascript
const response = await fetch("/products/api/v1/products/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
    },
    body: JSON.stringify({
        name: "USB Hub",
        price: "1200.00"
    })
});

const data = await response.json();

if (!response.ok) {
    console.error(data);
}
```

Authentication alone does not guarantee permission to modify a particular product. Add appropriate object-level authorization for private resources.

### ViewSets and routers

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
```

Configure a router:

```python
from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet

router = DefaultRouter()

router.register(
    "products",
    ProductViewSet,
    basename="product",
)

urlpatterns = router.urls
```

DRF is not required for every AJAX request. Standard Django views are appropriate for many template-based applications.

---

## 19. Method 15 — CSRF Protection

CSRF stands for Cross-Site Request Forgery.

Django protects unsafe HTTP methods using CSRF protection when the relevant middleware and view protections are enabled.

### Get the token from a form

```html
<form id="my-form">
    {% csrf_token %}
</form>
```

```javascript
const csrfToken = document.querySelector(
    "#my-form [name=csrfmiddlewaretoken]"
).value;
```

### Get the token from a cookie

This method works only if the cookie is accessible to JavaScript.

```javascript
function getCookie(name) {
    const cookies = document.cookie.split(";");

    for (const cookie of cookies) {
        const item = cookie.trim();

        if (item.startsWith(name + "=")) {
            return decodeURIComponent(
                item.substring(name.length + 1)
            );
        }
    }

    return null;
}

const csrfToken = getCookie("csrftoken");
```

### Send the token in Fetch

```javascript
await fetch("/products/api/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
    },
    body: JSON.stringify({
        name: "Webcam",
        price: "4000"
    })
});
```

### Important security rules

- Keep Django's CSRF protection enabled.
- Never disable CSRF just to make AJAX work.
- A CSRF cookie may be configured as HttpOnly.
- Cross-origin deployments require careful CORS, CSRF, and cookie configuration.
- CORS is not a replacement for CSRF protection.
- Token-based authentication has its own security considerations.

For pages without a form, `ensure_csrf_cookie` can be used to ensure the CSRF cookie is set.

---

## 20. Method 16 — AJAX Authentication

Django session authentication can work with AJAX.

### Basic login view

```python
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@require_POST
def ajax_login(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if user is None:
        return JsonResponse(
            {
                "success": False,
                "error": "Invalid credentials",
            },
            status=400,
        )

    login(request, user)

    return JsonResponse({
        "success": True,
        "message": "Login successful",
    })
```

### Submit the form

```javascript
const formData = new FormData(loginForm);

const response = await fetch("/ajax-login/", {
    method: "POST",
    headers: {
        "X-CSRFToken": csrfToken
    },
    body: formData
});

const data = await response.json();
```

### Security considerations

- Include a valid CSRF token.
- Use HTTPS in production.
- Apply login throttling and abuse prevention.
- Avoid logging passwords or session tokens.
- Protect private endpoints with authentication and authorization.
- Configure cookie and session settings appropriately.

---

## 21. Method 17 — Background Tasks and Real-Time Updates

AJAX does not automatically make slow backend operations faster. It allows the browser to communicate asynchronously.

For long-running operations, such as generating reports or sending emails, consider this architecture:

1. JavaScript submits a request.
2. Django validates the request.
3. Django queues a background task.
4. Django returns a task ID.
5. JavaScript polls a status endpoint.
6. Django returns the task status.

Celery is one option for background processing.

For real-time, two-way communication, consider Django Channels and WebSockets. WebSockets differ from ordinary AJAX request-response communication.

Django signals can help decouple model-related actions, but signals alone are not a background task queue.

---

## 22. Common Errors and Solutions

| Error | Possible cause | Solution |
|---|---|---|
| 400 Bad Request | Invalid input or JSON | Validate the payload |
| 403 Forbidden | Missing or invalid CSRF token | Send a valid token |
| 404 Not Found | Incorrect endpoint URL | Check Django URLs |
| 405 Method Not Allowed | Unsupported HTTP method | Use the allowed method |
| 415 Unsupported Media Type | Incorrect content type | Match the endpoint's expected format |
| 500 Internal Server Error | Backend exception | Inspect Django logs |
| Unexpected token `<` | HTML received instead of JSON | Inspect the response body |
| `request.POST` is empty | JSON body sent | Parse `request.body` |
| Page reloads after submit | Default form submission | Use `event.preventDefault()` |
| Duplicate submissions | Repeated button clicks | Disable the button while submitting |
| Outdated search results | Requests finish out of order | Use AbortController or sequence IDs |
| CORS error | Cross-origin request blocked | Configure origins and credentials correctly |

### Debugging checklist

1. Open browser developer tools.
2. Select the Network tab.
3. Trigger the AJAX request.
4. Check the request URL and method.
5. Inspect request headers and payload.
6. Check the response status and body.
7. Inspect the Django terminal for exceptions.

---

## 23. Production Best Practices

- Use Django URL reversing instead of hardcoded URLs where practical.
- Validate all incoming data on the server.
- Use ModelForms or DRF serializers for structured validation.
- Keep CSRF protection enabled.
- Check `response.ok` with Fetch.
- Use appropriate HTTP status codes.
- Implement authentication and object-level authorization.
- Use pagination for large datasets.
- Optimize database queries.
- Prevent duplicate submissions.
- Handle network failures gracefully.
- Use `textContent` for untrusted text.
- Validate uploaded files and enforce file-size limits.
- Use HTTPS in production.
- Never expose secret keys or private API credentials in frontend JavaScript.
- Write tests for validation, permissions, status codes, and failures.

---

## 24. Comparison of All Methods

| Method | JavaScript required | Response | Best use |
|---|---|---|---|
| Fetch API | Yes | JSON or HTML | Modern applications |
| XMLHttpRequest | Yes | JSON or HTML | Legacy applications and upload progress |
| jQuery AJAX | Yes, plus jQuery | JSON or HTML | Existing jQuery projects |
| Axios | Yes, plus Axios | JSON or HTML | Larger JavaScript applications |
| Django Form + AJAX | Some | JSON or HTML | Server-side validation |
| HTML partials | Yes | HTML | Template-based applications |
| HTMX | Minimal | HTML | Interactive server-rendered pages |
| DRF + Fetch/Axios | Yes | Usually JSON | REST APIs and mobile clients |
| WebSockets | Yes | Real-time events | Live notifications and chat |

---

## 25. Practice Roadmap

### Beginner

- [ ] Create a Django project and application.
- [ ] Create a Product model.
- [ ] Retrieve products using Fetch and JsonResponse.
- [ ] Submit a form without a page reload.
- [ ] Display success and error messages.

### Intermediate

- [ ] Implement complete AJAX CRUD.
- [ ] Implement live search with debouncing.
- [ ] Add server-side pagination.
- [ ] Upload images using FormData.
- [ ] Validate forms using ModelForm.
- [ ] Implement CSRF protection.
- [ ] Handle network errors.

### Advanced

- [ ] Create a Django REST Framework API.
- [ ] Implement serializers and permissions.
- [ ] Add authentication and object-level authorization.
- [ ] Build an interactive dashboard.
- [ ] Explore HTMX.
- [ ] Add background tasks using Celery.
- [ ] Explore WebSockets with Django Channels.
- [ ] Write automated tests.

---

## Final Recommendation

For a Django backend developer, learn AJAX in this order:

1. Fetch API and JsonResponse.
2. POST requests and JSON.
3. Django Forms with AJAX.
4. CRUD operations.
5. CSRF protection and authentication.
6. Live search, pagination, and file uploads.
7. Django REST Framework with Fetch or Axios.
8. HTMX, background tasks, and WebSockets.

**Core concept:** AJAX is the frontend communication mechanism. Django views, forms, models, authentication, and serializers determine how the backend processes each request.
