# AI-Powered Backend Developer + SaaS + AWS Roadmap
## Beginner to Advanced — Python, Django, AI, DevOps & Cloud Deployment

**Goal:** Build secure, scalable, production-ready AI-powered SaaS applications.

**Core Stack:**
- Python
- Django
- Django REST Framework (DRF)
- PostgreSQL
- React
- Redis
- Celery
- Docker
- AWS
- GitHub Actions
- LLM APIs
- RAG and Vector Search
- Multi-tenancy and SaaS Architecture

---

# Table of Contents

1. [Phase 0 — Developer Foundations](#phase-0--developer-foundations)
2. [Phase 1 — Python Advanced](#phase-1--python-advanced)
3. [Phase 2 — Django Backend Development](#phase-2--django-backend-development)
4. [Phase 3 — REST API and Authentication](#phase-3--rest-api-and-authentication)
5. [Phase 4 — PostgreSQL and Database Engineering](#phase-4--postgresql-and-database-engineering)
6. [Phase 5 — Testing and Code Quality](#phase-5--testing-and-code-quality)
7. [Phase 6 — React and Frontend Integration](#phase-6--react-and-frontend-integration)
8. [Phase 7 — Redis and Celery](#phase-7--redis-and-celery)
9. [Phase 8 — Production Deployment Fundamentals](#phase-8--production-deployment-fundamentals)
10. [Phase 9 — Linux, Networking and VPS Deployment](#phase-9--linux-networking-and-vps-deployment)
11. [Phase 10 — Docker and Containerization](#phase-10--docker-and-containerization)
12. [Phase 11 — CI/CD Automation](#phase-11--cicd-automation)
13. [Phase 12 — AWS Cloud Engineering](#phase-12--aws-cloud-engineering)
14. [Phase 13 — SaaS Architecture](#phase-13--saas-architecture)
15. [Phase 14 — SaaS Billing and Payments](#phase-14--saas-billing-and-payments)
16. [Phase 15 — LLM Application Development](#phase-15--llm-application-development)
17. [Phase 16 — RAG and Vector Databases](#phase-16--rag-and-vector-databases)
18. [Phase 17 — AI Agents and Tool Calling](#phase-17--ai-agents-and-tool-calling)
19. [Phase 18 — Security and Monitoring](#phase-18--security-and-monitoring)
20. [Phase 19 — Infrastructure as Code](#phase-19--infrastructure-as-code)
21. [Phase 20 — Kubernetes and Advanced Scaling](#phase-20--kubernetes-and-advanced-scaling)
22. [Final Project — AI Project Management SaaS](#final-project--ai-project-management-saas)
23. [Project Portfolio](#project-portfolio)
24. [Daily Study Routine](#daily-study-routine)
25. [Final Checklist](#final-checklist)

---

# Phase 0 — Developer Foundations

## 0.1 Computer and Web Fundamentals

Learn:

- How the internet works
- Client-server architecture
- HTTP and HTTPS
- DNS
- IP addresses and ports
- Request-response lifecycle
- JSON and XML
- REST architecture
- Cookies and sessions
- Browser developer tools

### Question: What happens when a user opens a website?

**Answer:**

1. The browser resolves the domain through DNS.
2. It establishes a network connection with the server.
3. For HTTPS, a TLS handshake establishes an encrypted connection.
4. The browser sends an HTTP request.
5. The server processes the request.
6. The server returns an HTTP response.
7. The browser renders the response.

## 0.2 Git and GitHub

Learn:

- `git init`
- `git clone`
- `git add`
- `git commit`
- `git push`
- `git pull`
- Branching and merging
- Pull requests
- `.gitignore`
- Resolving merge conflicts
- Writing meaningful commit messages

### Practice

Create a GitHub repository for each project and maintain a useful README.

## 0.3 Linux Basics

Learn:

```bash
pwd
ls -la
cd /path/to/project
mkdir my-project
touch app.py
cp source.txt destination.txt
mv old.txt new.txt
rm file.txt
cat file.txt
less file.txt
grep "ERROR" app.log
find . -name "*.py"
```

Learn file permissions and ownership:

```bash
chmod 644 file.txt
chmod 755 script.sh
chown user:group file.txt
```

**Important:** Understand a command before running it with `sudo` or against production files.

---

# Phase 1 — Python Advanced

## Topics

- Variables and data types
- Lists, tuples, sets and dictionaries
- Conditions and loops
- Functions and arguments
- `*args` and `**kwargs`
- List and dictionary comprehensions
- Modules and packages
- Exception handling
- File handling
- Object-oriented programming
- Inheritance and composition
- Decorators
- Iterators and generators
- Context managers
- Type hints
- Dataclasses
- Virtual environments
- Dependency management
- Logging
- Unit testing
- Async programming fundamentals

## Example: Type Hints and Error Handling

```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Divisor cannot be zero")

    return a / b


try:
    result = divide(10, 2)
    print(result)
except ValueError as error:
    print(error)
```

## Question: Why use a virtual environment?

**Answer:** A virtual environment isolates project dependencies, helping different projects use different package versions without interfering with one another.

## Practice Projects

1. Command-line expense tracker
2. File organizer
3. Contact management system
4. Log analyzer
5. REST API client

**Completion goal:** Write reusable, readable Python code and understand exceptions, modules, OOP and testing.

---

# Phase 2 — Django Backend Development

## Topics

- Django project structure
- Apps and settings
- URLs and views
- Function-based views
- Class-based views
- Templates
- Models and fields
- Django ORM
- QuerySets
- CRUD operations
- Forms and ModelForms
- Middleware
- Signals
- Custom user models
- Authentication and authorization
- Model relationships
- Migrations
- Static and media files
- Environment variables
- Django admin
- Service-layer organization
- Caching fundamentals

## Example: Django Model

```python
from django.conf import settings
from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Question: What is Django ORM?

**Answer:** Django ORM allows you to interact with database records using Python objects and QuerySets instead of writing SQL for every operation.

Example:

```python
Task.objects.create(
    title="Learn Django ORM",
    owner=user,
)

tasks = Task.objects.filter(
    owner=user,
    status="todo",
)
```

## Recommended Architecture

```text
project/
├── config/
├── apps/
│   ├── users/
│   ├── tasks/
│   └── projects/
├── templates/
├── static/
├── media/
├── tests/
├── manage.py
├── requirements.txt
└── .env.example
```

Keep views focused on HTTP handling. Move complex business rules into clearly named functions or service modules when that improves maintainability.

## Practice Projects

1. Blog application
2. Personal portfolio backend
3. Task management system
4. Inventory management API
5. Employee management system

---

# Phase 3 — REST API and Authentication

## Topics

- REST principles
- HTTP methods
- HTTP status codes
- JSON serialization
- Django REST Framework
- Serializers
- API views
- Generic views
- ViewSets and routers
- Filtering and searching
- Ordering
- Pagination
- Validation
- Permissions
- Throttling
- API versioning
- OpenAPI and Swagger documentation
- JWT authentication
- Session authentication
- OAuth2 concepts
- CORS and CSRF
- Refresh-token handling

## Example: DRF Serializer

```python
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
```

## Example: API ViewSet

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

## Question: Why filter by the current user?

**Answer:** Authentication identifies the caller, but it does not automatically authorize access to every database record. Filtering records by their owner helps prevent users from accessing other users' tasks.

## API Checklist

- Validate every input.
- Apply authentication where required.
- Check object-level permissions.
- Paginate large collections.
- Use appropriate HTTP status codes.
- Document request and response formats.
- Test both authorized and unauthorized access.
- Avoid returning sensitive fields.

**Security note:** For browser applications, consider the trade-offs between secure HttpOnly cookies and token-based authentication. Cookie-based authentication requires appropriate CSRF protection. Avoid storing long-lived sensitive tokens in browser storage without understanding the risks.

---

# Phase 4 — PostgreSQL and Database Engineering

## Topics

- Relational database concepts
- Tables, rows and columns
- Primary and foreign keys
- Unique constraints
- Check constraints
- One-to-one relationships
- One-to-many relationships
- Many-to-many relationships
- SQL CRUD
- Joins
- Aggregation and grouping
- Transactions
- Indexes
- Query plans
- Normalization
- Database migrations
- Connection pooling
- Database backups and restores
- Isolation levels
- Locking fundamentals

## SQL Example

```sql
SELECT id, title, status
FROM tasks
WHERE status = 'todo'
ORDER BY created_at DESC
LIMIT 20;
```

## Example: Indexing

```python
class Task(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, db_index=True)
```

An index can speed up some searches and filters, but it consumes storage and adds overhead to writes. Add indexes based on actual query patterns and measurements.

## Question: What is an N+1 query problem?

**Answer:** It occurs when an application executes one query to retrieve a collection and then additional queries for each item in that collection.

In Django, use:

```python
# For ForeignKey and OneToOne relationships
Task.objects.select_related("owner")

# For ManyToMany and reverse relationships
Project.objects.prefetch_related("members")
```

Choose the correct optimization based on the relationship and verify query counts.

## Practice

- Design a normalized database for a task application.
- Add suitable constraints and indexes.
- Inspect slow queries.
- Use `EXPLAIN ANALYZE` carefully to understand query plans.
- Test database backup and restore procedures.

---

# Phase 5 — Testing and Code Quality

## Topics

- Unit testing
- Integration testing
- API testing
- Django `TestCase`
- DRF `APITestCase`
- Pytest
- Fixtures and factories
- Mocking external services
- Regression testing
- Test coverage
- Code formatting
- Linting
- Type checking

## Example: API Test

```python
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="developer",
            password="test-password-123",
        )

    def test_tasks_require_authentication(self):
        response = self.client.get("/api/tasks/")

        self.assertIn(response.status_code, [401, 403])
```

Adapt the endpoint and expected authentication status to your project's configuration.

## Question: Why write tests before deployment?

**Answer:** Tests catch regressions and help verify that important behavior remains correct after code changes. They are especially useful for permissions, billing, authentication and multi-tenant data isolation.

**Rule:** Add tests throughout development rather than waiting until the project is complete.

---

# Phase 6 — React and Frontend Integration

For a backend-focused career, learn enough frontend development to build and integrate a working application.

## Topics

- HTML and semantic markup
- CSS and responsive design
- JavaScript fundamentals
- ES modules
- Promises and `async`/`await`
- React components
- Props and state
- Hooks
- Forms and validation
- Routing
- API requests
- Loading and error states
- Authentication flows
- Environment variables
- Build tools

## Example: API Request

```javascript
async function fetchTasks() {
  const response = await fetch("/api/tasks/", {
    credentials: "include",
  });

  if (!response.ok) {
    throw new Error("Could not fetch tasks");
  }

  return response.json();
}
```

This example assumes a cookie-based authentication setup. If your API uses bearer tokens, implement the appropriate authorization header and token lifecycle instead.

## Practice Project

Build a React dashboard that supports:

- Login and logout
- Task listing
- Task creation and editing
- Filtering and pagination
- Loading and error states
- Responsive layout

---

# Phase 7 — Redis and Celery

## Redis

Learn:

- Key-value storage
- Expiration and TTL
- Caching
- Cache invalidation
- Rate-limiting concepts
- Redis data structures
- Redis authentication and network security

## Celery

Learn:

- Tasks
- Workers
- Brokers
- Retries
- Scheduling with Celery Beat
- Task time limits
- Idempotent task design
- Task monitoring
- Failure handling
- Optional result backends

## Architecture

```text
Django Application
       |
       | Enqueue task
       v
Redis Broker
       |
       v
Celery Worker
       |
       +---- Send email
       +---- Generate report
       +---- Process uploaded file
       +---- Call external API
```

## Example: Celery Task

```python
from celery import shared_task


@shared_task(
    autoretry_for=(ConnectionError,),
    retry_backoff=True,
    max_retries=3,
)
def generate_report(report_id: int):
    # Load the report and perform the required work.
    # Ensure retries do not create duplicate side effects.
    return {"report_id": report_id, "status": "processed"}
```

This is a simplified example. A real task should fetch the report, generate the file, store it, and record success or failure.

## Question: Why use Celery?

**Answer:** Celery moves long-running or scheduled work outside the normal web request-response cycle. The API can respond quickly while workers process background jobs.

## Practice Projects

1. Background email delivery
2. Scheduled report generation
3. CSV import processing
4. Retryable external API integration

**Important:** `depends_on` in Docker Compose does not always mean a service is ready to accept connections. Configure health checks, connection retries and sensible timeouts.

---

# Phase 8 — Production Deployment Fundamentals

## Topics

- Development versus production settings
- Environment variables
- Secret management
- `DEBUG=False`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- Static file collection
- Media storage
- WSGI and ASGI
- Gunicorn
- Uvicorn where appropriate
- Nginx
- PostgreSQL production configuration
- Logging
- Error reporting
- HTTPS
- Database migrations
- Backups and restore testing

## Production Checklist

```python
DEBUG = False
```

Configure hosts explicitly:

```python
ALLOWED_HOSTS = [
    "example.com",
    "www.example.com",
]
```

Configure trusted HTTPS origins where needed:

```python
CSRF_TRUSTED_ORIGINS = [
    "https://example.com",
    "https://www.example.com",
]
```

These are examples; replace the domains with your actual production domains.

## Django Deployment Check

```bash
python manage.py check --deploy
python manage.py collectstatic --noinput
python manage.py migrate
```

Run migrations as a controlled deployment step. Back up important data first and verify migrations in a staging environment when possible.

## Question: Why is `DEBUG=False` important?

**Answer:** Debug mode can expose internal application details, settings and debugging information. Production applications should disable it and use proper logging and error reporting.

---

# Phase 9 — Linux, Networking and VPS Deployment

## Linux Administration

Learn:

- Users and groups
- Permissions
- SSH
- Processes
- Services with systemd
- Disk and memory inspection
- Environment variables
- Firewall rules
- Log files
- Cron jobs
- Package management

Useful commands:

```bash
whoami
ps aux
top
df -h
free -h
systemctl status nginx
journalctl -u nginx
ss -tulpn
```

## Networking

Learn:

- DNS records: A, AAAA, CNAME and MX
- Ports and firewalls
- TCP/IP fundamentals
- TLS certificates
- Reverse proxies
- HTTP headers
- Domain configuration

## Deployment Architecture

```text
Browser
   |
 HTTPS
   |
Nginx
   |
Gunicorn / Django
   |
PostgreSQL
```

Redis and Celery can be added for caching and background processing.

## Deployment Steps

1. Provision a Linux server.
2. Configure a non-root deployment user.
3. Set up SSH access securely.
4. Configure the firewall.
5. Install Python and required system packages.
6. Deploy application code.
7. Create a virtual environment.
8. Install dependencies.
9. Configure production environment variables.
10. Configure PostgreSQL securely.
11. Run migrations.
12. Collect static files.
13. Configure Gunicorn.
14. Configure Nginx as a reverse proxy.
15. Configure DNS and HTTPS.
16. Configure systemd services.
17. Test logs, error handling and restart behavior.
18. Configure backups and recovery procedures.

**Security rule:** Do not expose PostgreSQL or Redis publicly unless a specific, properly secured architecture requires it.

---

# Phase 10 — Docker and Containerization

## Topics

- Images and containers
- Dockerfile
- Docker Compose
- Volumes
- Networks
- Environment variables
- Build cache
- Multi-stage builds
- Non-root containers
- Health checks
- Image tagging
- Container logs
- Container registries

## Example Dockerfile

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Replace `config.wsgi:application` if your Django project uses a different package name. Add production-specific static file handling and dependency installation as required.

## Example Docker Compose

```yaml
services:
  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: app_db
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app_user -d app_db"]
      interval: 5s
      timeout: 5s
      retries: 10

volumes:
  postgres_data:
```

Use a real secret for `POSTGRES_PASSWORD`; never commit `.env` to Git. For production, configure restricted networking, backups, migrations and health checks. A database container's persistent volume is not a substitute for backups.

## Practice

- Containerize a Django API.
- Add PostgreSQL.
- Add Redis and a Celery worker.
- Run the full stack using Compose.
- Test restart and recovery behavior.

---

# Phase 11 — CI/CD Automation

## Topics

- Continuous integration
- Continuous delivery and deployment
- GitHub Actions
- Automated tests
- Linting and formatting
- Build artifacts
- Container image builds
- Image registries
- Deployment workflows
- Environment-specific configuration
- Rollback strategies
- Deployment approvals

## Example Workflow

```yaml
name: Django CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: python manage.py test
```

This starter workflow assumes the tests can run with the configured settings and dependencies. Add a PostgreSQL service and required environment variables when your test suite needs a database.

## Question: What does CI/CD mean?

**Answer:**

- **Continuous Integration (CI):** Automatically validates code changes through tests and checks.
- **Continuous Delivery:** Keeps validated changes ready for release.
- **Continuous Deployment:** Automatically deploys qualifying changes to an environment.

Start with automated tests. Add deployment automation after you understand your manual release and rollback procedures.

---

# Phase 12 — AWS Cloud Engineering

## Core AWS Services

### Identity and Security

- IAM users, roles and policies
- Least-privilege permissions
- Security groups
- Secrets Manager
- Systems Manager Parameter Store
- CloudTrail

### Compute

- EC2
- Auto Scaling concepts
- Elastic Load Balancing
- ECS
- ECR
- Lambda fundamentals

### Storage and Databases

- S3
- RDS for PostgreSQL
- EBS
- Backup and recovery concepts

### Networking

- VPC
- Public and private subnets
- Route tables
- Internet Gateway
- NAT Gateway concepts
- DNS with Route 53
- HTTPS with AWS Certificate Manager

### Monitoring

- CloudWatch metrics
- CloudWatch logs
- Alarms
- CloudTrail auditing

## Recommended Learning Order

1. Create an AWS account and enable cost alerts.
2. Learn IAM and least-privilege access.
3. Understand regions, availability zones and VPCs.
4. Deploy a small application on EC2.
5. Configure security groups.
6. Configure a domain and HTTPS.
7. Learn S3 for file storage.
8. Learn RDS for managed PostgreSQL.
9. Configure backups and monitoring.
10. Learn ECR and ECS for container deployment.
11. Add load balancing and scaling.
12. Explore Secrets Manager and ElastiCache.
13. Learn SQS when asynchronous messaging is needed.

## Example AWS Architecture

```text
Users
  |
Route 53
  |
HTTPS / Load Balancer
  |
ECS Application Service
  |
  +------ RDS PostgreSQL
  |
  +------ S3
  |
  +------ ElastiCache Redis
  |
  +------ SQS --> Worker Service
```

This is one possible architecture, not a mandatory starting point. For a small project, EC2 or a simpler managed container setup may be sufficient.

## Cost and Security Checklist

- Enable billing alerts.
- Use least-privilege IAM policies.
- Do not publish database credentials.
- Keep databases in private subnets where appropriate.
- Restrict inbound traffic.
- Encrypt sensitive data.
- Configure backups and test restoration.
- Monitor resource utilization.
- Delete unused resources.
- Review costs after experiments.

---

# Phase 13 — SaaS Architecture

## What Is SaaS?

Software as a Service (SaaS) is a software delivery model in which customers use an application hosted and maintained by the provider, often through a subscription.

Examples of SaaS capabilities include:

- Organizations and teams
- Invitations and membership
- Role-based access control
- Subscription plans
- Usage limits
- Billing history
- Audit logs
- Tenant-specific data
- Admin dashboards

## Multi-Tenancy

Multi-tenancy means a single application serves multiple customers while enforcing separation between their data and permissions.

### Important Concepts

- Tenant or organization model
- Membership model
- Current organization selection
- Role-based permissions
- Tenant-scoped querysets
- Tenant-aware background jobs
- Tenant-scoped file access
- Tenant-specific audit logs
- Isolation tests

## Example Data Model

```text
User
 |
 +---- OrganizationMembership ---- Organization
                |
                +---- role
                +---- joined_at

Organization
 |
 +---- Projects
 +---- Tasks
 +---- Subscriptions
 +---- Audit Logs
```

A user may belong to multiple organizations. Therefore, do not assume that every user has exactly one organization.

## Example Membership Model

```python
from django.conf import settings
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=200)


class OrganizationMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization_memberships",
    )
    role = models.CharField(max_length=20, choices=Role.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "user"],
                name="unique_organization_membership",
            )
        ]
```

## Question: How do you prevent tenant data leakage?

**Answer:**

1. Resolve the current organization from a trusted, validated membership.
2. Scope database queries to that organization.
3. Check permissions on every relevant operation.
4. Scope file downloads and background jobs.
5. Test that users from one tenant cannot access another tenant's records.
6. Enforce important invariants in the database where possible.

Never rely only on a tenant ID supplied by the frontend.

---

# Phase 14 — SaaS Billing and Payments

## Topics

- Subscription lifecycle
- Free and paid plans
- Monthly and yearly billing
- Trial periods
- Usage limits
- Payment providers
- Checkout sessions
- Webhooks
- Failed payments
- Cancellation
- Refunds
- Billing history
- Invoice records
- Idempotency
- Entitlement checks

## Typical Payment Flow

```text
Customer
   |
   v
Backend creates checkout session
   |
   v
Payment provider checkout
   |
   v
Provider sends signed webhook
   |
   v
Backend verifies signature
   |
   v
Backend processes event safely
   |
   v
Subscription and entitlements updated
```

## Security Rules

- Verify webhook signatures.
- Treat webhook delivery as repeatable.
- Store processed event IDs or use equivalent idempotency controls.
- Use database transactions for related updates.
- Never trust a frontend success redirect as proof of payment.
- Never store raw payment-card data unless you meet the applicable compliance requirements.
- Keep subscription status synchronized with provider events.
- Enforce plan limits on the backend.

## Example Entitlement Check

```python
def can_create_project(subscription, current_project_count):
    if not subscription.is_active:
        return False

    return current_project_count < subscription.plan.project_limit
```

This is illustrative. A real implementation must define how trials, grace periods, cancellation and plan changes affect access.

---

# Phase 15 — LLM Application Development

## Topics

- Large Language Models
- Prompt design
- System and user messages
- LLM APIs
- Token usage
- Context windows
- Temperature and output controls
- Structured output
- JSON validation
- Streaming responses
- Rate limits
- Retries and timeouts
- Cost monitoring
- Error handling
- Privacy and retention
- Model evaluation

## Example Use Cases

- AI task summaries
- Meeting summaries
- Email drafting
- Report generation
- Natural-language search
- Project risk summaries
- Support assistants

## Example Backend Flow

```text
React Frontend
      |
      v
Django API
      |
      +---- Authenticate user
      |
      +---- Check permissions and usage limits
      |
      +---- Validate request
      |
      v
LLM Provider API
      |
      v
Validate output
      |
      v
Return result to frontend
```

## Question: Why call the LLM through the backend?

**Answer:** Keeping provider credentials on the backend protects API keys and lets you enforce authentication, permissions, rate limits, logging and usage quotas.

## Best Practices

- Store API keys in secret management systems.
- Set timeouts and sensible retry policies.
- Validate structured output.
- Limit input and output size.
- Track usage and cost.
- Avoid sending unnecessary personal or confidential data.
- Do not assume model-generated answers are always correct.
- Test failure cases, not just successful responses.

---

# Phase 16 — RAG and Vector Databases

## What Is RAG?

Retrieval-Augmented Generation (RAG) retrieves relevant information from a knowledge source and supplies that information to an LLM to help it answer a question.

## RAG Pipeline

```text
Documents
   |
   v
Text Extraction
   |
   v
Chunking
   |
   v
Embedding Model
   |
   v
Vector Database
   |
   v
User Question
   |
   v
Question Embedding
   |
   v
Retrieve Relevant Chunks
   |
   v
Build Context
   |
   v
LLM Response
```

## Topics

- Embeddings
- Chunking strategies
- Vector similarity
- Metadata filtering
- PostgreSQL with pgvector
- Semantic search
- Hybrid search
- Retrieval evaluation
- Prompt injection risks
- Document permissions
- Tenant isolation
- Citation and source tracking

## Why Use pgvector?

`pgvector` adds vector storage and similarity-search capabilities to PostgreSQL, allowing many applications to keep relational records and embeddings in the same database platform.

## Multi-Tenant RAG Security

- Associate documents with an organization or owner.
- Apply access filters during retrieval.
- Enforce authorization before returning retrieved content.
- Do not rely on the LLM to enforce permissions.
- Test cross-tenant retrieval attempts.
- Treat retrieved documents as untrusted input.
- Keep citations or source metadata so users can inspect supporting documents.

## Practice Project

Build a document question-answering API that:

1. Accepts authorized document uploads.
2. Extracts text.
3. Splits text into chunks.
4. Creates embeddings.
5. Stores chunks and vectors.
6. Retrieves relevant content.
7. Generates an answer grounded in the retrieved content.
8. Returns source references.
9. Enforces user and tenant permissions.

---

# Phase 17 — AI Agents and Tool Calling

## What Is an AI Agent?

An AI agent is a system that uses a model to decide among permitted actions, invokes tools, observes their results and continues toward a defined goal.

## Topics

- Function and tool calling
- Structured arguments
- Tool validation
- State management
- Workflow orchestration
- Human approval
- Retries and timeouts
- Agent evaluation
- Audit logs
- Cost and iteration limits

## Example Architecture

```text
User Request
     |
     v
Django API
     |
     v
LLM Chooses a Permitted Tool
     |
     v
Backend Validates Arguments
     |
     v
Permission Check
     |
     v
Tool Executes
     |
     v
Tool Result Returned to LLM
     |
     v
Final Response
```

## Example Tools

- `search_tasks`
- `create_task`
- `summarize_project`
- `generate_report`
- `search_documents`

## Security Rules

- Give the agent only the tools it needs.
- Validate every tool argument.
- Apply user and tenant permissions to every action.
- Require approval for destructive or high-impact operations.
- Use allowlists and bounded execution.
- Never expose unrestricted shell or SQL access to an LLM.
- Protect against prompt injection from user input and retrieved documents.
- Log tool calls without unnecessarily storing sensitive data.

**Important:** Start with deterministic workflows and a small set of tools before building complex autonomous agents.

---

# Phase 18 — Security and Monitoring

## Application Security

- Input validation
- Authentication and authorization
- Object-level permissions
- SQL injection prevention
- Cross-site scripting awareness
- CSRF protection
- CORS configuration
- Secure cookies
- Password security
- Rate limiting
- File upload validation
- Secret management
- Dependency updates
- Audit logging
- Least privilege

## Production Monitoring

Learn:

- Structured logging
- Error tracking
- Health checks
- Metrics
- Response latency
- Error rates
- Database performance
- Queue depth
- Celery task failures
- Resource utilization
- Alerting

## Backup and Recovery

- Schedule database backups.
- Define retention policies.
- Encrypt backup files.
- Restrict backup access.
- Store copies separately from the primary system.
- Test restoring backups.
- Document recovery steps.

## Question: Is having a backup enough?

**Answer:** No. A backup is useful only if it can be restored successfully within an acceptable recovery time. Regular restoration tests are essential.

---

# Phase 19 — Infrastructure as Code

## Terraform

Learn:

- Providers
- Resources
- Variables
- Outputs
- Modules
- State files
- Remote state
- Plans and applies
- Resource dependencies
- Secrets handling
- Environment separation

## Example Workflow

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Review the plan before applying changes. Protect Terraform state because it may contain sensitive infrastructure information.

## Practice

Use Terraform to provision a small, appropriately secured environment and document how to recreate and destroy it safely.

---

# Phase 20 — Kubernetes and Advanced Scaling

Learn Kubernetes after you understand Docker, networking, deployment and monitoring.

## Topics

- Pods
- Deployments
- Services
- Ingress
- ConfigMaps
- Secrets
- Namespaces
- Health probes
- Resource requests and limits
- Autoscaling
- Persistent storage
- Rolling deployments
- Observability
- Cluster security

## Important Principle

Kubernetes is not required for every SaaS application. A VM, managed container service or simpler deployment platform may be more economical and easier to maintain for a small application.

Learn it when orchestration, scaling or operational requirements justify the additional complexity.

---

# Final Project — AI Project Management SaaS

## Project Goal

Build a production-oriented SaaS application that lets organizations manage projects and tasks while using AI to summarize progress, search documents and assist with project workflows.

## Core Features

### 1. User Management

- Registration
- Login and logout
- Password reset
- User profile
- Session or token lifecycle

### 2. Organizations and Teams

- Organization creation
- Team invitations
- Membership management
- Roles and permissions
- Organization switching
- Tenant-scoped data

### 3. Project Management

- Create and update projects
- Assign team members
- Create and assign tasks
- Task statuses and priorities
- Comments
- Due dates
- Activity history

### 4. SaaS Billing

- Subscription plans
- Trial support
- Usage limits
- Checkout integration
- Webhook processing
- Billing history
- Subscription cancellation

### 5. AI Features

- Summarize project progress
- Draft task descriptions
- Generate project reports
- Answer questions about authorized documents
- Search documents using RAG
- Suggest next actions
- Provide controlled tool calling

### 6. Background Processing

- Email notifications
- Report generation
- Document processing
- Embedding generation
- Scheduled jobs
- Retryable tasks

### 7. Production Readiness

- Automated tests
- Docker
- CI/CD
- HTTPS
- Production database
- Object storage
- Logging and monitoring
- Backups and restoration
- Security review
- Cost controls

## Suggested Architecture

```text
                    Users
                      |
                      v
                React Frontend
                      |
                      v
                 HTTPS / API
                      |
                      v
                Django + DRF
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
      PostgreSQL    Redis      LLM API
          |           |
          |           v
          |      Celery Workers
          |           |
          v           v
       pgvector     S3 Storage
          |
          v
     RAG Retrieval
```

The diagram is conceptual. In production, configure network boundaries, credentials, tenant isolation, retries, monitoring and storage access explicitly.

## Suggested Repository Structure

```text
ai-project-management-saas/
├── backend/
│   ├── config/
│   ├── apps/
│   │   ├── users/
│   │   ├── organizations/
│   │   ├── projects/
│   │   ├── tasks/
│   │   ├── billing/
│   │   ├── documents/
│   │   └── ai/
│   ├── tests/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
├── infrastructure/
│   ├── docker/
│   └── terraform/
├── .github/
│   └── workflows/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# Project Portfolio

Build projects in increasing order of complexity.

## Project 1 — Task Management API

**Stack:** Python, Django, DRF, PostgreSQL

Features:

- CRUD endpoints
- Authentication
- Permissions
- Pagination
- Filtering
- API documentation
- Automated tests

## Project 2 — Background Job Platform

**Stack:** Django, Redis, Celery, PostgreSQL

Features:

- Scheduled jobs
- Email delivery
- Report generation
- Retry logic
- Task status tracking
- Worker monitoring

## Project 3 — Production-Ready Django App

**Stack:** Django, PostgreSQL, Nginx, Gunicorn, Linux

Features:

- Domain and HTTPS
- Production settings
- Static files
- Logging
- Backups
- Deployment documentation

## Project 4 — Dockerized Full-Stack Application

**Stack:** Django, React, PostgreSQL, Redis, Docker Compose

Features:

- Multi-service local development
- Containerized deployment
- Persistent database storage
- Health checks
- Environment configuration

## Project 5 — AWS Deployment

**Stack:** AWS, Docker, PostgreSQL, S3, CloudWatch

Features:

- Cloud deployment
- Secure networking
- Database backups
- File storage
- Monitoring
- Cost controls

## Project 6 — Multi-Tenant SaaS

**Stack:** Django, DRF, PostgreSQL, React

Features:

- Organizations
- Membership and roles
- Tenant isolation
- Subscription plans
- Usage limits
- Audit logs

## Project 7 — AI Document Assistant

**Stack:** Django, LLM API, PostgreSQL, pgvector

Features:

- Document ingestion
- Embeddings
- Retrieval
- Source references
- Tenant-scoped search
- Evaluation tests

## Project 8 — AI Project Management SaaS

Combine the earlier projects into a single portfolio-quality application with billing, AI features, background jobs, deployment automation and monitoring.

---

# Daily Study Routine

A practical routine for approximately 2–4 hours per day:

| Activity | Time |
|---|---:|
| Learn a concept | 30 minutes |
| Write code | 60 minutes |
| Build a project feature | 45 minutes |
| Testing and debugging | 30 minutes |
| Notes and GitHub updates | 15 minutes |

Adjust the schedule based on your current level and available time.

## Weekly Workflow

- **Day 1:** Learn the topic and write short notes.
- **Day 2:** Follow a small practical example.
- **Day 3:** Build a feature without copying the tutorial.
- **Day 4:** Write tests and handle edge cases.
- **Day 5:** Review security and performance.
- **Day 6:** Refactor and document the project.
- **Day 7:** Review progress and revise weak topics.

---

# Suggested Learning Timeline

The complete roadmap is substantial. Treat the timeline as a flexible guide rather than a guarantee.

| Stage | Approximate duration |
|---|---|
| Python and developer foundations | 3–6 weeks |
| Django and REST APIs | 4–8 weeks |
| PostgreSQL and testing | 3–5 weeks |
| React integration | 2–5 weeks |
| Redis, Celery and background jobs | 2–4 weeks |
| Linux and manual deployment | 2–4 weeks |
| Docker and CI/CD | 2–5 weeks |
| AWS fundamentals | 3–6 weeks |
| SaaS architecture and billing | 3–6 weeks |
| LLMs, RAG and AI tools | 4–8 weeks |
| Final project hardening | 4–8 weeks |

These stages overlap. Depending on your existing knowledge and daily study time, the full roadmap may take **6–12 months or longer**.

---

# Final Checklist

## Backend

- [ ] Strong Python fundamentals
- [ ] Django models, ORM and migrations
- [ ] DRF serializers, views and permissions
- [ ] Authentication and authorization
- [ ] PostgreSQL schema design and query optimization
- [ ] Automated API tests
- [ ] Logging and error handling

## Frontend

- [ ] HTML, CSS and JavaScript fundamentals
- [ ] React components and state
- [ ] API integration
- [ ] Forms and error states
- [ ] Authentication integration

## Background Processing

- [ ] Redis caching
- [ ] Celery workers
- [ ] Retries and timeouts
- [ ] Scheduled tasks
- [ ] Idempotent task design

## Deployment

- [ ] Linux and SSH
- [ ] DNS and HTTPS
- [ ] Nginx and Gunicorn
- [ ] Docker and Compose
- [ ] CI/CD
- [ ] Production settings
- [ ] Database backup and restore
- [ ] Monitoring and alerts

## AWS

- [ ] IAM and least privilege
- [ ] VPC and security groups
- [ ] EC2
- [ ] S3
- [ ] RDS
- [ ] CloudWatch
- [ ] Container deployment
- [ ] Cost monitoring

## SaaS

- [ ] Organizations and memberships
- [ ] Tenant isolation
- [ ] Roles and permissions
- [ ] Subscription lifecycle
- [ ] Payment webhooks
- [ ] Usage limits
- [ ] Audit logs

## AI

- [ ] LLM API integration
- [ ] Structured output validation
- [ ] Cost and rate limits
- [ ] Embeddings
- [ ] RAG with pgvector
- [ ] Retrieval evaluation
- [ ] Secure tool calling
- [ ] Prompt-injection defenses
- [ ] Tenant-aware AI access controls

---

# Final Advice

1. **Build first, then scale.** Start with a working Django API before introducing complex infrastructure.
2. **Learn deployment by doing it.** Deploy one application manually before automating the process.
3. **Test permissions early.** Authentication without proper authorization is not sufficient.
4. **Learn Docker before Kubernetes.** Kubernetes is an advanced tool, not a requirement for every project.
5. **Treat payments and AI as security-sensitive features.** Validate inputs, permissions, webhooks and outputs.
6. **Document your projects.** Include setup instructions, API documentation, architecture diagrams and screenshots where useful.
7. **Build a project portfolio.** A deployed application with tests and a clear README demonstrates practical ability better than a list of technologies.

**Recommended priority:** Python → Django → DRF → PostgreSQL → Testing → Redis/Celery → Linux and deployment → Docker → CI/CD → AWS → SaaS architecture → LLMs → RAG → AI agents → advanced infrastructure.
