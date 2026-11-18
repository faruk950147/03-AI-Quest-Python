# POST https://sandbox.sslcommerz.com/gwprocess/v4/api.php
store_id: xstor6aed594d3b6a9
store_passwd: YOUR_STORE_PASSWORD
total_amount: 100.00
currency: BDT
tran_id: TXN_1793939825
success_url: https://sandbox-gw.sslcommerz.com/success
fail_url: https://sandbox-gw.sslcommerz.com/fail
cancel_url: https://sandbox-gw.sslcommerz.com/cancel
ipn_url: https://sandbox-gw.sslcommerz.com/ipn
cus_name: Customer Name
cus_email: customer@example.com
cus_add1: Dhaka
cus_city: Dhaka
cus_postcode: 1000
cus_country: Bangladesh
cus_phone: 01711111111
shipping_method: NO
product_name: Computer
product_category: Electronic
product_profile: general


========================================================================
# Payment Gateway Integration — Full Notes
## Sandbox/Test to Live/Production
### Example: Django REST Framework + PostgreSQL + SSLCommerz

---

# 1. What is a Payment Gateway?

A Payment Gateway is a service that allows customers to make online payments using different payment methods.

Examples:
- SSLCommerz
- aamarPay
- ShurjoPay
- Stripe
- PayPal

### Example

ধরো, একটি E-commerce website-এ একজন customer একটি product কিনবে।

Product Price: ৳1,000

Customer: Rahim

Payment Method: SSLCommerz

Payment Flow:

1. Customer selects a product.
2. Customer clicks the Pay Now button.
3. Backend creates an order.
4. Backend creates a payment request.
5. Payment Gateway receives the request.
6. Customer redirects to the payment page.
7. Customer completes payment.
8. Gateway sends the payment result to the backend.
9. Backend verifies the payment.
10. Order status becomes CONFIRMED.

---

# 2. Sandbox vs Live Environment

Payment gateways generally provide two environments.

## Sandbox / Test Environment

Sandbox is used for development and testing.

Features:
- Fake transactions.
- Test credentials.
- No real money is transferred.
- Developers can test success, failure and cancellation.
- Useful for debugging and integration.

Example:

```env
PAYMENT_MODE=sandbox
```

SSLCommerz Sandbox URL:

```text
https://sandbox.sslcommerz.com
```

## Live / Production Environment

Live is used for real transactions.

Features:
- Real customer payments.
- Real merchant credentials.
- Actual money transactions.
- Requires business verification and provider approval.

Example:

```env
PAYMENT_MODE=live
```

SSLCommerz Live URL:

```text
https://securepay.sslcommerz.com
```

### Main Difference

| Sandbox | Live |
|---|---|
| Test transaction | Real transaction |
| Test credentials | Live credentials |
| No real money | Real money |
| Development | Production |
| Testing | Actual business |

**Important:** Never use live credentials in local development or commit credentials to GitHub.

---

# 3. Complete Payment Gateway Integration Workflow

## Step 1: Create a Sandbox Account

Developer creates a test account with the payment gateway provider.

Collect:
- Store ID
- Store Password / Secret Key
- Sandbox API URL
- API Documentation

Example:

```env
SSLCOMMERZ_STORE_ID=test_store_id
SSLCOMMERZ_STORE_PASSWORD=test_store_password
```

These are fictional example values.

## Step 2: Read API Documentation

Read the official documentation before implementation.

Understand:
- Authentication
- Payment initiation API
- Payment validation API
- Success callback
- Fail callback
- Cancel callback
- IPN / Webhook
- Refund API
- Error responses

Documentation:

https://developer.sslcommerz.com/

## Step 3: Design the System Architecture

Example architecture:

```text
Frontend
   |
   | Pay Now
   v
Django REST API
   |
   | Create Order
   v
PostgreSQL Database
   |
   | Create Payment
   v
Payment Gateway API
   |
   | Redirect Customer
   v
Gateway Payment Page
   |
   | Customer Pays
   v
Gateway Server
   |
   | Success / IPN
   v
Django Backend
   |
   | Verify Transaction
   v
PostgreSQL Database
   |
   v
Order Confirmed
```

