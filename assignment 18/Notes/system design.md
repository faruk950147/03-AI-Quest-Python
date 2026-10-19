
# SYSTEM DESIGN: BEGINNER TO ADVANCED
## Complete Notes in Bangla + English
### Python | Django | Backend Engineering | System Design Interviews

---

# TABLE OF CONTENTS

1. Introduction to System Design
2. HLD vs LLD
3. Requirements Gathering
4. Client-Server Architecture
5. Internet and Networking Basics
6. HTTP, HTTPS, DNS and REST API
7. Latency, Throughput and Availability
8. Capacity Estimation
9. Database Fundamentals
10. SQL vs NoSQL
11. Database Schema and Normalization
12. Indexing and Query Optimization
13. Transactions and ACID
14. Database Replication
15. Database Sharding
16. Caching and Redis
17. Load Balancing
18. CDN and Object Storage
19. Message Queues and Background Jobs
20. Scalability
21. Distributed Systems
22. CAP Theorem
23. Consistency Models
24. Fault Tolerance and Reliability
25. Idempotency, Retry and Circuit Breaker
26. Rate Limiting
27. Monolith vs Microservices
28. Event-Driven Architecture
29. API Gateway
30. Authentication and Security
31. Logging, Monitoring and Observability
32. Search Systems
33. File Upload System
34. URL Shortener Design
35. Chat Application Design
36. E-commerce System Design
37. Notification Service Design
38. News Feed Design
39. Video Streaming System
40. Ride-Sharing System
41. Ticket Booking System
42. System Design Interview Framework
43. Common Interview Questions and Answers
44. Common Mistakes
45. Python and Django Practical Examples
46. Beginner-to-Advanced Project Roadmap
47. 12-Week Study Plan
48. Final Checklist
49. Glossary
50. Learning Resources

---

# 1. INTRODUCTION TO SYSTEM DESIGN

## 1.1 What is System Design?

System Design হলো একটি software system কীভাবে তৈরি, organize, scale এবং maintain করা হবে তার পরিকল্পনা।

সহজভাবে:
- কোন components থাকবে?
- Components কীভাবে communicate করবে?
- Data কোথায় store হবে?
- Traffic কীভাবে handle হবে?
- System failure হলে কী হবে?
- Security কীভাবে নিশ্চিত হবে?
- Cost ও performance-এর মধ্যে balance কীভাবে করা হবে?

Example: একটি online shopping application design করতে হলে ভাবতে হবে:
- User authentication
- Product catalog
- Shopping cart
- Order processing
- Payment integration
- Database
- Cache
- Notification
- Load balancing
- Monitoring

## 1.2 Why is System Design Important?

System Design সাহায্য করে:
- Large traffic handle করতে
- Application fast রাখতে
- Failure থেকে recover করতে
- Data consistency বজায় রাখতে
- Infrastructure cost নিয়ন্ত্রণ করতে
- Software maintainable রাখতে
- Technical trade-offs বুঝতে

## 1.3 Example: Small vs Large Application

Small application:

User -> Django -> PostgreSQL

Large application:

Users
  |
CDN / DNS
  |
Load Balancer
  |
Application Servers
  |
Cache / Message Queue / Database
  |
Object Storage / Monitoring

মনে রাখবে: সব application-এর জন্য complex architecture দরকার হয় না। Requirements অনুযায়ী design নির্বাচন করতে হয়।

---

# 2. HIGH-LEVEL DESIGN (HLD) VS LOW-LEVEL DESIGN (LLD)

## 2.1 High-Level Design

HLD system-এর বড় components এবং তাদের interactions ব্যাখ্যা করে।

Examples:
- Client
- API server
- Database
- Cache
- Load balancer
- Message broker
- Object storage

Interview-এ HLD-এর focus:
- Architecture
- Data flow
- Scalability
- Availability
- Storage choices
- Bottlenecks
- Trade-offs

## 2.2 Low-Level Design

LLD individual components কীভাবে implement হবে তা ব্যাখ্যা করে।

Examples:
- Class design
- Interfaces
- Database models
- Methods
- Design patterns
- Object relationships

