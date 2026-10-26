# System Design — Complete Notes (বাংলায়)

**Level:** Beginner to Intermediate  
**Focus:** Backend Development, HLD, LLD এবং Software Engineer Interview  
**Example Stack:** Python, Django REST Framework, PostgreSQL, Redis

## Table of Contents

1. [System Design Fundamentals](#1-system-design-fundamentals)
2. [Architecture Types](#2-architecture-types)
3. [High-Level Design (HLD)](#3-high-level-design-hld)
4. [API Design](#4-api-design)
5. [Scalability and Performance](#5-scalability-and-performance)
6. [Caching and CDN](#6-caching-and-cdn)
7. [Database Design](#7-database-design)
8. [Distributed Systems](#8-distributed-systems)
9. [Security and Reliability](#9-security-and-reliability)
10. [Low-Level Design (LLD)](#10-low-level-design-lld)
11. [OOP and SOLID Principles](#11-oop-and-solid-principles)
12. [Design Patterns](#12-design-patterns)
13. [Observability](#13-observability)
14. [System Design Interview Framework](#14-system-design-interview-framework)
15. [Practical System Design Problems](#15-practical-system-design-problems)
16. [Study Roadmap](#16-study-roadmap)
17. [Interview Revision Questions](#17-interview-revision-questions)

---

# 1. System Design Fundamentals

## 1.1 What Is System Design?

System Design হলো software system-এর architecture, components, database, communication, data flow, scalability, security এবং reliability পরিকল্পনা করার প্রক্রিয়া।

### Example: E-commerce System

একটি e-commerce application-এ থাকতে পারে:

- User Authentication
- Product Catalog
- Shopping Cart
- Order Management
- Payment Processing
- Inventory Management
- Notification System
- Database and Cache

System Design নির্ধারণ করে এই component-গুলো কীভাবে একসঙ্গে কাজ করবে।

## 1.2 Why Is System Design Important?

- Scalability বাড়াতে।
- Application performance উন্নত করতে।
- Database load কমাতে।
- System failure সামলাতে।
- Security নিশ্চিত করতে।
- Code maintainability বাড়াতে।
- বড় traffic handle করতে।
- ভবিষ্যতে নতুন feature যোগ করা সহজ করতে।

## 1.3 Types of System Design

| Type | Description | Example |
|---|---|---|
| HLD | High-level architecture | YouTube architecture |
| LLD | Class ও component design | Parking Lot classes |
| Database Design | Data model ও relationships | User ও Order tables |
| API Design | API contract ও endpoints | REST API |
| Infrastructure Design | Deployment ও networking | Load balancer, containers |

System Design-এর প্রধান দুইটি category হলো HLD এবং LLD।

## 1.4 Functional Requirements

Functional Requirements বোঝায় system কী কী কাজ করবে।

Example — Chat Application:

- User message পাঠাতে পারবে।
- User message receive করতে পারবে।
- Message history দেখতে পারবে।
- Online status দেখতে পারবে।

## 1.5 Non-Functional Requirements

Non-Functional Requirements বোঝায় system কত ভালোভাবে কাজ করবে।

| Requirement | Meaning |
|---|---|
| Scalability | Workload বাড়লে system সামলাতে পারবে |
| Availability | Service ব্যবহারযোগ্য থাকবে |
| Reliability | নির্ভরযোগ্যভাবে কাজ করবে |
| Performance | দ্রুত response দেবে |
| Security | Unauthorized access প্রতিরোধ করবে |
| Maintainability | Code পরিবর্তন করা সহজ হবে |
| Durability | Committed data সংরক্ষিত থাকবে |

## 1.6 Client-Server Architecture

```text
Client
  |
  | HTTP Request
  v
Application Server
  |
  v
Database
  |
  v
Application Server
  |
  | HTTP Response
  v
Client
```

### Components

- **Client:** Browser, mobile app বা frontend।
- **Server:** Request process করে।
- **Database:** Data store করে।
- **Response:** Server-এর ফেরত পাঠানো result।

### Django Request Flow

```text
Client
  -> URL Router
  -> Middleware
  -> View / API View
  -> Business Logic
  -> Django ORM
  -> Database
  -> JSON Response
```

---

# 2. Architecture Types

## 2.1 Monolithic Architecture

একটি application-এর মধ্যে একাধিক business module থাকে এবং সাধারণত একসঙ্গে deploy করা হয়।

### Advantages

- সহজ development।
- সহজ deployment।
- শুরুতে কম operational complexity।
- Local function call-এর মাধ্যমে component communication।

### Disadvantages

- বড় codebase maintain করা কঠিন হতে পারে।
- পুরো application deploy করতে হতে পারে।
- আলাদা module স্বাধীনভাবে scale করা কঠিন হতে পারে।

### Example

একটি Django project-এ:

```text
E-commerce Application
├── users
├── products
├── cart
├── orders
└── payments
```

## 2.2 Microservices Architecture

Application-কে একাধিক independent service-এ ভাগ করা হয়।

```text
API Gateway
    |
    ├── User Service
    ├── Product Service
    ├── Order Service
    ├── Payment Service
    └── Notification Service
```

### Advantages

- Service অনুযায়ী scaling।
- Independent deployment সম্ভব।
- Service-specific technology ব্যবহার করা যায়।
- Failure isolation করা সম্ভব।

### Disadvantages

- Network communication complexity।
- Distributed data consistency।
- Monitoring ও debugging কঠিন।
- Deployment ও infrastructure পরিচালনা জটিল।

**Important:** ছোট application-এর জন্য modular monolith অনেক সময় microservices-এর চেয়ে ভালো starting point।

## 2.3 Layered Architecture

```text
Presentation Layer
        |
        v
Application / Business Layer
        |
        v
Data Access Layer
        |
        v
Database
```

### Layers

1. Presentation Layer — UI ও API interface।
2. Business Layer — Business rules।
3. Data Access Layer — Database operations।
4. Database Layer — Data storage।

## 2.4 Event-Driven Architecture

একটি event ঘটলে অন্য component সেই event process করে।

```text
Order Service
     |
     v
Message Broker
     |
     ├── Email Worker
     ├── Inventory Worker
     └── Analytics Worker
```

Example: `OrderCreated` event-এর পরে email notification পাঠানো।

## 2.5 Serverless Architecture

Cloud provider-managed functions বা services ব্যবহার করে application-এর কিছু অংশ চালানো হয়।

Example:

- AWS Lambda
- Azure Functions
- Google Cloud Functions

Serverless মানে server নেই নয়; server management-এর বড় অংশ provider পরিচালনা করে।

---

# 3. High-Level Design (HLD)

HLD-তে পুরো system-এর major components, responsibilities, communication এবং data flow নির্ধারণ করা হয়।

## 3.1 Three-Tier Architecture

```text
Presentation Tier
        |
        v
Application Tier
        |
        v
Data Tier
```

- Presentation: React, HTML বা mobile UI।
- Application: Django বা FastAPI।
- Data: PostgreSQL, Redis বা object storage।

## 3.2 API Gateway

API Gateway client request গ্রহণ করে এবং উপযুক্ত backend service-এ পাঠায়।

### Responsibilities

- Request routing
- Authentication integration
- Rate limiting
- Request logging
- API version routing

API Gateway নিজেও bottleneck বা single point of failure হতে পারে; তাই production design-এ redundancy ও scaling বিবেচনা করতে হয়।

## 3.3 Load Balancer

Load balancer incoming requests একাধিক server-এর মধ্যে distribute করে।

```text
              Client
                |
                v
          Load Balancer
          /     |     \
         v      v      v
      Server1 Server2 Server3
```

### Algorithms

- Round Robin
- Weighted Round Robin
- Least Connections
- IP Hash

### Benefits

- Traffic distribution
- Healthy server-এ routing
- Overload কমানো
- Availability বাড়াতে সাহায্য করা

## 3.4 Reverse Proxy

Reverse proxy client এবং backend server-এর মাঝখানে কাজ করে।

Common uses:

- TLS termination
- Request routing
- Compression
- Static file serving
- Load balancing

Examples: Nginx, HAProxy।

## 3.5 API Versioning

API versioning backward compatibility বজায় রাখতে সাহায্য করে।

Example:

```text
/api/v1/products/
/api/v2/products/
```

Versioning-এর পাশাপাশি deprecation policy ও migration plan থাকা উচিত।

---

# 4. API Design

## 4.1 REST API

REST API resource-oriented HTTP interface ব্যবহার করে।

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/products/` | List products |
| GET | `/api/products/10/` | Retrieve product |
| POST | `/api/products/` | Create product |
| PUT | `/api/products/10/` | Replace product |
| PATCH | `/api/products/10/` | Partially update product |
| DELETE | `/api/products/10/` | Delete product |

## 4.2 HTTP Status Codes

| Code | Meaning |
|---|---|
| 200 | OK |
| 201 | Created |
| 204 | Successful, no response body |
| 400 | Bad Request |
| 401 | Unauthenticated |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

## 4.3 Pagination

অনেক data একবারে পাঠানোর বদলে ছোট অংশে পাঠানো হয়।

Example:

```http
GET /api/products/?page=2&page_size=20
```

Offset pagination সহজ, কিন্তু বড় dataset-এ cursor pagination বেশি কার্যকর হতে পারে।

## 4.4 API Security

- Input validation।
- Authentication।
- Authorization।
- Rate limiting।
- HTTPS।
- Consistent error handling।
- Sensitive data filtering।
- Request size limits।

## 4.5 Idempotent HTTP Operations

একই request পুনরায় পাঠালে server-এর state-এর ওপর একই effect হওয়াকে idempotency বলা হয়।

GET, PUT এবং DELETE-এর intended semantics সাধারণত idempotent। POST সাধারণত idempotent নয়, তবে idempotency key ব্যবহার করে নির্দিষ্ট POST operation-কে safely retry করা যায়।

---

# 5. Scalability and Performance

## 5.1 Scalability

Scalability হলো workload বাড়লে system-এর capacity ও performance বজায় রাখার ক্ষমতা।

### Vertical Scaling

একটি server-এর CPU, RAM বা storage বাড়ানো।

Advantages:

- সহজ implementation।
- কম distributed coordination।

Disadvantages:

- Hardware limit।
- Single-server dependency থাকতে পারে।

### Horizontal Scaling

একাধিক server বা instance যোগ করা।

```text
              Load Balancer
              /     |     \
             v      v      v
          Server1 Server2 Server3
```

Advantages:

- Capacity বাড়ানো যায়।
- Redundancy সম্ভব।
- Traffic distribute করা যায়।

Challenges:

- Shared state।
- Database bottleneck।
- Session management।
- Distributed coordination।

## 5.2 Stateless Application

Stateless application প্রতিটি request process করার জন্য local server session-এর ওপর নির্ভর করে না।

Benefits:

- সহজ horizontal scaling।
- যেকোনো healthy instance-এ request পাঠানো যায়।
- Instance replacement সহজ হয়।

Session বা shared state প্রয়োজন হলে external session store বা অন্য shared storage ব্যবহার করা যেতে পারে।

## 5.3 Latency vs Throughput

- **Latency:** একটি request সম্পন্ন হতে কত সময় লাগে।
- **Throughput:** নির্দিষ্ট সময়ে কত request process হয়।

Example:

- API latency: 100 ms।
- Throughput: 1,000 requests/second।

দুটি আলাদা metric। একটি system-এর throughput বাড়লেও latency খারাপ হতে পারে।

## 5.4 Capacity Estimation

ধরা যাক:

- Daily users = 100,000
- Requests per user per day = 20

Daily requests:

```text
100,000 × 20 = 2,000,000 requests/day
```

Average RPS:

```text
2,000,000 / 86,400 ≈ 23.15 requests/second
```

Peak traffic average-এর 5 গুণ হলে:

```text
23.15 × 5 ≈ 116 requests/second
```

এটি illustrative estimate। বাস্তব capacity নির্ভর করে request complexity, caching, database load, traffic pattern এবং downstream services-এর ওপর।

---

# 6. Caching and CDN

## 6.1 What Is Caching?

Cache হলো frequently accessed data দ্রুত সরবরাহ করার জন্য ব্যবহৃত storage layer।

### Benefits

- Response time কমানো।
- Database load কমানো।
- Repeated computation এড়ানো।
- Read-heavy workload উন্নত করা।

## 6.2 Cache Types

| Type | Example |
|---|---|
| Browser Cache | CSS, JS, images |
| CDN Cache | Static content |
| Application Cache | Frequently accessed objects |
| Distributed Cache | Redis |
| Database Cache | Database-managed query/page caching |

## 6.3 Cache-Aside Pattern

```text
Application
    |
    v
Check Cache
    |
    ├── Cache Hit -> Return Data
    |
    └── Cache Miss
            |
            v
         Database
            |
            v
        Update Cache
            |
            v
        Return Data
```

Python conceptual example:

```python
def get_product(product_id):
    key = f"product:{product_id}"

    product = cache.get(key)

    if product is not None:
        return product

    product = load_product_from_db(product_id)

    if product is not None:
        cache.set(key, product, timeout=300)

    return product
```

## 6.4 Cache Invalidation

Data পরিবর্তিত হলে cache update বা delete করতে হয়।

Common strategies:

- TTL (Time To Live)
- Write-through
- Cache-aside invalidation
- Event-based invalidation

### Common Problems

- Cache stampede
- Hot keys
- Stale data
- Cache misses
- Inconsistent invalidation

## 6.5 CDN

CDN হলো geographically distributed server network, যা user-এর কাছাকাছি location থেকে content serve করে।

### Benefits

- Latency কমানো।
- Origin server-এর traffic কমানো।
- Static content দ্রুত সরবরাহ।
- Geographic distribution।

Private authenticated content cache করার সময় access control ও cache key সঠিকভাবে configure করতে হবে।

---

# 7. Database Design

## 7.1 SQL vs NoSQL

### SQL

Data relational tables-এ রাখা হয়।

Examples:

- PostgreSQL
- MySQL

Use cases:

- Orders
- Payments
- Inventory
- Relational business data

### NoSQL

Document, key-value, wide-column অথবা graph data model ব্যবহার করতে পারে।

Examples:

- MongoDB
- DynamoDB
- Cassandra
- Neo4j

Database selection নির্ভর করে access patterns, consistency, transaction requirements এবং operational constraints-এর ওপর।

## 7.2 Database Indexing

Index data দ্রুত খুঁজতে সাহায্য করে।

```sql
CREATE INDEX idx_users_email
ON users(email);
```

### Advantages

- Search performance উন্নত হতে পারে।
- Sorting দ্রুত হতে পারে।
- Unique constraints enforce করা যায়।

### Disadvantages

- Storage লাগে।
- Write operations ধীর হতে পারে।
- Index maintenance overhead তৈরি হয়।

Query plan পরীক্ষা করে index তৈরি করা উচিত।

## 7.3 Normalization

Normalization relational database-এর duplication ও update anomalies কমাতে সাহায্য করে।

### 1NF

Atomic values এবং repeating groups এড়ানো।

### 2NF

1NF পূরণ এবং partial dependency দূর করা।

### 3NF

2NF পূরণ এবং inappropriate transitive dependency দূর করা।

Example:

```text
Customer
--------
id
name
phone

Order
-----
id
customer_id

Product
-------
id
name

OrderItem
---------
order_id
product_id
quantity
```

## 7.4 ACID Properties

- **Atomicity:** সব operation commit হবে অথবা transaction rollback হবে।
- **Consistency:** Constraints ও invariants বজায় থাকবে।
- **Isolation:** Concurrent transaction নির্ধারিত isolation rules মেনে চলবে।
- **Durability:** Commit সফল হলে data database-এর durability guarantees অনুযায়ী সংরক্ষিত থাকবে।

Django example:

```python
from django.db import transaction

@transaction.atomic
def create_order():
    # Validate business rules.
    # Create order.
    # Create order items.
    # Update related records.
    pass
```

## 7.5 Database Replication

এক database-এর data অন্য server-এ replicate করা।

```text
        Primary Database
          /         \
         v           v
    Replica 1     Replica 2
```

### Benefits

- Read scaling।
- Redundancy।
- Disaster recovery।

### Challenges

- Replication lag।
- Failover complexity।
- Stale reads।

## 7.6 Database Sharding

বড় dataset-কে একাধিক partition বা shard-এ ভাগ করা।

```text
Shard 1 -> Users 1–100000
Shard 2 -> Users 100001–200000
Shard 3 -> Users 200001–300000
```

### Strategies

- Range-based sharding
- Hash-based sharding
- Directory-based sharding

### Challenges

- Hot shards
- Cross-shard queries
- Rebalancing
- Distributed transactions

**Remember:** Replication data copy করে; sharding data ভাগ করে।

## 7.7 SQL Query Optimization

- Slow query identify করা।
- `EXPLAIN` ব্যবহার করা।
- Appropriate index তৈরি করা।
- N+1 queries এড়ানো।
- Pagination ব্যবহার করা।
- অপ্রয়োজনীয় columns retrieve না করা।
- Connection pooling বিবেচনা করা।

Django example:

```python
orders = Order.objects.select_related("customer")

for order in orders:
    print(order.customer.name)
```

Reverse foreign key বা many-to-many relations-এর জন্য `prefetch_related()` ব্যবহার করা যায়।

---

# 8. Distributed Systems

## 8.1 Distributed System

একাধিক network-connected computer বা service মিলে একটি logical system হিসেবে কাজ করে।

Examples:

- Distributed databases
- Microservices
- Message brokers
- Distributed caching

### Challenges

- Network failures
- Partial failures
- Consistency
- Duplicate messages
- Ordering
- Clock differences
- Distributed debugging

## 8.2 CAP Theorem

CAP-এর তিনটি property:

- **Consistency:** CAP-এর অর্থে প্রতিটি successful read সর্বশেষ successful write দেখতে পায়।
- **Availability:** প্রতিটি request non-error response পায়, যদিও সেটি stale হতে পারে।
- **Partition Tolerance:** Network partition হলেও system কাজ চালিয়ে যাওয়ার চেষ্টা করে।

Network partition-এর সময় strict consistency এবং full availability একসঙ্গে guarantee করা যায় না।

## 8.3 Strong vs Eventual Consistency

| Strong Consistency | Eventual Consistency |
|---|---|
| Defined model অনুযায়ী latest write দেখা যায় | Update বন্ধ হলে replicas eventually converge করতে পারে |
| Financial balance-এর মতো ক্ষেত্রে প্রয়োজন হতে পারে | Social feed বা distributed cache-এ উপযোগী হতে পারে |
| Latency trade-off থাকতে পারে | সাময়িক stale data দেখা যেতে পারে |

## 8.4 Message Queue

Message queue producer এবং consumer-কে asynchronous processing-এর মাধ্যমে আলাদা করে।

### Components

- Producer
- Broker
- Consumer
- Acknowledgment
- Retry
- Dead Letter Queue (DLQ)

### Technologies

- RabbitMQ
- Apache Kafka
- Amazon SQS
- Redis Streams

### Important Concepts

- At-most-once delivery
- At-least-once delivery
- Idempotent consumers
- Message ordering
- Retry policy

At-least-once delivery-তে duplicate message আসতে পারে। তাই consumer-কে duplicate-safe রাখা গুরুত্বপূর্ণ।

## 8.5 Retry, Timeout and Backoff

- **Timeout:** নির্দিষ্ট সময়ে response না এলে অপেক্ষা বন্ধ করা।
- **Retry:** ব্যর্থ operation আবার চেষ্টা করা।
- **Exponential Backoff:** Retry-এর delay ক্রমান্বয়ে বাড়ানো।
- **Jitter:** Retry timing-এ random variation যোগ করা।

Blind retry না করে error type, operation semantics এবং idempotency বিবেচনা করতে হবে।

## 8.6 Circuit Breaker

Remote service বারবার fail করলে নতুন request সাময়িকভাবে block করার pattern।

### States

1. Closed — Request চলতে থাকে।
2. Open — Request দ্রুত fail বা fallback হয়।
3. Half-open — সীমিত request দিয়ে recovery পরীক্ষা করা হয়।

## 8.7 Transactional Outbox

Business data এবং event outbox record একই database transaction-এ সংরক্ষণ করা হয়।

```text
Database Transaction
    |
    ├── Save Order
    └── Save Outbox Event
              |
              v
        Event Publisher
              |
              v
         Message Broker
```

এতে database commit-এর সঙ্গে event publishing-এর consistency সমস্যা কমানো যায়। Duplicate event handling তবুও দরকার।

---

# 9. Security and Reliability

## 9.1 Authentication vs Authorization

- Authentication: User কে তা যাচাই করা।
- Authorization: User কী করতে পারবে তা যাচাই করা।

### Authentication Methods

- Sessions
- JWT
- OAuth 2.0
- OpenID Connect
- Multi-factor authentication

JWT signed হলে সেটি স্বয়ংক্রিয়ভাবে encrypted হয় না।

## 9.2 Security Principles

- HTTPS/TLS
- Least privilege
- Input validation
- Parameterized queries
- Secret management
- Encryption at rest
- Rate limiting
- Audit logging
- Backup and recovery

Django production settings-এ `DEBUG=False`, secure secret management, HTTPS এবং সঠিক cookie ও permission configuration নিশ্চিত করতে হবে।

## 9.3 Idempotency

একই operation একাধিকবার request করলেও duplicate side effect তৈরি না হওয়ার বৈশিষ্ট্য।

Example:

```http
POST /api/payments/
Idempotency-Key: order-123-payment
```

Server idempotency key ও operation result সংরক্ষণ করে duplicate requests নিরাপদে handle করতে পারে।

## 9.4 Fault Tolerance

Component failure হলেও system কাজ চালিয়ে যেতে সাহায্য করা।

Common techniques:

- Redundant instances
- Health checks
- Failover
- Timeouts
- Retries
- Circuit breakers
- Graceful degradation
- Backups
- Disaster recovery

---

# 10. Low-Level Design (LLD)

LLD individual classes, objects, methods, interfaces এবং তাদের relationships নির্ধারণ করে।

## 10.1 OOP Fundamentals

### Encapsulation

Data এবং methods একসঙ্গে রাখা এবং controlled interface দিয়ে state পরিবর্তন করা।

```python
class BankAccount:
    def __init__(self, balance=0):
        self.__balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        self.__balance += amount

    def get_balance(self):
        return self.__balance
```

### Abstraction

Implementation detail লুকিয়ে interface প্রকাশ করা।

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass
```

### Inheritance

এক class অন্য class-এর behavior inherit করতে পারে।

```python
class Animal:
    def speak(self):
        return "Sound"

class Dog(Animal):
    def speak(self):
        return "Bark"
```

### Polymorphism

একই interface দিয়ে ভিন্ন implementation ব্যবহার করা।

```python
class CardPayment(PaymentMethod):
    def pay(self, amount):
        return f"Card payment: {amount}"

class CashPayment(PaymentMethod):
    def pay(self, amount):
        return f"Cash payment: {amount}"
```

## 10.2 Composition vs Inheritance

Inheritance হলো is-a relationship; composition হলো has-a বা uses-a relationship।

```python
class EmailSender:
    def send(self, message):
        print(message)

class NotificationService:
    def __init__(self, sender):
        self.sender = sender

    def notify(self, message):
        self.sender.send(message)
```

Composition implementation পরিবর্তন করা সহজ করতে পারে।

## 10.3 UML Relationships

| Relationship | Meaning |
|---|---|
| Association | Class-গুলোর মধ্যে সম্পর্ক |
| Inheritance | Is-a relationship |
| Composition | Strong whole-part relationship |
| Aggregation | Independent parts-সহ whole-part relationship |
| Dependency | একটি class অন্যটির ওপর নির্ভরশীল |

Example:

```text
Customer 1 ---- * Order
Order    1 ---- * OrderItem
Product  1 ---- * OrderItem
```

---

# 11. OOP and SOLID Principles

## 11.1 Single Responsibility Principle (SRP)

একটি class-এর একটি সুস্পষ্ট responsibility থাকা উচিত।

Example:

- `InvoiceCalculator`
- `InvoiceEmailer`

## 11.2 Open/Closed Principle (OCP)

Code extension-এর জন্য open এবং অপ্রয়োজনীয় modification-এর জন্য closed হওয়া উচিত।

## 11.3 Liskov Substitution Principle (LSP)

Subclass যেন base class-এর contract বজায় রেখে তার জায়গায় ব্যবহার করা যায়।

## 11.4 Interface Segregation Principle (ISP)

Client-কে অপ্রয়োজনীয় method-এর ওপর নির্ভর করতে বাধ্য করা উচিত নয়।

## 11.5 Dependency Inversion Principle (DIP)

High-level business logic-কে concrete implementation-এর বদলে abstraction-এর ওপর নির্ভর করতে উৎসাহিত করে।

### SOLID-এর উদ্দেশ্য

- Coupling কমানো।
- Testing সহজ করা।
- Code maintainability বাড়ানো।
- Feature extension সহজ করা।

---

# 12. Design Patterns

Design pattern হলো common software design problem-এর জন্য পরিচিত solution structure।

## 12.1 Creational Patterns

### Factory

Object creation logic কেন্দ্রীভূত করে।

Example: Payment type অনুযায়ী object তৈরি করা।

### Builder

ধাপে ধাপে complex object তৈরি করে।

### Singleton

একটি class-এর একটিমাত্র instance নিশ্চিত করার pattern। Shared global state তৈরি করতে পারে, তাই সাবধানে ব্যবহার করা উচিত।

## 12.2 Structural Patterns

- Adapter — Incompatible interface-কে compatible করা।
- Decorator — Existing behavior wrap করে বাড়ানো।
- Facade — Complex subsystem-এর simple interface।
- Proxy — অন্য object-এর access নিয়ন্ত্রণ করা।

## 12.3 Behavioral Patterns

### Strategy

Interchangeable algorithms আলাদা implementation-এ রাখা।

### Observer

State পরিবর্তন হলে subscribers-কে notify করা।

### Command

Action-কে object হিসেবে represent করা।

## 12.4 Strategy Pattern Example

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CardPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid {amount} using card"

class MobilePayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid {amount} using mobile payment"

class Checkout:
    def __init__(self, payment_strategy):
        self.payment_strategy = payment_strategy

    def process(self, amount):
        return self.payment_strategy.pay(amount)

checkout = Checkout(CardPayment())
print(checkout.process(500))
```

নতুন payment method যোগ করতে নতুন strategy implementation তৈরি করা যায়।

---

# 13. Observability

Observability হলো system-এর output থেকে তার internal state সম্পর্কে ধারণা পাওয়ার ক্ষমতা।

## 13.1 Three Pillars

### Logs

কী ঘটেছে তার record।

Example: Failed payment, API error।

### Metrics

Numerical measurements।

Example: Request rate, error rate, latency, CPU usage।

### Distributed Tracing

একটি request বিভিন্ন service-এর মধ্য দিয়ে কীভাবে গেছে তা অনুসরণ করা।

Example:

```text
API Gateway
    -> Order Service
    -> Payment Service
    -> Database
```

## 13.2 SLI, SLO and SLA

- SLI: বাস্তবে পরিমাপ করা indicator।
- SLO: Service-এর নির্ধারিত target।
- SLA: Customer-এর সঙ্গে agreed service commitment।

## 13.3 Availability

```text
Availability =
    Uptime / Total Time × 100%
```

30 দিনের মাসে:

| Availability | Approximate Downtime |
|---|---:|
| 99% | 432 minutes |
| 99.9% | 43.2 minutes |
| 99.99% | 4.32 minutes |

---

# 14. System Design Interview Framework

যেকোনো system design problem সমাধানের জন্য এই ধাপগুলো অনুসরণ করো।

## Step 1: Requirements Gathering

- System-এর উদ্দেশ্য কী?
- কারা ব্যবহার করবে?
- Core features কী?
- কী constraints আছে?

## Step 2: Scale Estimation

- Daily active users।
- Requests per second।
- Read/write ratio।
- Data volume।
- Peak traffic।

## Step 3: API Design

- Endpoints।
- Request/response formats।
- Authentication।
- Error handling।

## Step 4: Database Design

- Entities।
- Relationships।
- Indexes।
- Transactions।
- Consistency requirements।

## Step 5: High-Level Architecture

- Client।
- Application server।
- Load balancer।
- Database।
- Cache।
- Queue।
- External services।

## Step 6: Deep Dive

- Bottlenecks।
- Database performance।
- Caching strategy।
- Concurrency।
- Failure handling।

## Step 7: Security and Reliability

- Authentication।
- Authorization।
- Timeouts।
- Retries।
- Idempotency।
- Monitoring।
- Recovery।

## Step 8: Trade-offs

কেন একটি solution বেছে নিলে এবং অন্য solution-এর কী সুবিধা-অসুবিধা আছে তা ব্যাখ্যা করো।

---

# 15. Practical System Design Problems

## 15.1 URL Shortener

### Requirements

- Long URL-কে short URL-এ রূপান্তর।
- Short code দিয়ে redirect।
- Expiration support।
- Optional analytics।

### Architecture

```text
Client
   |
   v
API Server
   |
   +----> Database
   |
   +----> Cache

Short Code
   |
   v
Lookup URL
   |
   v
HTTP Redirect
```

### Database Model

```text
URLMapping
----------
id
short_code
long_url
created_at
expires_at
user_id
```

### Important Decisions

- Short code unique হতে হবে।
- Collision handle করতে হবে।
- Lookup-এর জন্য index ও cache ব্যবহার করা যায়।
- Expiration policy নির্ধারণ করতে হবে।
- User-submitted URLs validate করতে হবে।
- Open redirect ও abuse প্রতিরোধ করতে হবে।

## 15.2 Chat Application

### Requirements

- Send messages।
- Receive messages।
- Message history।
- Delivery status।
- Online status।

### Architecture

```text
Client
   |
   v
WebSocket Gateway
   |
   v
Message Service
   |
   +----> Database
   |
   +----> Message Broker
                |
                v
          Delivery Workers
```

### Important Decisions

- Real-time communication-এর জন্য WebSocket ব্যবহার করা যেতে পারে।
- Offline messages durable storage-এ রাখতে হবে।
- Ordering strategy নির্ধারণ করতে হবে।
- Duplicate delivery handle করতে হবে।
- Presence information cache-এ রাখা যেতে পারে।

## 15.3 E-commerce Backend

### Core Components

- User Service
- Product Catalog
- Cart Service
- Order Service
- Inventory Service
- Payment Integration
- Notification Service

### Order Flow

```text
Customer
   |
   v
Checkout API
   |
   v
Validate Inventory
   |
   v
Create Pending Order
   |
   v
Payment Provider
   |
   v
Confirm Payment Status
   |
   v
Confirm Order
   |
   v
Send Notification
```

### Challenges

- Overselling প্রতিরোধ।
- Duplicate orders ঠেকানো।
- Payment timeout handle করা।
- Webhook verification।
- Inventory reservation।
- Payment reconciliation।
- Order status consistency।

## 15.4 Rate Limiter

### Requirements

- Per-user বা per-IP request limit।
- Configurable time window।
- Limit exceed করলে request reject করা।

### Algorithms

- Fixed Window Counter
- Sliding Window Log
- Sliding Window Counter
- Token Bucket
- Leaky Bucket

## 15.5 Notification System

### Requirements

- Email, SMS এবং push notifications।
- Retry handling।
- Delivery status।
- Duplicate prevention।

### Architecture

```text
Application
    |
    v
Message Queue
    |
    +----> Email Worker
    +----> SMS Worker
    +----> Push Worker
```

---

# 16. Study Roadmap

| Week | Topics | Practice |
|---|---|---|
| 1 | Fundamentals, HTTP, APIs, SQL | Django REST API |
| 2 | Database design, indexing, transactions | Order management |
| 3 | HLD, caching, load balancing | URL Shortener |
| 4 | Queues, asynchronous jobs, reliability | Notification System |
| 5 | Distributed systems, security, observability | API improvement |
| 6 | OOP, SOLID, design patterns | Parking Lot LLD |
| 7 | Chat, rate limiter, e-commerce | Mock interviews |

প্রতিদিন ১–২ ঘণ্টা অনুশীলন দিয়ে শুরু করতে পারো। নিজের বর্তমান দক্ষতা অনুযায়ী সময় বাড়ানো বা কমানো যাবে।

---

# 17. Interview Revision Questions

## Fundamentals

1. What is System Design?
2. What is the difference between HLD and LLD?
3. What are functional and non-functional requirements?
4. What is client-server architecture?
5. What is the difference between monolith and microservices?

## Scalability

6. What is vertical scaling?
7. What is horizontal scaling?
8. What is load balancing?
9. What is caching?
10. What is a CDN?
11. What is rate limiting?
12. What is the difference between latency and throughput?

## Database

13. What is database indexing?
14. What is normalization?
15. What are ACID properties?
16. What is database replication?
17. What is database sharding?
18. How do you solve the N+1 query problem?

## Distributed Systems

19. What is CAP theorem?
20. What is eventual consistency?
21. What is a message queue?
22. What is idempotency?
23. What is a circuit breaker?
24. What is the transactional outbox pattern?

## LLD

25. What are the four pillars of OOP?
26. What are SOLID principles?
27. What is composition versus inheritance?
28. What is the Strategy pattern?
29. What is the Factory pattern?
30. What is the Observer pattern?

## Practical Problems

31. Design a URL Shortener.
32. Design a Chat Application.
33. Design a Rate Limiter.
34. Design an E-commerce Backend.
35. Design a Notification System.
36. Design a Parking Lot.

---

# Final Advice

System Design শেখার সময় শুধু definition মুখস্থ করবে না।

প্রতিটি topic-এর জন্য:

1. Definition নিজের ভাষায় লিখবে।
2. Architecture diagram আঁকবে।
3. একটি real-world example ব্যাখ্যা করবে।
4. Python বা Django দিয়ে ছোট implementation করবে।
5. Design-এর trade-offs বুঝবে।
6. Interview প্রশ্নের উত্তর practice করবে।

**Recommended order for a Python/Django Backend Developer:**

`HTTP & APIs → Database Design → HLD → Caching → Queues → Distributed Systems → LLD → Design Patterns → Mock Interviews`