## Step 4: Database Design

We need at least two tables:

1. Order
2. Payment

### Order Model

```python
# orders/models.py

import uuid
from django.db import models


class Order(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    customer_name = models.CharField(max_length=100)

    customer_email = models.EmailField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
```

### Payment Model

```python
# payments/models.py

import uuid
from django.db import models
from orders.models import Order


class Payment(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("CANCELLED", "Cancelled"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name="payments"
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )

    gateway_transaction_id = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10,
        default="BDT"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    gateway_response = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_id
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 4. Project Structure

Example Django project structure:

```text
payment_project/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│
├── orders/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│
├── payments/
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── views.py
│   ├── urls.py
│
├── .env
├── .gitignore
└── manage.py
```

Install packages:

```bash
pip install django djangorestframework
pip install psycopg2-binary
pip install requests python-decouple
```

---

# 5. Environment Configuration

Create a `.env` file:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

PAYMENT_MODE=sandbox

SSLCOMMERZ_STORE_ID=your_store_id
SSLCOMMERZ_STORE_PASSWORD=your_store_password

BACKEND_URL=http://127.0.0.1:8000
FRONTEND_URL=http://localhost:3000

DB_NAME=payment_db
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

Load environment variables:

```python
# settings.py

from decouple import config

PAYMENT_MODE = config("PAYMENT_MODE", default="sandbox")

SSLCOMMERZ_STORE_ID = config("SSLCOMMERZ_STORE_ID")

SSLCOMMERZ_STORE_PASSWORD = config(
    "SSLCOMMERZ_STORE_PASSWORD"
)

BACKEND_URL = config("BACKEND_URL")

FRONTEND_URL = config("FRONTEND_URL")
```

Add `.env` to `.gitignore`:

```text
.env
__pycache__/
*.pyc
venv/
```

---

# 6. SSLCommerz Payment Service

Create:

`payments/services.py`

This service handles communication with SSLCommerz.

```python
import requests

from django.conf import settings