Django example:

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
```

এই model হলো implementation-level design-এর একটি অংশ।

## 2.3 Difference

| HLD | LLD |
|---|---|
| System architecture | Component implementation |
| Services and data flow | Classes and methods |
| Scalability and availability | Code structure and patterns |
| Architecture diagrams | Class diagrams |
| Large-scale view | Detailed view |

---

# 3. REQUIREMENTS GATHERING

Design করার আগে requirements পরিষ্কার করতে হবে।

## 3.1 Functional Requirements

System কী কী কাজ করবে?

Example: E-commerce
- User register করতে পারবে
- User login করতে পারবে
- Products browse করতে পারবে
- Cart-এ item যোগ করতে পারবে
- Order place করতে পারবে
- Payment করতে পারবে

## 3.2 Non-Functional Requirements

System কত ভালোভাবে কাজ করবে?

Examples:
- Performance
- Scalability
- Availability
- Reliability
- Security
- Maintainability
- Durability
- Cost efficiency

Example requirements:
- API response time অধিকাংশ request-এর জন্য 200 ms-এর নিচে রাখতে হবে
- System 100,000 daily active users handle করবে
- Payment data secure রাখতে হবে
- Database backup থাকতে হবে

এগুলো উদাহরণ; real target business requirements অনুযায়ী ঠিক করতে হবে।

## 3.3 Constraints

Constraints হলো design-এর সীমাবদ্ধতা।

Examples:
- Budget
- Deadline
- Team size
- Existing technology
- Legal requirements
- Data residency
- Cloud provider

## 3.4 Interview Rule

Design শুরু করার আগে জিজ্ঞেস করো:
1. Main features কী?
2. Expected users কত?
3. Daily requests কত?
4. Read বেশি, নাকি write বেশি?
5. Data কতদিন রাখতে হবে?
6. Availability target কত?
7. Strong consistency দরকার কি?
8. Budget বা technology constraints কী?

---

# 4. CLIENT-SERVER ARCHITECTURE

Client হলো request পাঠানো application।

Examples:
- Browser
- Mobile app
- Desktop application

Server হলো request process করে response দেওয়া system।

Diagram:

Client
  |
  | HTTP Request
  v
Server
  |
  v
Database
  |
  v
Server
  |
  | HTTP Response
  v
Client

Example:

GET /api/products/

Response:

```json
{
  "results": [
    {
      "id": 1,
      "name": "Keyboard",
      "price": "1500.00"
    }
  ]
}
```

Client সাধারণত business logic-এর authoritative source নয়। Sensitive validation ও authorization server-side করতে হয়।

---

# 5. INTERNET AND NETWORKING BASICS

## 5.1 IP Address

IP address network-এ device বা network interface identify করতে সাহায্য করে।

Example:
192.0.2.10

## 5.2 Port

Port একটি machine-এর নির্দিষ্ট network service-এ connection নির্দেশ করে।

Common ports:
- HTTP: 80
- HTTPS: 443
- PostgreSQL: 5432
- Redis: 6379

Production-এ database port public internet-এ expose করা উচিত নয়।

## 5.3 TCP

TCP reliable, ordered byte stream দেয়।

ব্যবহার:
- HTTPS traffic
- Database connections
- অনেক API communication

## 5.4 UDP

UDP connectionless datagram transport।

ব্যবহার:
- DNS-এর কিছু query
- Real-time media
- Gaming
- কিছু low-latency protocol

## 5.5 TLS

TLS communication encrypt করে এবং server identity verify করতে সাহায্য করে।

HTTPS = HTTP over TLS.

## 5.6 DNS

DNS domain name-কে সংশ্লিষ্ট IP address বা অন্য DNS record-এ resolve করতে সাহায্য করে।

Example:
example.com -> IP address

DNS change সব জায়গায় সঙ্গে সঙ্গে কার্যকর হবে এমন নয়; caching ও TTL গুরুত্বপূর্ণ।

---

# 6. HTTP, HTTPS, DNS AND REST API

## 6.1 HTTP Methods

GET:
Resource পড়া।

POST:
Resource তৈরি বা operation শুরু করা।

PUT:
সাধারণত resource replace করা।

PATCH:
Resource-এর কিছু field update করা।

DELETE:
Resource delete করা।

## 6.2 HTTP Status Codes

200 OK
201 Created
202 Accepted
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
429 Too Many Requests
500 Internal Server Error
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout

401 সাধারণত authentication দরকার বা invalid।
403 মানে request বোঝা হয়েছে, কিন্তু permission নেই।

## 6.3 REST API Example

Endpoints:

GET    /api/products/
GET    /api/products/42/
POST   /api/products/
PATCH  /api/products/42/
DELETE /api/products/42/

Good API practices:
- Consistent naming
- Input validation
- Authentication and authorization
- Pagination
- Error response format
- API versioning where needed
- Rate limiting
- Documentation

## 6.4 Pagination

Offset pagination:

GET /api/products/?limit=20&offset=40

Cursor pagination:

GET /api/products/?cursor=eyJpZCI6MTAwfQ

Large datasets-এ cursor pagination অনেক ক্ষেত্রে বেশি efficient এবং changing data-এর সঙ্গে বেশি stable হতে পারে।

---

# 7. LATENCY, THROUGHPUT AND AVAILABILITY

## 7.1 Latency

একটি request সম্পন্ন হতে যত সময় লাগে।

Example:
API latency = 120 ms

## 7.2 Throughput

একক সময়ে system যতগুলো operation handle করে।

Example:
5,000 requests/second

## 7.3 RPS

Requests Per Second.

Formula:

RPS = Total Requests / Total Seconds

Example:
864,000 requests/day ÷ 86,400 seconds/day
= 10 average requests/second

Peak traffic average-এর অনেক বেশি হতে পারে।

## 7.4 Percentile Latency

p50: 50% requests এই সময়ের মধ্যে complete হয়।

p95: 95% requests এই সময়ের মধ্যে complete হয়।

p99: 99% requests এই সময়ের মধ্যে complete হয়।

শুধু average latency দেখলে slow requests আড়াল হয়ে যেতে পারে।

## 7.5 Availability

Availability = Uptime / Total Scheduled Time × 100%

Illustrative annual downtime:

| Availability | Approx. downtime/year |
|---|---:|
| 99% | 3.65 days |
| 99.9% | 8.76 hours |
| 99.99% | 52.6 minutes |
| 99.999% | 5.26 minutes |

এই হিসাব 365-day year ধরে করা হয়েছে।

---

# 8. CAPACITY ESTIMATION

Interview-এ exact number নয়, assumptions পরিষ্কারভাবে দেখানো গুরুত্বপূর্ণ।

## 8.1 Daily Active Users

ধরি:
- DAU = 1,000,000
- User প্রতি দিনে 20 requests

Daily requests:

1,000,000 × 20
= 20,000,000 requests/day

Average RPS:

20,000,000 / 86,400
≈ 231 RPS

যদি peak traffic average-এর 5 গুণ হয়:

Peak RPS ≈ 1,155

এটি illustrative estimate, production measurement নয়।

## 8.2 Storage Estimation

ধরি:
- 2 million new records/day
- Average stored record size = 1 KB

Daily raw storage:

2,000,000 × 1 KB
≈ 2 GB/day

One year:

2 GB × 365
≈ 730 GB/year

Actual storage বেশি হতে পারে:
- Indexes
- Replicas
- Metadata
- Backups
- Logs
- Database overhead

## 8.3 Bandwidth

Bandwidth per second:

Requests/second × Average response size

ধরি:
- 1,000 RPS
- 50 KB average response

Approximate outgoing bandwidth:

1,000 × 50 KB
= 50 MB/s

Protocol overhead ও cache hit ratio এখানে ধরা হয়নি।

## 8.4 Database Connections

যদি 10 application instances-এর প্রতিটি 30 database connections ধরে:

10 × 30 = 300 connections

Database-এর connection limit ও workload অনুযায়ী connection pool configure করতে হবে।

---

# 9. DATABASE FUNDAMENTALS

Database application data store করে।

Common choices:
- PostgreSQL
- MySQL
- SQLite
- MongoDB
- Redis
- Elasticsearch / OpenSearch
- Cassandra

একটি technology সব workload-এর জন্য best নয়।

## 9.1 Relational Database

Data tables, rows এবং columns-এ রাখা হয়।

Example:

Users
| id | name | email |
|---|---|---|
| 1 | Omar | omar@example.com |
| 2 | Sara | sara@example.com |

Orders
| id | user_id | total |
|---|---|---|
| 101 | 1 | 2500 |
| 102 | 2 | 1800 |

`user_id` users table-এর সঙ্গে relation তৈরি করে।

## 9.2 Primary Key

প্রতিটি row uniquely identify করে।

## 9.3 Foreign Key

অন্য table-এর row-এর সঙ্গে relation establish করে।

## 9.4 Constraints

Examples:
- NOT NULL
- UNIQUE
- CHECK
- FOREIGN KEY

Constraints database level-এ invalid data আটকাতে সাহায্য করে।

---

# 10. SQL VS NOSQL

## SQL

Examples:
- PostgreSQL
- MySQL

Strengths:
- Relationships
- Joins
- Transactions
- Structured schema
- Complex queries

## NoSQL

Examples:
- MongoDB
- Cassandra
- DynamoDB

NoSQL database-গুলোর data model ও consistency guarantees আলাদা হতে পারে।

Potential benefits:
- Flexible document schema
- Particular access patterns-এর জন্য horizontal scaling
- Large distributed workloads-এর জন্য suitable data models

## Selection Guide

PostgreSQL ব্যবহার করো যখন:
- Relational data আছে
- Transactions দরকার
- Complex joins আছে
- Strong consistency গুরুত্বপূর্ণ

Document database বিবেচনা করো যখন:
- Data naturally documents আকারে থাকে
- Access pattern document-oriented
- Flexible schema দরকার

Key-value store ব্যবহার করো যখন:
- Key দিয়ে দ্রুত lookup দরকার
- Cache বা session data রাখা হবে

Database বাছাই hype দেখে নয়; data model, query pattern, consistency এবং operations বিবেচনা করে করতে হবে।

---

# 11. DATABASE SCHEMA AND NORMALIZATION

## 11.1 Normalization

Normalization duplicate data এবং update anomalies কমাতে সাহায্য করে।

Bad design:

Orders table-এ প্রতিটি order-এর সঙ্গে customer name, email ও address বারবার রাখা।

Better design:

Users table
Orders table
OrderItems table

## 11.2 Example Schema

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    status VARCHAR(30) NOT NULL,
    total NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orders_user_created
ON orders(user_id, created_at DESC);
```

## 11.3 Denormalization

Read performance improve করার জন্য controlled duplication।

Advantages:
- Fewer joins
- Faster reads in some workloads

Disadvantages:
- Duplicate data
- Update complexity
- Consistency problems

প্রথমে sensible normalized design দিয়ে শুরু করো; measurements দেখে denormalize করো।

---

# 12. INDEXING AND QUERY OPTIMIZATION

## 12.1 What is an Index?

Index database-কে matching rows খুঁজে পেতে সাহায্য করে।

Without index:
Large table-এর অনেক row scan হতে পারে।

