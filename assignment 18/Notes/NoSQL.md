# NoSQL Database — Complete Notes (বাংলায়)

## Table of Contents

1. [What is NoSQL?](#1-what-is-nosql)
2. [SQL vs NoSQL](#2-sql-vs-nosql)
3. [Types of NoSQL Databases](#3-types-of-nosql-databases)
4. [MongoDB Basics](#4-mongodb-basics)
5. [Important NoSQL Concepts](#5-important-nosql-concepts)
6. [Sharding and Replication](#6-sharding-and-replication)
7. [CAP Theorem](#7-cap-theorem)
8. [When to Use NoSQL](#8-when-to-use-nosql)
9. [NoSQL with Django](#9-nosql-with-django)
10. [Interview Questions](#10-interview-questions)
11. [Learning Roadmap](#11-learning-roadmap)

---

## 1. What is NoSQL?

**NoSQL** means "Not Only SQL". It refers to database systems that use data models beyond the traditional relational table model.

NoSQL databases are useful for flexible data structures, distributed systems, large-scale applications, and particular high-throughput workloads.

### Examples

- MongoDB
- Redis
- Apache Cassandra
- Neo4j
- Amazon DynamoDB
- Apache HBase

### Key Features

- Flexible data models
- Horizontal scaling support in many systems
- Distributed data storage
- Different consistency models
- Efficient access for specific query patterns

> NoSQL is not always better than SQL. The best choice depends on your application's requirements.

---

## 2. SQL vs NoSQL

| Feature | SQL | NoSQL |
|---|---|---|
| Data model | Tables, rows, columns | Documents, key-value, graph, wide-column |
| Schema | Usually predefined | Often flexible |
| Query language | SQL | Database-specific APIs or query languages |
| Relationships | JOINs and foreign keys | Embedding, references, or database-specific relationships |
| Scaling | Vertical and horizontal options | Horizontal scaling is common in distributed systems |
| Transactions | Widely supported | Support varies by database |
| Examples | PostgreSQL, MySQL | MongoDB, Redis, Cassandra |

### When to Choose SQL

- Complex relationships between entities
- Financial and transactional applications
- Strong relational integrity
- Complex reporting and JOIN queries

### When to Choose NoSQL

- Flexible or nested data
- Large distributed workloads
- Fast cache and session access
- Graph-based relationships
- Particular high-volume event or time-series workloads

---

## 3. Types of NoSQL Databases

### 3.1 Document Database

Stores data as documents, commonly using JSON-like structures.

**Examples:** MongoDB, Couchbase

**Use cases:**
- E-commerce products
- User profiles
- Content management systems
- Product catalogs

Example document:

```json
{
  "_id": "user_101",
  "name": "Omar",
  "email": "omar@example.com",
  "skills": ["Python", "Django"],
  "address": {
    "city": "Bogura",
    "country": "Bangladesh"
  }
}
```

**Advantages:**
- Flexible schema
- Supports nested objects and arrays
- Natural fit for JSON-like application data

### 3.2 Key-Value Database

Stores values associated with unique keys.

**Examples:** Redis, Amazon DynamoDB

**Use cases:**
- Caching
- Session storage
- Counters
- Rate limiting

Example:

```text
Key: user:101:name
Value: Omar
```

Redis example:

```python
import redis

client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)

client.set("user:101:name", "Omar")
name = client.get("user:101:name")

print(name)
```

### 3.3 Wide-Column Database

Organizes data into rows and column families, with designs suited to distributed workloads.

**Examples:** Apache Cassandra, Apache HBase

**Use cases:**
- Large-scale event logs
- Distributed telemetry
- High-volume time-series workloads

### 3.4 Graph Database

Represents data as nodes and relationships.

**Example:** Neo4j

**Use cases:**
- Social networks
- Recommendation systems
- Fraud detection
- Relationship analysis

Example:

```text
(Omar) ---- FRIEND_OF ----> (Rahim)
  |
  +-------- FOLLOWS -------> (Karim)
```

Graph databases are particularly useful when queries frequently traverse complex relationships.

---

## 4. MongoDB Basics

MongoDB is a document-oriented NoSQL database.

### Basic Terminology

| MongoDB | Relational Database |
|---|---|
| Database | Database |
| Collection | Table |
| Document | Row or record |
| Field | Column-like attribute |
| Index | Index |

### CRUD Operations

CRUD means Create, Read, Update, and Delete.

#### Create

```javascript
db.users.insertOne({
  name: "Omar",
  age: 25,
  skills: ["Python", "Django"]
});
```

#### Read

```javascript
db.users.find({ name: "Omar" });

db.users.findOne({ name: "Omar" });
```

#### Update

```javascript
db.users.updateOne(
  { name: "Omar" },
  { $set: { age: 26 } }
);
```

#### Delete

```javascript
db.users.deleteOne({ name: "Omar" });
```

### Filtering and Sorting

```javascript
// Find users older than 20
db.users.find({ age: { $gt: 20 } });

// Sort by age in descending order
db.users.find().sort({ age: -1 });

// Return only selected fields
db.users.find(
  {},
  { name: 1, age: 1, _id: 0 }
);
```

### Indexing

Indexes can speed up queries that match the indexed fields, at the cost of additional storage and write overhead.

```javascript
db.users.createIndex({ email: 1 });
```

For a unique email:

```javascript
db.users.createIndex(
  { email: 1 },
  { unique: true }
);
```

---

## 5. Important NoSQL Concepts

### 5.1 Flexible Schema

Documents in the same collection can have different fields, depending on the database's validation rules.

```json
{
  "name": "Omar",
  "age": 25
}
```

```json
{
  "name": "Rahim",
  "skills": ["Python", "SQL"]
}
```

Flexible schema does not mean data validation is unnecessary. Production applications should still enforce appropriate data rules.

### 5.2 Horizontal Scaling

Horizontal scaling means adding more machines or nodes to distribute storage and workload.

### 5.3 Denormalization

Denormalization means storing related data together to simplify or speed up common reads.

For example, an order document may contain a snapshot of the purchased product's name and price.

**Trade-off:** duplicated data can become harder to keep consistent when the original information changes.

### 5.4 Embedding vs Referencing

**Embedding:** Store related data inside one document.

```json
{
  "name": "Omar",
  "address": {
    "city": "Bogura"
  }
}
```

Best when related data is usually read together and has a suitable size and lifecycle.

**Referencing:** Store an identifier pointing to another document.

```json
{
  "order_id": "order_101",
  "customer_id": "user_101"
}
```

Best when data is shared across many records or should be managed independently.

### 5.5 Consistency

Consistency describes what data a read is allowed to observe after writes.

Depending on the database and configuration, a system may provide strong consistency for some operations and weaker or eventual consistency for others.

### 5.6 Eventual Consistency

With eventual consistency, replicas may temporarily return different values, but they are expected to converge if updates stop and the system recovers normally.

This can be useful when availability and distributed operation are important, but it is not suitable for every workload.

### 5.7 Transactions

Transactions group operations so they succeed or fail according to the database's transaction guarantees.

Some NoSQL databases support multi-document or distributed transactions. Others have more limited transaction models. Always check the database's actual guarantees.

---

## 6. Sharding and Replication

### 6.1 Sharding

Sharding partitions a dataset across multiple nodes.

```text
             Application
                  |
             Database Cluster
             /      |      \
         Shard 1  Shard 2  Shard 3
```

Each shard stores a portion of the data.

**Benefits:**
- Distributes storage
- Can increase throughput
- Supports growth beyond one machine's capacity

**Challenges:**
- Choosing an appropriate shard key
- Data rebalancing
- Cross-shard queries
- Uneven data distribution

### 6.2 Replication

Replication keeps multiple copies of data on different nodes.

```text
          Primary Node
          /          \
   Replica Node 1   Replica Node 2
```

**Benefits:**
- Can improve availability
- Supports failover
- Can improve read capacity in some configurations

**Challenges:**
- Replication lag
- Failover management
- Consistency considerations

### Sharding vs Replication

| Feature | Sharding | Replication |
|---|---|---|
| Main purpose | Partition data | Copy data |
| Storage | Each shard holds a portion | Replicas hold copies |
| Scaling benefit | Distributes storage and workload | Can improve availability and read capacity |
| Main challenge | Partition design | Synchronization and failover |

A database system may use sharding and replication together.

---

## 7. CAP Theorem

CAP describes a trade-off in distributed systems during a network partition.

### C — Consistency

A read sees the latest successful write according to the system's consistency guarantee.

### A — Availability

Every request to a non-failing node receives a non-error response.

### P — Partition Tolerance

The system continues operating despite communication failures between parts of the distributed system.

### Key Point

When a network partition occurs, a distributed system cannot guarantee both full availability and strong consistency for every operation simultaneously.

This does not mean that a database is always exclusively "CP" or "AP" in every situation. Actual behavior depends on the operation, configuration, and failure conditions.

---

## 8. When to Use NoSQL

Consider NoSQL when:

- Data is naturally document-based or graph-based.
- The data model changes frequently.
- Workload needs distribution across many nodes.
- Fast key-based access or caching is important.
- Application query patterns fit the chosen database well.

Consider SQL when:

- Data has many relational constraints.
- Complex JOIN queries are central.
- Strong transactional guarantees are required.
- Relational reporting and data integrity are priorities.

**Best practice:** Choose a database based on data access patterns and correctness requirements, not popularity alone.

---

## 9. NoSQL with Django

For Python/Django backend development, two useful technologies to learn are:

- **MongoDB:** Document storage.
- **Redis:** Caching, counters, sessions, and other in-memory data structures.

A common architecture is to keep the main relational data in PostgreSQL and use Redis to cache frequently requested results.

### Configure Redis Cache

Install the required package:

```bash
pip install django-redis
```

Configure `settings.py`:

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
```

Ensure Redis is running and that the connection settings match your environment.

### Cache Data in a Django View

```python
from django.core.cache import cache
from django.http import JsonResponse

def product_list(request):
    products = cache.get("products")

    if products is None:
        # Replace this with a real database query.
        products = [
            {"id": 1, "name": "Keyboard"},
            {"id": 2, "name": "Mouse"},
        ]

        cache.set("products", products, timeout=300)

    return JsonResponse({"products": products})
```

Here, the cached result expires after 300 seconds.

**Production considerations:**
- Invalidate or update the cache when source data changes.
- Use appropriate cache keys and timeouts.
- Avoid caching user-specific data under a shared key.
- Handle Redis failures appropriately.
- Monitor cache hit rate and database load.

### Example Architecture

```text
Client
  |
Django REST Framework API
  |
  +------ Redis Cache
  |
  +------ PostgreSQL Database
```

Redis reduces repeated database reads when cached data can be reused. PostgreSQL remains the source of truth for the example architecture.

---

## 10. Interview Questions

### Beginner

1. What is NoSQL?
2. What does "Not Only SQL" mean?
3. What are the four major types of NoSQL databases?
4. What is the difference between SQL and NoSQL?
5. What is a MongoDB collection?
6. What is a document database?
7. What is Redis commonly used for?

### Intermediate

8. What is the difference between embedding and referencing?
9. What is denormalization?
10. What is indexing, and what are its trade-offs?
11. What is the difference between sharding and replication?
12. What is eventual consistency?
13. What is the CAP theorem?
14. How would you cache a Django API response using Redis?

### Advanced

15. How would you choose a shard key?
16. How can a poor shard key affect performance?
17. How would you handle cache invalidation?
18. How would you maintain data consistency across services?
19. When would you choose PostgreSQL instead of MongoDB?
20. How would you design a high-throughput event storage system?

### Short Answers

**Q: Is NoSQL always faster than SQL?**

No. Performance depends on query patterns, data modeling, indexing, hardware, and workload.

**Q: What is the difference between sharding and replication?**

Sharding splits data into partitions. Replication maintains copies of data.

**Q: Why use Redis with Django?**

Redis can cache frequently accessed results and reduce repeated database work.

**Q: Is MongoDB schema-less?**

MongoDB has a flexible document model, but production applications should still validate their data.

**Q: Can NoSQL databases support transactions?**

Yes, some do. The scope and guarantees vary by database.

---

## 11. Learning Roadmap

### Week 1 — Fundamentals

- SQL vs NoSQL
- Types of NoSQL databases
- Use cases and trade-offs
- CAP theorem basics

### Week 2 — MongoDB

- Install and connect MongoDB
- CRUD operations
- Filtering and sorting
- Indexing
- Embedding vs referencing
- Data validation

### Week 3 — Redis

- Strings, hashes, lists, and sets
- Key expiration and TTL
- Caching API responses
- Cache invalidation
- Counters and rate limiting

### Week 4 — System Design

- Sharding and replication
- Consistency models
- Database selection
- Cache design
- Failure handling
- Monitoring and performance testing

### Practice Project

Build a **Product API using Django REST Framework**.

Requirements:

1. Create product CRUD endpoints.
2. Store product data in PostgreSQL.
3. Use Redis to cache the product-list endpoint.
4. Implement cache expiration and invalidation.
5. Add pagination and filtering.
6. Measure API response time with and without caching.
7. Document the architecture in a README.

---

## Final Summary

Remember these concepts:

- **MongoDB:** Document database.
- **Redis:** In-memory data structure store, commonly used for caching.
- **Cassandra:** Wide-column distributed database.
- **Neo4j:** Graph database.
- **Sharding:** Splits data across nodes.
- **Replication:** Maintains copies of data.
- **Indexing:** Can speed up queries but adds storage and write overhead.
- **CAP theorem:** Explains consistency and availability trade-offs during network partitions.
- **Database selection:** Depends on data structure, query patterns, consistency, transactions, and scale.