class SSLCommerzService:

    SANDBOX_URL = "https://sandbox.sslcommerz.com"

    LIVE_URL = "https://securepay.sslcommerz.com"

    @classmethod
    def get_base_url(cls):

        if settings.PAYMENT_MODE == "live":
            return cls.LIVE_URL

        return cls.SANDBOX_URL

    @classmethod
    def initiate_payment(cls, payment, order):

        url = (
            f"{cls.get_base_url()}"
            "/gwprocess/v4/api.php"
        )

        payload = {
            "store_id": settings.SSLCOMMERZ_STORE_ID,
            "store_passwd": settings.SSLCOMMERZ_STORE_PASSWORD,

            "total_amount": str(payment.amount),
            "currency": payment.currency,

            "tran_id": payment.transaction_id,

            "success_url": (
                f"{settings.BACKEND_URL}/api/payments/success/"
            ),

            "fail_url": (
                f"{settings.BACKEND_URL}/api/payments/fail/"
            ),

            "cancel_url": (
                f"{settings.BACKEND_URL}/api/payments/cancel/"
            ),

            "ipn_url": (
                f"{settings.BACKEND_URL}/api/payments/ipn/"
            ),

            "cus_name": order.customer_name,
            "cus_email": order.customer_email,

            "cus_add1": "Bangladesh",
            "cus_city": "Dhaka",
            "cus_country": "Bangladesh",

            "cus_phone": "01700000000",

            "shipping_method": "NO",
            "product_name": "E-commerce Product",
            "product_category": "General",
            "product_profile": "general",

            "num_of_item": 1,
        }

        response = requests.post(
            url,
            data=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    @classmethod
    def verify_payment(cls, val_id):

        url = (
            f"{cls.get_base_url()}"
            "/validator/api/validationserverAPI.php"
        )

        params = {
            "val_id": val_id,
            "store_id": settings.SSLCOMMERZ_STORE_ID,
            "store_passwd": settings.SSLCOMMERZ_STORE_PASSWORD,
            "format": "json",
        }

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()
```

**Note:** This is an educational service example. Check the current provider documentation for required fields, callback behavior, validation response fields and API changes.

---

# 7. Payment Initiation API

When a customer clicks Pay Now, the backend creates a payment record and requests a payment session from the gateway.

```python
# payments/views.py

import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from payments.models import Payment
from payments.services import SSLCommerzService


class InitiatePaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        order_id = request.data.get("order_id")

        try:
            order = Order.objects.get(
                id=order_id,
                customer_email=request.user.email,
                status="PENDING"
            )

        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        payment = Payment.objects.create(
            order=order,
            transaction_id=f"TXN-{uuid.uuid4().hex}",
            amount=order.total_amount,
            currency="BDT"
        )

        try:
            gateway_response = (
                SSLCommerzService.initiate_payment(
                    payment,
                    order
                )
            )

        except Exception:
            payment.status = "FAILED"
            payment.save(update_fields=["status", "updated_at"])

            return Response(
                {"error": "Payment gateway unavailable"},
                status=status.HTTP_502_BAD_GATEWAY
            )

        if (
            gateway_response.get("status") != "SUCCESS"
            or not gateway_response.get("GatewayPageURL")
        ):
            payment.status = "FAILED"
            payment.gateway_response = gateway_response
            payment.save()

            return Response(
                {
                    "error": "Payment initiation failed",
                    "details": gateway_response
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.gateway_response = {
            "sessionkey": gateway_response.get("sessionkey")
        }
        payment.save(update_fields=[
            "gateway_response",
            "updated_at"
        ])

        return Response({
            "message": "Payment session created",
            "transaction_id": payment.transaction_id,
            "payment_url": gateway_response["GatewayPageURL"]
        })
```

### API Endpoint

```text
POST /api/payments/initiate/
```

Example request:

```json
{
    "order_id": "YOUR_ORDER_UUID"
}
```

Example response:

```json
{
    "message": "Payment session created",
    "transaction_id": "TXN-EXAMPLE123",
    "payment_url": "https://sandbox.sslcommerz.com/example"
}
```

The payment URL above is illustrative, not a real session URL.

Frontend redirects the customer to the returned payment URL.

---

# 8. Payment Verification

This is one of the most important parts of payment integration.

Never trust only the success redirect from the browser.

The backend must verify the transaction directly with the payment gateway.

### What should be verified?

1. Gateway transaction status.
2. Transaction ID.
3. Amount.
4. Currency.
5. Merchant / Store ID.
6. Payment record status.
7. Associated order status.

Example:

```python
# payments/services.py

from decimal import Decimal, InvalidOperation

from django.db import transaction

from orders.models import Order
from payments.models import Payment


def complete_payment(payment, result):

    if result.get("status") not in ["VALID", "VALIDATED"]:
        return False

    if result.get("tran_id") != payment.transaction_id:
        return False

    if result.get("currency") != payment.currency:
        return False

    if result.get("store_id") != settings.SSLCOMMERZ_STORE_ID:
        return False

    try:
        verified_amount = Decimal(str(result.get("amount")))
    except (InvalidOperation, TypeError, ValueError):
        return False

    if verified_amount != payment.amount:
        return False

    with transaction.atomic():

        locked_payment = (
            Payment.objects
            .select_for_update()
            .get(id=payment.id)
        )

        locked_order = (
            Order.objects
            .select_for_update()
            .get(id=locked_payment.order_id)
        )

        # Idempotency: repeated callbacks must not process twice.
        if locked_payment.status == "SUCCESS":
            return True

        if locked_payment.status != "PENDING":
            return False

        if locked_order.status != "PENDING":
            return False

        locked_payment.status = "SUCCESS"

        locked_payment.gateway_transaction_id = (
            result.get("bank_tran_id", "")
        )

        locked_payment.gateway_response = result

        locked_payment.save()

        locked_order.status = "CONFIRMED"

        locked_order.save(update_fields=[
            "status",
            "updated_at"
        ])

    return True
```

The example assumes the provider returns these fields. Confirm exact field names and merchant identifiers from the current API response documentation.

---

# 9. Success Callback API

After successful payment, the gateway redirects the customer to the success URL.

Example callback:

```text
/api/payments/success/?tran_id=TXN-123&val_id=VAL-123
```

The backend must verify the payment with the gateway before confirming the order.

```python
# payments/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from payments.models import Payment
from payments.services import (
    SSLCommerzService,
    complete_payment
)


class PaymentSuccessView(APIView):

    authentication_classes = []
    permission_classes = []
    # Apply the callback/CSRF policy required by the provider.
    # Do not use CSRF exemption as a substitute for verification.

    def get(self, request):

        tran_id = request.query_params.get("tran_id")
        val_id = request.query_params.get("val_id")

        if not tran_id or not val_id:
            return Response(
                {"error": "Missing transaction information"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment = Payment.objects.get(
                transaction_id=tran_id
            )
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            result = SSLCommerzService.verify_payment(val_id)
        except Exception:
            return Response(
                {"error": "Payment verification unavailable"},
                status=status.HTTP_502_BAD_GATEWAY
            )

        if not complete_payment(payment, result):
            return Response(
                {"error": "Payment verification failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "message": "Payment successful",
            "transaction_id": tran_id
        })
```

---

# 10. IPN / Webhook Integration

## What is IPN?

IPN means Instant Payment Notification.

It is a server-to-server notification sent by the payment gateway to the merchant backend.

Why is IPN important?

The customer may:
- Close the browser.
- Lose internet connection.
- Leave the payment page.
- Fail to return to the website after payment.

The gateway can still notify the backend.

### IPN Flow

```text
Customer
   |
   v
Payment Gateway
   |
   | Payment completed
   v
Gateway Server
   |
   | IPN Request
   v
Merchant Backend
   |
   | Verify Transaction
   v
Database Updated
   |
   v
Order Confirmed
```

### IPN API Example

```python
class PaymentIPNView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        tran_id = request.data.get("tran_id")
        val_id = request.data.get("val_id")

        if not tran_id or not val_id:
            return Response(
                {"error": "Invalid IPN payload"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment = Payment.objects.get(
                transaction_id=tran_id
            )
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            result = SSLCommerzService.verify_payment(val_id)
        except Exception:
            return Response(
                {"error": "Verification unavailable"},
                status=status.HTTP_502_BAD_GATEWAY
            )

        if not complete_payment(payment, result):
            return Response(
                {"error": "Invalid payment"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "message": "IPN processed"
        })
```

**Important:** IPN is not automatically trusted. Follow the provider's signature, source verification, request method and validation requirements. Always verify the transaction server-to-server.

---

# 11. Fail and Cancel Callback

Payment can fail or be cancelled.

These states should not confirm an order.

Example:

```python
from django.db import transaction


class PaymentFailView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        tran_id = request.data.get("tran_id")

        if not tran_id:
            return Response(
                {"error": "Missing transaction ID"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            try:
                payment = (
                    Payment.objects
                    .select_for_update()
                    .get(transaction_id=tran_id)
                )
            except Payment.DoesNotExist:
                return Response(
                    {"error": "Payment not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if payment.status == "PENDING":
                payment.status = "FAILED"
                payment.save()

        return Response({"message": "Payment failed"})


class PaymentCancelView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        tran_id = request.data.get("tran_id")

        if not tran_id:
            return Response(
                {"error": "Missing transaction ID"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            try:
                payment = (
                    Payment.objects
                    .select_for_update()
                    .get(transaction_id=tran_id)
                )
            except Payment.DoesNotExist:
                return Response(
                    {"error": "Payment not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if payment.status == "PENDING":
                payment.status = "CANCELLED"
                payment.save()

        return Response({"message": "Payment cancelled"})
```

**Important:** Production implementations must verify failure/cancellation callbacks according to the gateway's documented callback rules. Do not let an unverified request arbitrarily change a successful payment to FAILED or CANCELLED.

---

# 12. URL Configuration

Create:

`payments/urls.py`

```python
from django.urls import path

from payments.views import (
    InitiatePaymentView,
    PaymentSuccessView,
    PaymentFailView,
    PaymentCancelView,
    PaymentIPNView,
)

urlpatterns = [

    path(
        "initiate/",
        InitiatePaymentView.as_view(),
        name="payment-initiate"
    ),

    path(
        "success/",
        PaymentSuccessView.as_view(),
        name="payment-success"
    ),

    path(
        "fail/",
        PaymentFailView.as_view(),
        name="payment-fail"
    ),

    path(
        "cancel/",
        PaymentCancelView.as_view(),
        name="payment-cancel"
    ),

    path(
        "ipn/",
        PaymentIPNView.as_view(),
        name="payment-ipn"
    ),
]
```

Main project URL:

```python
# config/urls.py

from django.urls import path, include

urlpatterns = [

    path(
        "api/payments/",
        include("payments.urls")
    ),

]
```

---

# 13. Postman Testing

Postman is used to test backend APIs before frontend integration.

## Test 1: Initiate Payment

Method:

```text
POST
```

URL:

```text
http://127.0.0.1:8000/api/payments/initiate/
```

Headers:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

Body:

```json
{
    "order_id": "YOUR_ORDER_UUID"
}
```

Expected response:

```json
{
    "message": "Payment session created",
    "transaction_id": "TXN-EXAMPLE123",
    "payment_url": "GATEWAY_PAYMENT_URL"
}
```

## Test 2: Success Callback

Normally the payment gateway invokes this endpoint.

For manual testing, use a mock gateway response or a proper sandbox transaction. Do not mark an order successful by manually submitting fake callback fields.

## Test 3: IPN

Method:

```text
POST
```

URL:

```text
http://127.0.0.1:8000/api/payments/ipn/
```

Use the exact callback payload defined by the provider.

## Test 4: Verify Database

Check the Payment table:

```text
status = SUCCESS
```

Check the Order table:

```text
status = CONFIRMED
```

---

# 14. Frontend Integration

After receiving the payment URL from the backend, redirect the customer to the gateway.

Example JavaScript:

```javascript
async function payNow(orderId) {

    const response = await fetch(
        "http://127.0.0.1:8000/api/payments/initiate/",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            },

            body: JSON.stringify({
                order_id: orderId
            })
        }
    );

    const data = await response.json();

    if (response.ok && data.payment_url) {
        window.location.href = data.payment_url;
    } else {
        alert(data.error || "Payment initiation failed");
    }
}
```

Frontend should display the final payment status by querying the backend. A redirect alone is not proof of payment.

---

# 15. Business Document Verification

Before enabling live payment, the gateway provider may request business documents.

Examples:
- Trade License
- NID of owner / authorized person
- TIN / e-TIN
- Business bank account information
- Company registration documents
- Website URL
- Product or service information
- Contact information

Required documents depend on provider, merchant type and applicable regulations.

### Verification Process

1. Client submits business documents.
2. Provider reviews documents.
3. Provider may request additional information.
4. Provider approves the merchant account.
5. Provider enables live credentials and payment facilities.

---

# 16. UAT — User Acceptance Testing

UAT means User Acceptance Testing.

It verifies that the payment integration works as expected for the business.

Test scenarios:

| Scenario | Expected Result |
|---|---|
| Successful payment | Order confirmed |
| Failed payment | Payment failed |
| Cancelled payment | Payment cancelled |
| Invalid transaction | Rejected |
| Wrong amount | Rejected |
| Wrong currency | Rejected |
| Duplicate IPN | No duplicate processing |
| Browser closed | IPN can update payment |
| Gateway timeout | Safe retry / pending state |
| Repeated success callback | No duplicate order processing |

The client and payment provider may review the application before live approval.

---

# 17. Switch Sandbox to Live

After approval, the provider supplies live credentials.

Example:

```env
PAYMENT_MODE=live

SSLCOMMERZ_STORE_ID=LIVE_STORE_ID
SSLCOMMERZ_STORE_PASSWORD=LIVE_STORE_PASSWORD
```

The service selects the live API URL based on the environment.

Important checklist:

- Replace sandbox credentials with live credentials.
- Confirm live API URLs.
- Configure production callback URLs.
- Configure IPN URL in the merchant dashboard if required.
- Enable HTTPS / SSL.
- Confirm production database settings.
- Test a real low-value transaction where appropriate.
- Confirm refund and settlement procedures.
- Never expose secret credentials to the frontend.

Never paste real credentials into source code or public repositories.

---

# 18. IPN Configuration in Merchant Dashboard

The merchant dashboard may provide an IPN configuration field.

Example:

```text
https://api.example.com/api/payments/ipn/
```

Configure the exact production endpoint.

Requirements:
- Publicly accessible HTTPS URL.
- Correct HTTP method.
- Correct request parsing.
- Provider-required verification.
- Reliable response handling.
- Proper logging and monitoring.

The exact IPN configuration process depends on the gateway.

---

# 19. Important Security Practices

Payment integration handles financial transactions, so security is essential.

1. Never trust frontend payment status.
2. Never confirm an order from a browser redirect alone.
3. Verify transactions with the gateway server-to-server.
4. Match transaction ID, amount, currency and merchant account.
5. Use HTTPS in production.
6. Keep API secrets in environment variables or a secrets manager.
7. Never expose store passwords in frontend JavaScript.
8. Use authentication and order ownership checks.
9. Use database transactions and row locks.
10. Implement idempotency for callbacks and IPNs.
11. Keep payment and order statuses consistent.
12. Log transaction references without logging passwords or sensitive data.
13. Add timeout and retry handling.
14. Reconcile pending transactions with the provider.
15. Test duplicate and out-of-order callbacks.
16. Restrict administrative access to payment records.

---

# 20. Additional Production Considerations

The examples above demonstrate the main integration flow. A production system should also implement:

### A. Atomic Payment Creation

Create the payment record and related business state safely using database transactions.

### B. Idempotency

Repeated gateway callbacks must not process the same payment twice.

### C. Transaction Reconciliation

Periodically compare pending local payments with gateway transaction records.

### D. Refund Support

Implement refund requests using the provider's documented refund API.

### E. Payment Retry

Allow customers to retry failed or expired payment sessions safely.

### F. Audit Logs

Store relevant payment events for debugging and financial audits.

### G. Monitoring

Monitor:
- Gateway API failures.
- Payment verification failures.
- Pending transactions.
- Duplicate callbacks.
- Refund failures.

### H. Automated Tests

Test:
- Successful verification.
- Invalid transaction ID.
- Incorrect amount.
- Incorrect currency.
- Invalid merchant ID.
- Duplicate callback.
- Gateway timeout.
- Concurrent callback requests.

---

# 21. Complete Payment Flow Example

Suppose:

```text
Customer Name: Rahim
Product: Laptop
Product Price: ৳1,000
Order ID: ORD-1001
Transaction ID: TXN-1001
Payment Gateway: SSLCommerz
```

### Step-by-step execution

Step 1: Rahim clicks Pay Now.

Step 2: Django creates an order.

```text
Order ID: ORD-1001
Amount: 1000.00
Status: PENDING
```

Step 3: Django creates a payment.

```text
Transaction ID: TXN-1001
Amount: 1000.00
Status: PENDING
```

Step 4: Django sends the payment request to SSLCommerz.

Step 5: SSLCommerz returns a GatewayPageURL.

Step 6: Frontend redirects Rahim to the gateway.

Step 7: Rahim completes payment.

Step 8: Gateway sends a callback / IPN.

Step 9: Django calls the payment validation API.

Step 10: Django verifies:

```text
Transaction ID: TXN-1001
Amount: 1000.00
Currency: BDT
Status: VALID
```

Step 11: Django updates the database.

Payment:

```text
Status: SUCCESS
```

Order:

```text
Status: CONFIRMED
```

Step 12: Frontend shows the successful payment result.

---

# 22. Payment Status Lifecycle

```text
             Payment Initiated
                    |
                    v
                  PENDING
                    |
        +-----------+-----------+
        |           |           |
        v           v           v
     SUCCESS      FAILED     CANCELLED
        |
        v
   Order Confirmed
```

A failed or cancelled payment should not confirm the order.

A payment may remain pending temporarily when the gateway response is delayed. Reconciliation is needed before treating it as permanently failed.

---

# 23. Common Errors and Solutions

| Error | Possible Solution |
|---|---|
| Invalid Store ID | Check merchant credentials |
| Invalid Password | Check store password / secret |
| Invalid Amount | Verify order amount |
| Invalid Currency | Use supported currency |
| Gateway URL missing | Check initiation API response |
| Callback not received | Check public callback URL |
| IPN not working | Check merchant dashboard settings |
| SSL error | Configure valid HTTPS |
| Duplicate callback | Implement idempotency |
| Payment pending | Verify transaction and reconcile |
| Payment mismatch | Compare amount, currency and transaction ID |

---

# 24. Important Interview Questions and Answers

### Q1. What is a Payment Gateway?

A payment gateway is a service that securely processes online payment transactions between customers, merchants and financial institutions.

### Q2. What is Sandbox?

Sandbox is a testing environment where developers can test payment integration without transferring real money.

### Q3. What is Live Environment?

Live is the production environment where real customer payments are processed.

### Q4. What is IPN?

IPN stands for Instant Payment Notification. It is a server-to-server notification sent by the payment gateway to inform the merchant backend about a transaction event.

### Q5. What is a Callback URL?

A callback URL is an endpoint where the payment gateway sends or redirects the customer after a payment event.

### Q6. Why do we verify payment?

Because browser redirects and callback data alone cannot be trusted. The backend must validate the transaction with the gateway.

### Q7. What is Transaction ID?

A transaction ID is a unique identifier used to track a payment.

### Q8. What happens if the customer closes the browser?

The gateway may still send an IPN to the backend. The backend can verify the transaction and update the order.

### Q9. What is UAT?

UAT means User Acceptance Testing. It checks whether the integrated system meets the business requirements.

### Q10. Why do we use environment variables?

To keep sensitive credentials outside the source code and manage different environments securely.

### Q11. What is Idempotency?

Idempotency ensures that processing the same request multiple times does not produce duplicate financial or business operations.

### Q12. What is Payment Reconciliation?

Payment reconciliation compares the merchant's payment records with the gateway's records to identify mismatches and pending transactions.

---

# 25. Final Integration Checklist

## Development

- [ ] Create sandbox account.
- [ ] Collect test credentials.
- [ ] Read API documentation.
- [ ] Design database schema.
- [ ] Implement payment initiation.
- [ ] Implement success callback.
- [ ] Implement fail callback.
- [ ] Implement cancel callback.
- [ ] Implement IPN.
- [ ] Implement server-side verification.
- [ ] Test using Postman.
- [ ] Test all payment scenarios.

## Business Approval

- [ ] Submit business documents.
- [ ] Complete merchant verification.
- [ ] Complete UAT.
- [ ] Obtain live credentials.
- [ ] Get live payment access approved.

## Production

- [ ] Configure live credentials.
- [ ] Configure live API URLs.
- [ ] Configure production callback URLs.
- [ ] Configure IPN URL.
- [ ] Enable HTTPS.
- [ ] Verify security settings.
- [ ] Test a real transaction.
- [ ] Monitor transactions.
- [ ] Implement reconciliation and refund handling.

---

# 26. Official Documentation

SSLCommerz:
https://developer.sslcommerz.com/

aamarPay:
https://aamarpay.com/

ShurjoPay:
https://shurjopay.com.bd/

Always follow the latest official provider documentation for API parameters, callback verification, credentials, IPN requirements and production approval.

---

# 27. Final Summary

Payment Gateway Integration workflow:

1. Create Sandbox Account.
2. Collect Test Credentials.
3. Read API Documentation.
4. Design Database and Architecture.
5. Implement Payment Initiation API.
6. Integrate Gateway API.
7. Implement Success / Fail / Cancel Callbacks.
8. Implement IPN / Webhook.
9. Verify Transactions Server-side.
10. Test Using Postman.
11. Submit Business Documents.
12. Complete Merchant Verification.
13. Complete UAT.
14. Obtain Live Credentials.
15. Configure Production Environment.
16. Configure IPN in Merchant Dashboard.
17. Test Live Payment.
18. Monitor and Reconcile Transactions.

**Remember:** Payment initiation is only the beginning. The most important part of a secure payment integration is server-side transaction verification, idempotent processing and reliable order-status management.