With index:
Database relevant rows দ্রুত locate করতে পারে।

## 12.2 Example

```sql
CREATE INDEX idx_users_email ON users(email);
```

Query:

```sql
SELECT *
FROM users
WHERE email = 'omar@example.com';
```

## 12.3 Composite Index

```sql
CREATE INDEX idx_orders_user_status
ON orders(user_id, status);
```

Column order গুরুত্বপূর্ণ। Index-এর usefulness query pattern-এর ওপর নির্ভর করে।

## 12.4 Index Disadvantages

- Additional storage
- INSERT overhead
- UPDATE overhead
- DELETE overhead
- Maintenance cost

## 12.5 Query Optimization

Check:
- `EXPLAIN`
- `EXPLAIN ANALYZE`
- N+1 queries
- Missing indexes
- Over-fetching
- Large OFFSET pagination
- Unnecessary joins
- Slow queries

Django example:

```python
orders = (
    Order.objects
    .filter(user_id=1)
    .select_related("user")
    .order_by("-created_at")
)
```

`select_related()` foreign-key বা one-to-one relation-এর জন্য useful। Many-to-many বা reverse one-to-many-এর জন্য সাধারণত `prefetch_related()` বিবেচনা করো।

---

# 13. TRANSACTIONS AND ACID

ACID database transactions-এর চারটি গুরুত্বপূর্ণ property।

## Atomicity

Transaction পুরোপুরি succeed করবে অথবা rollback হবে।

## Consistency

Transaction database constraints ও rules বজায় রাখবে।

## Isolation

Concurrent transactions একে অপরকে কীভাবে observe করবে তা নির্ধারণ করে।

## Durability

Committed data failure-এর পরও টিকে থাকার guarantee পায়, database configuration অনুযায়ী।

## Django Transaction Example

```python
from django.db import transaction

@transaction.atomic
def create_order(user, product, quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    product = Product.objects.select_for_update().get(
        pk=product.pk
    )

    if product.stock < quantity:
        raise ValueError("Insufficient stock")

    product.stock -= quantity
    product.save(update_fields=["stock"])

    order = Order.objects.create(
        user=user,
        status="pending",
    )

    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=quantity,
    )

    return order
```

এটি illustrative example। বাস্তবে price snapshot, order total, inventory reservation, payment flow, retry handling এবং idempotency-ও design করতে হবে।

---

# 14. DATABASE REPLICATION

Replication হলো database data-এর copies maintain করা।

Architecture:

Application
    |
    v
Primary Database
    |
    +----> Replica 1
    |
    +----> Replica 2

Primary সাধারণত writes গ্রহণ করে। Replicas read traffic নিতে পারে, যদি consistency requirements অনুমতি দেয়।

## Advantages

- Read scalability
- Failover options
- Additional copies

## Disadvantages

- Replication lag
- Operational complexity
- Failover complexity
- Replica data পুরোনো হতে পারে

Read-after-write consistency দরকার হলে কিছু read primary থেকে করতে হতে পারে।

---

# 15. DATABASE SHARDING

Sharding হলো data-কে একাধিক database node-এ partition করা।

Example:

User IDs 1–1M -> Shard A
User IDs 1M–2M -> Shard B
User IDs 2M–3M -> Shard C

## Common Strategies

### Range-based Sharding

ID range বা date range অনুযায়ী।

Problem:
Hot ranges তৈরি হতে পারে।

### Hash-based Sharding

hash(key) অনুযায়ী partition।

Advantage:
Data distribution balanced হতে পারে।

Disadvantage:
Resharding complex হতে পারে।

### Geographic Sharding

Region অনুযায়ী data partition।

## Sharding Challenges

- Cross-shard joins
- Transactions across shards
- Rebalancing
- Hot partitions
- Global uniqueness
- Operational complexity

Sharding সাধারণত প্রথম solution নয়। Indexing, query optimization, caching ও replication যথেষ্ট কি না আগে evaluate করো।

---

# 16. CACHING AND REDIS

## 16.1 What is Caching?

Frequently accessed data দ্রুত ফেরত দেওয়ার জন্য temporary storage-এ রাখা।

Architecture:

Client
  |
Application
  |
  +---- Cache Hit ----> Return Data
  |
  +---- Cache Miss ---> Database
                           |
                           v
                       Store in Cache
                           |
                           v
                       Return Data

## 16.2 Cache Benefits

- Lower latency
- Lower database load
- Better throughput
- Faster repeated reads

## 16.3 Cache Problems

- Stale data
- Cache invalidation
- Cache stampede
- Hot keys
- Memory limitations
- Cache outages

## 16.4 Cache-Aside Pattern

1. Cache lookup
2. Hit হলে return
3. Miss হলে database query
4. Result cache-এ store
5. Result return

Python example:

```python
import json
import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)

def get_product(product_id):
    key = f"product:{product_id}"

    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)

    product = load_product_from_database(product_id)

    if product is not None:
        redis_client.setex(
            key,
            300,
            json.dumps(product),
        )

    return product
```

`load_product_from_database()` এখানে illustrative placeholder।

## 16.5 Cache Invalidation

Product update হলে cache invalidate করা যেতে পারে:

```python
redis_client.delete(f"product:{product_id}")
```

Cache TTL ব্যবহার করো। Critical consistency requirement থাকলে শুধু TTL যথেষ্ট নাও হতে পারে।

## 16.6 Cache Stampede

একটি popular key expire হলে অনেক request একই সময় database-এ চলে যায়।

Mitigations:
- TTL jitter
- Single-flight request coalescing
- Short-lived stale-while-revalidate
- Controlled refresh
- Locking with careful timeout handling

---

# 17. LOAD BALANCING

Load balancer incoming requests একাধিক server-এ distribute করে।

Architecture:

Users
  |
Load Balancer
  |
  +---- App Server 1
  +---- App Server 2
  +---- App Server 3
              |
           Database

## Common Algorithms

### Round Robin
একটির পর একটি server নির্বাচন।

### Least Connections
যে server-এ active connection কম, তাকে preference।

### Weighted Round Robin
Server capacity অনুযায়ী weight দেওয়া।

### Consistent Hashing
একই key-কে consistent node-এ route করতে সাহায্য করে।

## Health Checks

Unhealthy server-এ traffic না পাঠাতে health checks ব্যবহার করা হয়।

## Important Django Considerations

- Session state external storage-এ রাখতে হতে পারে
- Uploaded files local disk-এ রাখলে instance-ভেদে সমস্যা হতে পারে
- Application instances stateless রাখা সহজে scale করতে সাহায্য করে
- Secret configuration environment/secret manager থেকে নিতে হবে

---

# 18. CDN AND OBJECT STORAGE

## 18.1 CDN

Content Delivery Network ব্যবহারকারীর কাছাকাছি edge location থেকে static content deliver করে।

Useful for:
- Images
- CSS
- JavaScript
- Public downloads
- Video segments

Benefits:
- Lower latency
- Reduced origin load
- Improved delivery performance

## 18.2 Object Storage

Examples:
- Amazon S3
- Cloudflare R2
- Google Cloud Storage
- Azure Blob Storage

Large files database row-এর মধ্যে না রেখে object storage-এ রাখা সাধারণ pattern।

Database-এ রাখা যেতে পারে:
- Object key
- Owner
- File metadata
- Content type
- Permissions
- Upload status

## 18.3 File Upload Flow

Client
  |
API Server -> Validate Permission
  |
Pre-signed Upload URL
  |
Object Storage
  |
Database Metadata
  |
CDN / Authorized Download

Large file application server-এর মধ্য দিয়ে stream করতেই হবে এমন নয়। Pre-signed URL ব্যবহার করে client সরাসরি storage-এ upload করতে পারে।

---

# 19. MESSAGE QUEUES AND BACKGROUND JOBS

## 19.1 Why Queues?

কিছু কাজ request-এর response-এর মধ্যে করতে হয় না।

Examples:
- Email sending
- SMS
- Image processing
- Report generation
- Webhook delivery
- Analytics
- Video transcoding

Architecture:

Client
  |
Django API
  |
Save Data + Enqueue Job
  |
Return Response

Queue
  |
Worker
  |
Execute Job

## 19.2 Common Technologies

- Celery
- RabbitMQ
- Redis-backed queues
- Kafka
- Amazon SQS

সব queue technology একই purpose বা delivery guarantee দেয় না।

## 19.3 Celery Example

```python
from celery import shared_task

@shared_task
def send_welcome_email(user_id):
    user = User.objects.get(pk=user_id)
    send_email_to_user(user.email)
```

Request handler:

```python
send_welcome_email.delay(user.id)
```

এখানে worker ও broker আলাদাভাবে configure করতে হবে।

## 19.4 Important Queue Concepts

- Producer
- Consumer
- Broker
- Acknowledgement
- Retry
- Dead-letter queue
- Consumer lag
- Backpressure
- Idempotent processing

Queue-তে message পাঠানো হয়েছে মানেই কাজটি সফলভাবে complete হয়েছে—এমন নয়।

---

# 20. SCALABILITY

Scalability হলো workload বাড়লে system-এর capacity বাড়ানোর ক্ষমতা।

## 20.1 Vertical Scaling

একটি machine-এর CPU, RAM বা storage বাড়ানো।

Advantages:
- Simple
- Fewer distributed components

Disadvantages:
- Hardware limits
- Large instance cost
- Single-node failure risk

## 20.2 Horizontal Scaling

আরও server বা instance যোগ করা।

Advantages:
- Higher aggregate capacity
- Redundancy
- Flexible scaling

Disadvantages:
- Coordination complexity
- Distributed state
- Network failures
- Operational overhead

## 20.3 Stateless Architecture

Application instance request process করার জন্য local in-memory state-এর ওপর নির্ভর না করলে horizontal scaling সহজ হয়।

Examples:
- Shared session store
- Database-backed state
- Object storage
- External cache

## 20.4 Bottleneck

System-এর যে component overall throughput সীমাবদ্ধ করে।

Examples:
- Slow database query
- CPU-intensive endpoint
- Connection pool exhaustion
- Third-party API
- Single queue consumer

Optimization করার আগে measurement দরকার।

---

# 21. DISTRIBUTED SYSTEMS

Distributed system হলো network-এর মাধ্যমে communicate করা একাধিক independent nodes-এর system।

Examples:
- Distributed database
- Microservices architecture
- Kafka cluster
- Distributed cache
- Cloud storage

## 21.1 Distributed Systems Challenges

- Network latency
- Partial failure
- Duplicate messages
- Clock differences
- Data consistency
- Leader election
- Network partition
- Retry storms
- Split brain

## 21.2 Partial Failure

একটি service fail করলেও পুরো system-এর অন্য parts চলতে পারে।

Example:
Order API কাজ করছে, কিন্তু notification service unavailable।

ভালো design-এ order creation সফল হতে পারে, notification queue-তে রাখা হয় এবং পরে retry করা হয়।

## 21.3 Timeouts

Remote calls-এর জন্য timeout দরকার। Timeout না থাকলে threads বা connections দীর্ঘ সময় আটকে থাকতে পারে।

## 21.4 Retries

Temporary failure হলে retry করা যায়।

কিন্তু retry:
- Bounded হতে হবে
- Exponential backoff ব্যবহার করতে পারে
- Jitter ব্যবহার করতে পারে
- Non-idempotent operation-এ duplicate side effect তৈরি করতে পারে

---

# 22. CAP THEOREM

CAP Theorem distributed data system-এর একটি fundamental concept।

Network partition হলে system-এর behavior-এ trade-off আসে:

- Consistency (C)
- Availability (A)
- Partition Tolerance (P)

## Consistency

CAP context-এ, successful operation-গুলোকে একটি single-copy sequential order-এর মতো দেখা যায় কি না, অর্থাৎ linearizable behavior।

## Availability

CAP-এর formal definition অনুযায়ী প্রতিটি request-এ non-error response দেওয়া হয়।

## Partition Tolerance

Network partition হলেও system কীভাবে behave করবে।

## Practical Understanding

Distributed network-এ partition সম্ভব। Partition ঘটলে system-কে consistency ও availability-এর মধ্যে trade-off করতে হতে পারে।

CP-style behavior:
- কিছু request reject বা block হতে পারে
- Consistency বজায় রাখার চেষ্টা করে

AP-style behavior:
- কিছু request accept হতে পারে
- Temporary inconsistency থাকতে পারে

বাস্তব database-এ CAP label alone দিয়ে পুরো system বোঝা যায় না। Exact consistency guarantee, failure mode ও operation semantics দেখতে হবে।

---

# 23. CONSISTENCY MODELS

## Strong Consistency / Linearizability

Successful write-এর পর পরবর্তী read সর্বশেষ committed value দেখতে পায়, operation ordering guarantee অনুযায়ী।

Useful for:
- Account balances
- Inventory reservation
- Certain payment state transitions

## Eventual Consistency

নতুন update বন্ধ থাকলে replicas সময়ের সঙ্গে converge করার কথা।

Useful for:
- Some social counters
- Search indexes
- Analytics
- Non-critical replicated views

## Read-Your-Writes

একজন user নিজের write-এর পর সেই update দেখতে পারে।

## Monotonic Reads

একজন reader একবার যে version দেখেছে, পরে তার চেয়ে পুরোনো version দেখতে পায় না।

Consistency model system-এর requirements অনুযায়ী বেছে নিতে হবে।

---

# 24. FAULT TOLERANCE AND RELIABILITY

## 24.1 Fault Tolerance

কোনো component fail করলেও system-এর critical functionality বজায় রাখার ক্ষমতা।

## 24.2 Redundancy

একাধিক instances বা copies রাখা।

Examples:
- Multiple application servers
- Database replicas
- Multiple availability zones

## 24.3 Failover

Primary component unavailable হলে backup component ব্যবহার করা।

## 24.4 Disaster Recovery

Major outage-এর পর system ও data restore করার পরিকল্পনা।

Important concepts:

RPO (Recovery Point Objective):
কতটা recent data loss গ্রহণযোগ্য।

RTO (Recovery Time Objective):
কত সময়ের মধ্যে service recover করতে হবে।

## 24.5 Backups

Backups থাকতে হবে এবং restore test করতে হবে। Backup আছে মানেই recovery নিশ্চিত নয়।

## 24.6 Graceful Degradation

একটি optional service unavailable হলেও core service চালু রাখা।

Example:
Recommendation service down, কিন্তু product browsing চালু।

---

# 25. IDEMPOTENCY, RETRY AND CIRCUIT BREAKER

## 25.1 Idempotency

একই operation একাধিকবার execute হলেও intended final effect একই থাকে।

GET সাধারণত idempotent।

PUT সাধারণত idempotent হওয়ার জন্য design করা হয়।

POST operation স্বয়ংক্রিয়ভাবে idempotent নয়।

## 25.2 Idempotency Key

Payment বা order creation-এর জন্য client একটি unique key পাঠাতে পারে।

Example:

Idempotency-Key: 4c6d9e...

Server:
1. Key validate করে
2. Existing operation check করে
3. New operation create করে
4. Result store করে
5. Duplicate request-এ আগের result return করে

Idempotency key-এর uniqueness, expiry এবং concurrent request handling design করতে হবে।

## 25.3 Exponential Backoff

Retry delay বাড়ানো:

Attempt 1: 100 ms
Attempt 2: 200 ms
Attempt 3: 400 ms
Attempt 4: 800 ms

Jitter যোগ করলে clients একসঙ্গে retry করার ঝুঁকি কমে।

## 25.4 Circuit Breaker

Repeated failures হলে remote dependency-তে request সাময়িকভাবে বন্ধ করে।

States:
- Closed: Requests pass through
- Open: Requests blocked or fail fast
- Half-open: Limited test requests allowed

Circuit breaker outage-এর সময় resource exhaustion কমাতে সাহায্য করে।

---

# 26. RATE LIMITING

Rate limiting নির্দিষ্ট সময়ে request-এর সংখ্যা নিয়ন্ত্রণ করে।

Example:
100 requests per minute per user.

## Algorithms

### Fixed Window

প্রতিটি fixed interval-এ counter।

Problem:
Window boundary-তে traffic burst হতে পারে।

### Sliding Window

Moving interval অনুযায়ী limit।

### Token Bucket

Tokens refill হয়। Token থাকলে request allowed।

### Leaky Bucket

Controlled rate-এ request process বা release করা হয়।

## Example

User:
- Limit = 100 requests/minute
- 101st request = HTTP 429

## Implementation Considerations

- Per user
- Per IP
- Per API key
- Per endpoint
- Distributed counter
- Retry-After header
- Trusted proxy configuration

IP-based limiting একা যথেষ্ট নয়; NAT ও distributed attacks বিবেচনা করতে হবে।

---

# 27. MONOLITH VS MICROSERVICES

## Monolithic Architecture

একটি application codebase বা deployable unit-এ major functionality থাকে।

Advantages:
- Easy to start
- Simpler local development
- Straightforward transactions
- Fewer network calls

Disadvantages:
- Large codebase complexity
- Coordinated deployments
- Independent scaling সীমিত হতে পারে

## Microservices Architecture

System আলাদা services-এ বিভক্ত হয়।

Example:

User Service
Product Service
Order Service
Payment Service
Notification Service

Advantages:
- Independent deployment
- Independent scaling
- Clear service boundaries

Disadvantages:
- Network failure
- Distributed transactions
- Observability complexity
- Deployment overhead
- Data consistency challenges

## Recommendation

ছোট team ও early-stage project-এ modular monolith প্রায়ই practical starting point।

কোনো service independently scale, deploy বা maintain করার বাস্তব কারণ তৈরি হলে microservices বিবেচনা করো।

---

# 28. EVENT-DRIVEN ARCHITECTURE

একটি component event publish করে, অন্য components সেই event consume করে।

Example:

Order Service
  |
  | OrderCreated event
  v
Message Broker
  |
  +----> Notification Consumer
  |
  +----> Analytics Consumer
  |
  +----> Inventory Consumer

## Benefits

- Loose coupling
- Asynchronous processing
- Independent consumers
- Easier integration between bounded contexts

## Challenges

- Duplicate events
- Event ordering
- Eventual consistency
- Schema evolution
- Retry behavior
- Debugging complexity

## Transactional Outbox Pattern

Problem:
Database commit সফল হলো, কিন্তু event publish ব্যর্থ হলো।

Solution:
একই database transaction-এ business record ও outbox event লিখে রাখো। Background publisher পরে event publish করবে।

Consumer idempotent হতে হবে, কারণ delivery duplicate হতে পারে।

---

# 29. API GATEWAY

API Gateway clients ও backend services-এর মধ্যে entry point হিসেবে কাজ করতে পারে।

Responsibilities:
- Routing
- Authentication integration
- Rate limiting
- TLS termination
- Request logging
- Request transformation

Diagram:

Client
  |
API Gateway
  |
  +---- User Service
  +---- Product Service
  +---- Order Service

Gateway নিজেই bottleneck বা single point of failure হতে পারে, তাই production deployment-এ redundancy ও monitoring দরকার।

---

# 30. AUTHENTICATION AND SECURITY

## Authentication

User কে, তা verify করা।

## Authorization

User কী করতে পারবে, তা determine করা।

## Common Mechanisms

- Server-side sessions
- Access tokens
- OAuth 2.0
- OpenID Connect
- API keys for appropriate machine-to-machine use cases

## Security Practices

- HTTPS/TLS
- Password hashing using suitable password hash algorithms
- Least privilege
- Input validation
- Output encoding
- CSRF protection where relevant
- Secure cookies
- Secret management
- Audit logs
- Dependency updates
- Database access control
- Encryption at rest where required
- Backup protection

## Django Security

- `DEBUG = False` in production
- Correct `ALLOWED_HOSTS`
- Secure secret management
- CSRF protection
- HTTPS enforcement
- Secure session cookies
- Secure password handling
- Permission checks on every sensitive operation
- Avoid raw SQL unless safely parameterized

Never commit production passwords, tokens or secret keys to Git.

---

# 31. LOGGING, MONITORING AND OBSERVABILITY

## Logging

Events-এর detailed record।

Example:
- Request received
- Payment failed
- Worker retry
- Database timeout

## Metrics

Numerical measurements over time।

Examples:
- Requests per second
- Error rate
- p95 latency
- CPU usage
- Memory usage
- Queue lag
- Database connection count

## Tracing

একটি request multiple services অতিক্রম করলে পুরো path track করা।

## The Three Pillars

Logs + Metrics + Traces

## Golden Signals

- Latency
- Traffic
- Errors
- Saturation

## Tools

- Prometheus
- Grafana
- OpenTelemetry
- Sentry
- ELK / OpenSearch stack

Alert meaningful হতে হবে। Alert fatigue হলে important failures miss হতে পারে।

---

# 32. SEARCH SYSTEMS

Search requirements সাধারণ SQL query থেকে আলাদা হতে পারে।

Possible features:
- Full-text search
- Typo tolerance
- Autocomplete
- Ranking
- Filters
- Facets
- Highlighting

Technologies:
- PostgreSQL full-text search
- Elasticsearch
- OpenSearch
- Dedicated search services

Typical architecture:

Client
  |
Search API
  |
Search Index
  |
Return Results

Database source of truth হতে পারে, আর search index asynchronousভাবে update হতে পারে।

এই কারণে search results সাময়িকভাবে stale হতে পারে।

---

# 33. FILE UPLOAD SYSTEM DESIGN

## Requirements

- User upload করবে
- File type validate হবে
- File size limit থাকবে
- File private বা public হতে পারে
- Download authorization থাকবে
- Metadata store হবে

## Architecture

Client
  |
Django API
  |
Authorize Upload
  |
Pre-signed URL
  |
Object Storage
  |
Metadata Database
  |
Optional CDN

## Security Considerations

- Maximum file size
- Allowed file types
- File content validation
- Malware scanning where appropriate
- Random object keys
- Private bucket by default
- Short-lived pre-signed URLs
- Access control
- Content-Disposition and safe serving
- Quotas

User-provided filename-কে trusted filesystem path হিসেবে ব্যবহার করো না।

---

# 34. SYSTEM DESIGN CASE STUDY: URL SHORTENER

## Requirements

- Long URL থেকে short URL তৈরি
- Short URL redirect
- Duplicate long URL allowed কি না define করা
- Expiration optional
- Abuse protection
- Analytics optional

## API

POST /api/urls/
GET /{short_code}

Request:

```json
{
  "url": "https://example.com/articles/system-design"
}
```

Response:

```json
{
  "short_code": "aB91x",
  "short_url": "https://short.example/aB91x"
}
```

## Architecture

Client
  |
Load Balancer
  |
URL Service
  |
  +---- Redis Cache
  |
  +---- PostgreSQL
  |
Analytics Queue

## Database Schema

urls:
- id
- short_code
- original_url
- created_at
- expires_at
- owner_id

short_code-এর ওপর UNIQUE constraint দরকার।

## Read Flow

1. User short URL open করে
2. Cache lookup
3. Cache miss হলে database lookup
4. URL expiry ও status check
5. Redirect response
6. Analytics event asynchronousভাবে process করা যেতে পারে

## Short Code Generation

Options:
- Random token
- Base62 encoding of unique ID
- Carefully designed hash-based scheme

Collision handling দরকার।

Random code generate করলে unique constraint দিয়ে collision detect করে retry করা যায়।

## Trade-offs

- Random code vs encoded ID
- 301 vs 302 redirect
- Cache hit rate
- Abuse detection
- Analytics accuracy
- Expiration cleanup

---

# 35. SYSTEM DESIGN CASE STUDY: CHAT APPLICATION

## Requirements

- One-to-one messaging
- Group chat
- Message history
- Online presence
- Delivery status
- Notifications
- Optional read receipts

## Architecture

Clients
  |
WebSocket Gateway
  |
Chat Service
  |
  +---- Message Database
  |
  +---- Presence Store
  |
  +---- Message Broker
  |
  +---- Notification Service

## WebSocket

Persistent bidirectional connection দেয়।

Useful for:
- Chat
- Live notifications
- Collaborative interfaces

## Message Flow

1. Sender sends message
2. Server authenticates and authorizes sender
3. Message persisted
4. Server routes message to recipient connection
5. Recipient acknowledges delivery
6. Offline recipient notification পেতে পারে

## Important Decisions

- Message ordering
- Message ID
- Retry and deduplication
- Group fan-out
- Offline storage
- WebSocket reconnection
- Presence expiry
- Encryption requirements

Message delivered হওয়া এবং user message পড়া এক জিনিস নয়।

---

# 36. SYSTEM DESIGN CASE STUDY: E-COMMERCE

## Main Components

- User Service
- Product Catalog
- Search
- Cart
- Order Service
- Inventory
- Payment Integration
- Notification
- Analytics

## High-Level Architecture

Client
  |
Load Balancer
  |
Django Application
  |
  +---- PostgreSQL
  |
  +---- Redis
  |
  +---- Queue / Workers
  |
  +---- Object Storage
  |
  +---- Payment Provider

## Order Flow

1. User checks out
2. Server validates cart
3. Price and stock are checked
4. Order is created in a pending state
5. Inventory is reserved according to business rules
6. Payment provider processes payment
7. Payment result is verified
8. Order status is updated
9. Confirmation notification is queued

## Critical Concerns

- Price must be calculated server-side
- Inventory race conditions
- Duplicate checkout requests
- Payment webhook verification
- Idempotency
- Refund handling
- Reservation expiration
- Audit logs
- Reconciliation jobs

Payment provider API call-এর মধ্যে দীর্ঘ database transaction খোলা রাখা সাধারণত ভালো design নয়।

একটি distributed checkout flow-এর জন্য explicit state machine ও compensation logic দরকার হতে পারে।

---

# 37. SYSTEM DESIGN CASE STUDY: NOTIFICATION SERVICE

## Requirements

- Email
- SMS
- Push notifications
- Retry failed delivery
- User preferences
- Delivery status
- Rate limits

## Architecture

Application
  |
Notification API
  |
Queue
  |
Workers
  |
  +---- Email Provider
  +---- SMS Provider
  +---- Push Provider

## Important Concepts

- Template rendering
- Provider fallback
- Retry with backoff
- Dead-letter queue
- Deduplication
- User opt-out
- Delivery tracking
- Provider rate limits

Notification failure-এর কারণে core order creation fail করানো উচিত কি না, তা requirements অনুযায়ী নির্ধারণ করতে হবে।

---

# 38. SYSTEM DESIGN CASE STUDY: NEWS FEED

## Requirements

- Follow users
- Publish posts
- Display personalized feed
- Pagination
- Ranking
- Privacy checks

## Two Strategies

### Pull Model

Feed request-এর সময় followed users-এর posts query করা হয়।

Good for:
- Smaller accounts
- Lower write overhead

Potential problem:
- Read-time query expensive হতে পারে

### Push Model

নতুন post publish হলে followers-এর feed materialize করা হয়।

Good for:
- Fast feed reads

Potential problem:
- Celebrities with millions of followers can create enormous fan-out

## Hybrid Model

Most users-এর জন্য push, very high-follower accounts-এর জন্য pull বা hybrid retrieval।

## Architecture

Post Service
  |
Event Queue
  |
Feed Fan-out Workers
  |
Feed Store
  |
Feed API
  |
Client

Feed design-এ ranking, deletion, privacy, duplicate posts এবং pagination বিবেচনা করতে হবে।

---

# 39. SYSTEM DESIGN CASE STUDY: VIDEO STREAMING

## Requirements

- Video upload
- Transcoding
- Multiple resolutions
- Streaming
- Captions
- Access control
- Analytics

## Architecture

Uploader
  |
Object Storage
  |
Processing Queue
  |
Transcoding Workers
  |
Video Segments + Manifests
  |
CDN
  |
Viewer

## Key Concepts

- Adaptive bitrate streaming
- HLS / MPEG-DASH
- Transcoding
- Segment storage
- CDN cache
- Signed URLs or cookies
- Processing status

Large media files সাধারণত application database-এ রাখা হয় না।

---

# 40. SYSTEM DESIGN CASE STUDY: RIDE-SHARING

## Requirements

- Driver location updates
- Passenger ride request
- Nearby driver search
- Matching
- Ride status
- ETA
- Payments

## Architecture

Mobile Apps
  |
API Gateway
  |
Ride Service
  |
  +---- Location Service
  |
  +---- Matching Service
  |
  +---- Geospatial Store
  |
  +---- Queue
  |
  +---- Notification Service

## Challenges

- High-frequency location updates
- Geospatial queries
- Concurrent driver assignment
- Matching latency
- Location freshness
- Ride state transitions
- Network disconnection

একজন driver যেন একই সময়ে দুইটি ride-এ assign না হয়, সে জন্য concurrency control দরকার।

---

# 41. SYSTEM DESIGN CASE STUDY: TICKET BOOKING

## Requirements

- Search events
- Show seat availability
- Reserve seats
- Payment
- Confirm booking
- Handle cancellation

## Main Challenge

একই seat অনেক user একসঙ্গে বুক করতে চাইতে পারে।

## Possible Flow

1. User selects seat
2. Server creates temporary reservation
3. Reservation has expiry time
4. Payment is processed
5. Successful payment-এর পর booking confirm
6. Expired reservation release

## Important Design Choices

- Database transactions
- Unique constraints
- Row locking
- Optimistic concurrency
- Reservation TTL
- Idempotency
- Payment reconciliation
- Queue-based expiration

Cache availability দেখাতে সাহায্য করতে পারে, কিন্তু cache alone booking-এর authoritative source হওয়া উচিত নয়।

---

# 42. SYSTEM DESIGN INTERVIEW FRAMEWORK

একটি system design interview-এ এই sequence follow করো।

## Step 1: Clarify Requirements

Ask:
- Core features কী?
- User count কত?
- Traffic pattern কী?
- Read/write ratio কী?
- Availability target কী?
- Strong consistency কোথায় দরকার?

## Step 2: Estimate Scale

Estimate:
- Daily active users
- Requests per second
- Peak RPS
- Storage per day
- Bandwidth
- Read/write ratio

Assumptions clearly state করবে।

## Step 3: Define APIs

Example:

POST /api/orders/
GET /api/orders/{id}/
GET /api/products/

## Step 4: Design Data Model

Define:
- Entities
- Relationships
- Primary keys
- Unique constraints
- Indexes

## Step 5: Draw High-Level Architecture

Client
  |
Load Balancer
  |
Application
  |
  +---- Database
  +---- Cache
  +---- Queue
  +---- Object Storage

## Step 6: Explain Main Data Flow

একটি write request ও একটি read request step-by-step explain করো।

## Step 7: Identify Bottlenecks

Potential bottlenecks:
- Database
- Cache
- Network
- Third-party APIs
- Worker queue
- CPU
- Storage

## Step 8: Scale the System

Potential solutions:
- Indexing
- Caching
- Read replicas
- Horizontal scaling
- Queue-based processing
- Partitioning
- CDN

## Step 9: Discuss Failure Modes

Ask:
- Database unavailable হলে?
- Queue consumer fail করলে?
- Duplicate request এলে?
- Cache stale হলে?
- Third-party payment timeout হলে?

## Step 10: Discuss Trade-offs

প্রতিটি decision-এর benefits, costs এবং alternatives ব্যাখ্যা করো।

---

# 43. COMMON SYSTEM DESIGN INTERVIEW QUESTIONS

## Q1. What is System Design?

System components, data flow, interactions এবং operational requirements-এর architecture পরিকল্পনা।

## Q2. What is scalability?

Workload বাড়লে system-এর capacity বাড়ানোর ক্ষমতা।

## Q3. Vertical vs horizontal scaling?

Vertical: একটি machine-এর resources বাড়ানো।

Horizontal: আরও instances যোগ করা।

## Q4. What is caching?

Frequently accessed data faster storage-এ রেখে latency ও backend load কমানো।

## Q5. What is a CDN?

Distributed edge network থেকে content deliver করার infrastructure।

## Q6. What is a load balancer?

Traffic একাধিক backend instance-এ distribute করে।

## Q7. What is replication?

একাধিক nodes-এ data copies রাখা।

## Q8. What is sharding?

Data-কে partitions-এ ভাগ করে আলাদা nodes-এ রাখা।

## Q9. What is a database index?

Query-তে matching records দ্রুত locate করার data structure।

## Q10. What is a message queue?

Producer ও consumer-এর মধ্যে asynchronous messages রাখার mechanism।

## Q11. What is eventual consistency?

Updates চলা বন্ধ হলে replicas eventually converge করতে পারে।

## Q12. What is CAP Theorem?

Distributed data system-এ network partition ঘটলে consistency ও availability behavior-এর trade-off নিয়ে theorem।

## Q13. What is a microservice?

একটি bounded business capability-এর জন্য independently deployable service।

## Q14. What is idempotency?

একই operation repeat করলেও intended final effect একই থাকা।

## Q15. What is rate limiting?

নির্দিষ্ট সময়ে request-এর সংখ্যা সীমিত করা।

## Q16. What is a circuit breaker?

Repeated failures-এর সময় remote dependency-তে requests সাময়িকভাবে বন্ধ রাখা।

## Q17. What is a cache stampede?

একটি cache entry expire হলে অনেক requests একসঙ্গে backend-এ চলে যাওয়া।

## Q18. What is a database connection pool?

Database connections reuse করার mechanism, যা connection overhead ও resource use নিয়ন্ত্রণ করে।

## Q19. What is a hot key?

একটি key-তে disproportionate traffic জমা হওয়া।

## Q20. What is backpressure?

Downstream system overload হলে upstream workload control বা slow down করা।

## Q21. What is a dead-letter queue?

Repeatedly unprocessable messages আলাদা করে রাখা queue।

## Q22. What is observability?

Logs, metrics, traces এবং related signals থেকে system behavior বোঝার ক্ষমতা।

## Q23. What is a single point of failure?

একটি component fail করলেই critical system functionality unavailable হয়ে যায়।

## Q24. What is a distributed transaction?

একাধিক resource বা service-এর state পরিবর্তনের transaction; implementation ও guarantee technology অনুযায়ী ভিন্ন হয়।

## Q25. What is the Saga pattern?

Distributed business transaction-কে local transactions ও compensating actions-এর sequence হিসেবে পরিচালনা করা।

## Q26. What is the transactional outbox pattern?

Business data ও event record একই database transaction-এ write করে reliable event publication-এর সুবিধা দেওয়া।

## Q27. What is p99 latency?

99% requests যে latency-এর মধ্যে complete হয়, সেই percentile value।

## Q28. What is graceful degradation?

Optional functionality fail হলেও core functionality চালু রাখা।

## Q29. What is RPO?

Recovery Point Objective: কতটা data loss গ্রহণযোগ্য।

## Q30. What is RTO?

Recovery Time Objective: কত সময়ের মধ্যে recovery করতে হবে।

---

# 44. COMMON SYSTEM DESIGN MISTAKES

1. Requirements না বুঝেই architecture শুরু করা।
2. Traffic estimate না করা।
3. অপ্রয়োজনীয় microservices তৈরি করা।
4. সব data Redis-এ রাখার চেষ্টা করা।
5. Database indexing উপেক্ষা করা।
6. Cache invalidation strategy না রাখা।
7. Timeout ও retry না দেওয়া।
8. Retry loop-এর limit না রাখা।
9. Idempotency উপেক্ষা করা।
10. Authentication ও authorization গুলিয়ে ফেলা।
11. Single point of failure তৈরি করা।
12. Backup restore test না করা।
13. Monitoring ছাড়া production চালানো।
14. Queue consumer failure উপেক্ষা করা।
15. Payment flow-এ duplicate operation ঠেকানোর ব্যবস্থা না রাখা।
16. শুধু average latency দেখা।
17. Data consistency requirements define না করা।
18. Trade-offs explain না করা।
19. Cost বিবেচনা না করা।
20. Measurement ছাড়া premature optimization করা।

---

# 45. PYTHON AND DJANGO PRACTICAL EXAMPLES

## 45.1 Simple Django Model

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
```

## 45.2 Indexing

```python
class Meta:
    indexes = [
        models.Index(fields=["created_at"]),
    ]
```

এটি model class-এর ভেতরে রাখতে হবে। Migration তৈরি ও apply করতে হবে।

## 45.3 Pagination

```python
from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
```

## 45.4 Query Optimization

```python
products = Product.objects.all().only(
    "id",
    "name",
    "price",
)
```

`only()` ব্যবহার করলে পরে deferred fields access করে অতিরিক্ত queries তৈরি হচ্ছে কি না দেখো।

## 45.5 Atomic Database Operation

```python
from django.db import transaction

with transaction.atomic():
    # Related database writes go here.
    pass
```

## 45.6 Background Task

```python
from celery import shared_task

@shared_task
def generate_report(report_id):
    # Load report data and generate the report.
    pass
```

## 45.7 Security Checklist

- Environment variables for secrets
- `DEBUG=False` in production
- HTTPS
- CSRF protection
- Proper permission checks
- Database constraints
- Input validation
- Rate limiting
- Audit logs
- Backup and restore tests

---

# 46. BEGINNER-TO-ADVANCED PROJECT ROADMAP

## Project 1: URL Shortener

Learn:
- REST API
- PostgreSQL
- Unique constraints
- Redis cache
- Redirects
- Rate limiting

## Project 2: Blog API

Learn:
- User authentication
- Permissions
- Database relationships
- Pagination
- Query optimization

## Project 3: File Upload Service

Learn:
- Object storage
- Pre-signed URLs
- File metadata
- Access control
- Background processing

## Project 4: Notification Service

Learn:
- Celery
- Redis or RabbitMQ
- Retries
- Dead-letter queue
- Idempotency

## Project 5: E-commerce Backend

Learn:
- Product catalog
- Cart
- Orders
- Inventory
- Payment state machine
- Database transactions

## Project 6: Real-Time Chat

Learn:
- WebSockets
- Message persistence
- Online presence
- Delivery status
- Queues

## Project 7: News Feed

Learn:
- Feed generation
- Fan-out
- Caching
- Ranking
- Pagination

## Project 8: Video Platform

Learn:
- Object storage
- Transcoding workers
- CDN
- Streaming protocols
- Background processing

---

# 47. COMPLETE 12-WEEK STUDY PLAN

## Week 1: Foundations

- System Design introduction
- HLD vs LLD
- Requirements
- Client-server
- HTTP and REST

Practice:
Draw a simple Django API architecture.

## Week 2: Networking and Estimation

- DNS
- TCP/UDP
- TLS
- Latency
- Throughput
- RPS
- Capacity estimation

Practice:
Estimate traffic for a blog with 100,000 daily users.

## Week 3: Databases

- SQL vs NoSQL
- Schema design
- Relationships
- Normalization
- Constraints
- ACID

Practice:
Design an order database.

## Week 4: Performance

- Indexes
- Query optimization
- N+1 queries
- Connection pooling
- Redis
- Cache invalidation

Practice:
Optimize a slow Django endpoint.

## Week 5: Scaling

- Vertical and horizontal scaling
- Load balancers
- Stateless services
- Replication
- Sharding

Practice:
Scale a product API for increased read traffic.

## Week 6: Asynchronous Processing

- Message queues
- Celery
- Background workers
- Retry strategies
- Idempotency
- Dead-letter queues

Practice:
Build a notification worker.

## Week 7: Distributed Systems

- CAP
- Consistency
- Network failures
- Timeouts
- Circuit breakers
- Backpressure

Practice:
Design a resilient order processing workflow.

## Week 8: Reliability and Security

- High availability
- Fault tolerance
- Backups
- RPO and RTO
- Authentication
- Authorization
- Rate limiting

Practice:
Threat-model a Django REST API.

## Week 9: Architecture Patterns

- Monolith
- Modular monolith
- Microservices
- Event-driven systems
- API gateway
- Transactional outbox

Practice:
Draw an e-commerce architecture.

## Week 10: Core Case Studies

- URL Shortener
- File Upload
- Notification Service
- Chat Application

Practice:
Explain every design in 30 minutes.

## Week 11: Advanced Case Studies

- News Feed
- Video Streaming
- Ride-Sharing
- Ticket Booking

Practice:
Estimate capacity and explain failure handling.

## Week 12: Interview Preparation

- Requirement clarification
- Capacity estimation
- API design
- Data modeling
- Architecture diagrams
- Bottlenecks
- Trade-offs
- Mock interviews

Practice:
Complete two timed system design interviews.

---

# 48. FINAL SYSTEM DESIGN CHECKLIST

Before finalizing any design, check:

## Requirements
- [ ] Functional requirements
- [ ] Non-functional requirements
- [ ] Expected scale
- [ ] Constraints

## APIs
- [ ] Endpoints
- [ ] Authentication
- [ ] Authorization
- [ ] Pagination
- [ ] Error responses
- [ ] Rate limiting

## Data
- [ ] Database selection
- [ ] Schema
- [ ] Indexes
- [ ] Constraints
- [ ] Transactions
- [ ] Retention policy

## Performance
- [ ] Caching
- [ ] Query optimization
- [ ] Load balancing
- [ ] CDN where appropriate
- [ ] Background jobs

## Scalability
- [ ] Horizontal scaling
- [ ] Database scaling
- [ ] Queue capacity
- [ ] Hot keys
- [ ] Bottlenecks

## Reliability
- [ ] Timeouts
- [ ] Retries
- [ ] Idempotency
- [ ] Failover
- [ ] Backups
- [ ] Restore tests

## Security
- [ ] HTTPS
- [ ] Secret management
- [ ] Permissions
- [ ] Input validation
- [ ] Audit logs
- [ ] Data protection

## Operations
- [ ] Logs
- [ ] Metrics
- [ ] Traces
- [ ] Alerts
- [ ] Deployment strategy
- [ ] Disaster recovery

## Trade-offs
- [ ] Alternatives
- [ ] Cost
- [ ] Complexity
- [ ] Performance
- [ ] Consistency
- [ ] Maintainability

---

# 49. GLOSSARY

API: Application Programming Interface
ACID: Atomicity, Consistency, Isolation, Durability
CDN: Content Delivery Network
CAP: Consistency, Availability, Partition Tolerance
CRUD: Create, Read, Update, Delete
DNS: Domain Name System
HLD: High-Level Design
HTTP: Hypertext Transfer Protocol
HTTPS: HTTP over TLS
LLD: Low-Level Design
MTTR: Mean Time to Recovery
NoSQL: Non-relational database category
RPO: Recovery Point Objective
RPS: Requests Per Second
RTO: Recovery Time Objective
SQL: Structured Query Language
SLA: Service Level Agreement
SLO: Service Level Objective
SLI: Service Level Indicator
TCP: Transmission Control Protocol
TLS: Transport Layer Security
UDP: User Datagram Protocol
WAL: Write-Ahead Log

---

# 50. LEARNING RESOURCES

## Books

1. Designing Data-Intensive Applications — Martin Kleppmann
2. System Design Interview — Alex Xu, Volumes 1 and 2
3. Fundamentals of Software Architecture — Mark Richards and Neal Ford

## Official Documentation

- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- PostgreSQL: https://www.postgresql.org/docs/
- Redis: https://redis.io/docs/
- Celery: https://docs.celeryq.dev/
- Docker: https://docs.docker.com/
- Kubernetes: https://kubernetes.io/docs/
- OpenTelemetry: https://opentelemetry.io/docs/

## How to Study

প্রতিটি topic-এর জন্য:
1. Concept বোঝো।
2. নিজের ভাষায় definition লেখো।
3. Diagram আঁকো।
4. Python/Django example implement করো।
5. Failure scenario চিন্তা করো।
6. Alternative design compare করো।
7. Interview question practice করো।
8. Project-এ apply করো।

---

# FINAL ADVICE

System Design মুখস্থ করার বিষয় নয়। এটি requirements, constraints এবং trade-offs বুঝে architecture তৈরি করার skill।

Beginner হিসেবে:
- HTTP
- REST API
- PostgreSQL
- Database indexing
- Redis
- Load balancing
- Background jobs

এই fundamentals ভালোভাবে শিখে তারপর distributed systems ও advanced architecture-এ যাও।

Python/Django backend developer হিসেবে প্রথমে একটি well-structured Django application তৈরি করো। এরপর Redis, Celery, PostgreSQL optimization, object storage, monitoring এবং deployment যোগ করো।

সবশেষে প্রতিটি project-এর জন্য নিজেকে প্রশ্ন করো:

1. Traffic 10 গুণ হলে কী হবে?
2. Database unavailable হলে কী হবে?
3. একই request দুইবার এলে কী হবে?
4. Cache stale হলে কী হবে?
5. Third-party API timeout হলে কী হবে?
6. Data backup ও recovery কীভাবে হবে?
7. কোন component bottleneck তৈরি করবে?
8. আরও simple এবং কম খরচের design সম্ভব কি?

এই প্রশ্নগুলোর উত্তর দিতে পারলে তোমার System Design skill ধাপে ধাপে Beginner থেকে Advanced পর্যায়ে উন্নত হবে।
