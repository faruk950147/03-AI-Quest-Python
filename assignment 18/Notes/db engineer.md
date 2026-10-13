# Database Engineer Roadmap with Complete Notes
## Beginner to Advanced — Bangla + English

# PART 1: DATABASE FUNDAMENTALS

## 1. What is Data?

**Definition:** Data হলো raw facts and figures যা processing-এর আগে অর্থপূর্ণ তথ্য নাও হতে পারে।

Example:
- Name: Faruk
- Age: 25
- Department: CSE

## 2. What is a Database?

**Definition:** A database is an organized collection of related data that can be stored, accessed, managed, and updated efficiently.

Example:
A university database stores students, teachers, courses, and results.

## 3. What is DBMS?

**Definition:** DBMS (Database Management System) হলো এমন software যার মাধ্যমে database তৈরি, সংরক্ষণ, query, update এবং manage করা যায়।

Examples:
- PostgreSQL
- MySQL
- SQLite
- Oracle Database
- Microsoft SQL Server

## 4. What is RDBMS?

**Definition:** RDBMS (Relational Database Management System) হলো এমন DBMS যেখানে data relational tables-এর মাধ্যমে সংরক্ষণ করা হয়।

Example:

Students Table:

| student_id | name | department |
|---|---|---|
| 1 | Faruk | CSE |
| 2 | Rahim | EEE |

## 5. DBMS vs RDBMS

| DBMS | RDBMS |
|---|---|
| General database management system | Relational database management system |
| Data model বিভিন্ন রকম হতে পারে | Relational tables ব্যবহার করে |
| সব DBMS relational নয় | RDBMS হলো relational DBMS |
| Example: document database software-ও DBMS হতে পারে | PostgreSQL, MySQL |

## 6. Database Components

- Table: Rows and columns-এর মাধ্যমে data রাখে।
- Row: একটি record।
- Column: একটি attribute বা field।
- Schema: Database objects-এর structure।
- Query: Database-কে দেওয়া operation বা request।
- Constraint: Data validity বজায় রাখার rule।
- Index: নির্দিষ্ট data দ্রুত খুঁজতে সাহায্য করে এমন structure।

## 7. Keys in Database

### Primary Key

একটি table-এর প্রতিটি row-কে uniquely identify করে।

Properties:
- Unique হতে হবে।
- NULL হতে পারবে না।
- একটি table-এ একটি primary-key constraint থাকতে পারে; সেটি এক বা একাধিক column নিয়ে তৈরি হতে পারে।

```sql
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);
```

### Foreign Key

একটি table-এর data-কে অন্য table-এর referenced key-এর সঙ্গে সম্পর্কিত করে।

```sql
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id)
);
```

### Other Keys

- Candidate Key: সম্ভাব্য minimal unique key।
- Super Key: যে column set একটি row uniquely identify করে।
- Composite Key: একাধিক column নিয়ে তৈরি key।
- Alternate Key: Candidate key-গুলোর মধ্যে নির্বাচিত primary key ছাড়া অন্য key।
- Unique Constraint: Duplicate value প্রতিরোধ করে; NULL handling database অনুযায়ী ভিন্ন হতে পারে।

## 8. Database Relationships

### One-to-One
একটি record-এর সঙ্গে অন্য table-এর সর্বোচ্চ একটি record সম্পর্কিত।

Example: Person → Passport

### One-to-Many
একটি record-এর সঙ্গে অন্য table-এর একাধিক record সম্পর্কিত।

Example: Department → Students

### Many-to-Many
দুই table-এর একাধিক record পরস্পরের সঙ্গে সম্পর্কিত।

Example: Students ↔ Courses

এক্ষেত্রে সাধারণত একটি junction table ব্যবহার করা হয়।

## 9. Normalization

**Definition:** Normalization হলো relational database এমনভাবে design করা, যাতে unnecessary duplication এবং insertion, update, deletion anomalies কমে।

### 1NF
- প্রতিটি cell-এ atomic value থাকবে।
- Repeating groups থাকবে না।

### 2NF
- Table 1NF-এ থাকবে।
- কোনো non-key attribute composite candidate key-এর proper subset-এর ওপর নির্ভর করবে না।

### 3NF
- Table 2NF-এ থাকবে।
- Non-key attributes-এর মধ্যে অনুপযুক্ত transitive dependency থাকবে না।

### BCNF
প্রতিটি non-trivial functional dependency-তে determinant একটি superkey হতে হবে।

## 10. ER Diagram

ER Diagram হলো database-এর entities, attributes এবং relationships-এর visual representation।

Example:
- Student
- Course
- Teacher
- Enrollment

Practice:
University database-এর ER diagram তৈরি করো।

---

# PART 2: SQL COMPLETE NOTES

## 11. What is SQL?

**Definition:** SQL (Structured Query Language) হলো relational database-এ data query ও manipulate এবং database objects define করার standard language।

## 12. Categories of SQL

### DQL — Data Query Language
- SELECT

### DML — Data Manipulation Language
- INSERT
- UPDATE
- DELETE

### DDL — Data Definition Language
- CREATE
- ALTER
- DROP
- TRUNCATE

### DCL — Data Control Language
- GRANT
- REVOKE

### Transaction Control
- BEGIN
- COMMIT
- ROLLBACK
- SAVEPOINT

Note: SQL command classification কিছু textbook ও database system-এ ভিন্নভাবে উপস্থাপিত হতে পারে।

## 13. SELECT Statement

```sql
SELECT name, email
FROM students;
```

Explanation:
- SELECT নির্দিষ্ট columns বেছে নেয়।
- FROM data source নির্ধারণ করে।

## 14. WHERE Clause

```sql
SELECT *
FROM students
WHERE department = 'CSE';
```

WHERE condition অনুযায়ী rows filter করে।

## 15. ORDER BY

```sql
SELECT *
FROM students
ORDER BY name ASC;
```

- ASC: Ascending order
- DESC: Descending order

## 16. INSERT

```sql
INSERT INTO students (student_id, name)
VALUES (1, 'Faruk');
```

নতুন record যোগ করে।

## 17. UPDATE

```sql
UPDATE students
SET name = 'Omar Faruk'
WHERE student_id = 1;
```

সতর্কতা: WHERE clause ছাড়া UPDATE করলে সব rows পরিবর্তিত হতে পারে।

## 18. DELETE

```sql
DELETE FROM students
WHERE student_id = 1;
```

WHERE clause ছাড়া DELETE করলে সব rows মুছে যেতে পারে।

## 19. Aggregate Functions

- COUNT(): Number of rows বা non-NULL values গণনা।
- SUM(): মোট যোগফল।
- AVG(): Average।
- MIN(): সর্বনিম্ন value।
- MAX(): সর্বোচ্চ value।

```sql
SELECT department, COUNT(*) AS total_students
FROM students
GROUP BY department;
```

## 20. GROUP BY vs HAVING

GROUP BY rows-কে group করে।

HAVING grouped results-এর ওপর condition প্রয়োগ করে।

```sql
SELECT department, COUNT(*) AS total
FROM students
GROUP BY department
HAVING COUNT(*) > 5;
```

## 21. SQL JOIN

### INNER JOIN
শুধু matching rows ফেরত দেয়।

```sql
SELECT s.name, e.course_id
FROM students AS s
INNER JOIN enrollments AS e
ON s.student_id = e.student_id;
```

### LEFT JOIN
Left table-এর সব rows এবং matching right-side rows ফেরত দেয়।

### RIGHT JOIN
Right table-এর সব rows এবং matching left-side rows ফেরত দেয়।

### FULL OUTER JOIN
দুই table-এর সব rows ফেরত দেয়; unmatched side-এ NULL থাকে।

### CROSS JOIN
দুই table-এর Cartesian product তৈরি করে।

### SELF JOIN
একই table-কে নিজের সঙ্গে join করে।

## 22. Subquery

একটি query-এর ভেতরে আরেকটি query।

```sql
SELECT name
FROM students
WHERE student_id IN (
    SELECT student_id
    FROM enrollments
);
```

## 23. CTE

CTE (Common Table Expression) হলো `WITH` clause দিয়ে সংজ্ঞায়িত temporary named query result।

```sql
WITH department_counts AS (
    SELECT department, COUNT(*) AS total
    FROM students
    GROUP BY department
)
SELECT *
FROM department_counts
WHERE total > 5;
```

## 24. Window Functions

Window functions rows-কে collapse না করে related rows-এর ওপর calculation করতে দেয়।

```sql
SELECT
    student_id,
    score,
    RANK() OVER (ORDER BY score DESC) AS position
FROM results;
```

Important functions:
- ROW_NUMBER()
- RANK()
- DENSE_RANK()
- LAG()
- LEAD()
- SUM() OVER()
- AVG() OVER()

## 25. SQL Transactions

Transaction হলো operations-এর একটি logical unit।

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 500
WHERE account_id = 1;

UPDATE accounts
SET balance = balance + 500
WHERE account_id = 2;

COMMIT;
```

যেকোনো error হলে application বা database error-handling logic অনুযায়ী rollback করা প্রয়োজন হতে পারে।

## 26. ACID Properties

- Atomicity: Transaction সম্পূর্ণ হবে অথবা rollback হবে।
- Consistency: Database constraints বজায় থাকবে।
- Isolation: Concurrent transactions-এর interaction নিয়ন্ত্রিত থাকবে।
- Durability: Commit করা data সঠিক durability configuration-এর অধীনে টিকে থাকবে।

## 27. Advanced SQL Topics

- CASE
- COALESCE
- NULLIF
- EXISTS
- NOT EXISTS
- UNION
- UNION ALL
- INTERSECT
- EXCEPT
- Recursive CTE
- Correlated Subqueries
- Date and Time Functions
- JSON/JSONB
- Conditional Aggregation
- Ranking
- Running Totals

Practice target: 100 SQL problems.

---

# PART 3: POSTGRESQL NOTES

## 28. What is PostgreSQL?

PostgreSQL একটি open-source relational database system, যা advanced SQL, transactions, indexing, extensibility এবং concurrency control সমর্থন করে।

Official Documentation:
https://www.postgresql.org/docs/current/

## 29. PostgreSQL Data Types

- SMALLINT
- INTEGER
- BIGINT
- NUMERIC
- REAL
- DOUBLE PRECISION
- BOOLEAN
- CHAR
- VARCHAR
- TEXT
- DATE
- TIME
- TIMESTAMP
- TIMESTAMPTZ
- UUID
- JSON
- JSONB
- ARRAY

Data type বাছাই করার সময় storage, validation এবং query requirements বিবেচনা করতে হবে।

## 30. Constraints

- PRIMARY KEY
- FOREIGN KEY
- UNIQUE
- NOT NULL
- CHECK
- DEFAULT

Example:

```sql
CREATE TABLE products (
    product_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    sku TEXT UNIQUE
);
```

## 31. Views

View হলো stored query definition-এর মাধ্যমে উপস্থাপিত virtual table।

```sql
CREATE VIEW active_students AS
SELECT student_id, name
FROM students
WHERE status = 'active';
```

## 32. Materialized Views

Materialized view query result সংরক্ষণ করে। Data update করতে সাধারণত refresh করতে হয়।

```sql
REFRESH MATERIALIZED VIEW sales_summary;
```

## 33. Functions and Procedures

Functions values বা result sets ফেরত দিতে পারে। Procedures procedural operations চালানোর জন্য ব্যবহৃত হয়।

Learn:
- PL/pgSQL
- Function parameters
- Return types
- Exception handling
- Stored procedures
- Triggers

## 34. Indexing Basics

Index data search দ্রুত করতে পারে, কিন্তু অতিরিক্ত index storage ও write overhead বাড়ায়।

```sql
CREATE INDEX idx_students_email
ON students(email);
```

Index সব query-কে দ্রুত করবে না। Query pattern ও execution plan অনুযায়ী index design করতে হয়।

## 35. PostgreSQL Administration

- psql
- pgAdmin
- DBeaver
- Database Roles
- Permissions
- Database Configuration
- Connection Management
- Logs
- Extensions
- Backup and Restore
- Upgrades

---

# PART 4: DATABASE INTERNALS

## 36. Database Storage

Learn:
- Pages and Blocks
- Heap Tables
- Tuple Storage
- Buffer Cache
- Shared Buffers
- Disk I/O
- WAL
- Checkpoints
- Background Processes

## 37. B-Tree Index

B-tree একটি balanced search tree family-এর structure, যা PostgreSQL-এর default index type।

Benefits:
- Equality searches
- Range queries
- Ordered retrieval
- অনেক ক্ষেত্রে sorting-এর কাজ কমানো

## 38. Composite Index

একাধিক column নিয়ে তৈরি index।

```sql
CREATE INDEX idx_orders_customer_date
ON orders(customer_id, created_at);
```

Column order গুরুত্বপূর্ণ। সাধারণত index-এর leading columns query predicates-এর সঙ্গে মিলে গেলে index বেশি কার্যকর হতে পারে।

## 39. Query Planner

Query planner SQL query execute করার জন্য সম্ভাব্য execution plans evaluate করে।

Learn:
- Cost Estimation
- Table Statistics
- Sequential Scan
- Index Scan
- Join Algorithms
- Cardinality Estimation
- Sort and Aggregate Costs

## 40. EXPLAIN ANALYZE

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM orders
WHERE customer_id = 101;
```

EXPLAIN query plan দেখায়। ANALYZE query execute করে actual measurements সংগ্রহ করে।

সতর্কতা: EXPLAIN ANALYZE সাধারণ SELECT-এর ক্ষেত্রে query চালায় এবং data-modifying statements-এর ক্ষেত্রে পরিবর্তনও ঘটাতে পারে। Production-এ ব্যবহারের আগে সতর্ক হও।

## 41. MVCC

MVCC (Multi-Version Concurrency Control) হলো এমন concurrency-control technique, যেখানে transactions-এর জন্য data versions ব্যবহৃত হয়।

Benefits:
- Readers ও writers-এর মধ্যে অনেক ক্ষেত্রে blocking কমায়।
- Transaction snapshots সমর্থন করে।
- Concurrent access সহজ করে।

PostgreSQL-এ obsolete row versions পরিষ্কার করার জন্য VACUUM গুরুত্বপূর্ণ।

## 42. WAL

Write-Ahead Logging পরিবর্তনগুলোর log আগে লিখে crash recovery এবং replication-এ সহায়তা করে।

Learn:
- WAL Records
- Checkpoints
- WAL Archiving
- Crash Recovery
- Replication
- PITR

---

# PART 5: PERFORMANCE OPTIMIZATION

## 43. Query Optimization Checklist

- EXPLAIN ANALYZE ব্যবহার করো।
- Slow query শনাক্ত করো।
- WHERE conditions পরীক্ষা করো।
- JOIN conditions পরীক্ষা করো।
- উপযুক্ত index তৈরি করো।
- অপ্রয়োজনীয় SELECT * এড়িয়ে চলো।
- N+1 queries শনাক্ত করো।
- Table statistics পরীক্ষা করো।
- অতিরিক্ত indexing এড়িয়ে চলো।
- Realistic data দিয়ে benchmark করো।

## 44. Connection Pooling

Connection pooling database connections পুনরায় ব্যবহার করে connection overhead কমাতে পারে।

Learn:
- Connection Lifecycle
- Pool Size
- Idle Connections
- Timeouts
- Pool Exhaustion
- Transaction Pooling
- Session Pooling

Tools:
- PgBouncer
- Application-Level Connection Pools

## 45. Performance Metrics

- Query Latency
- p50 Latency
- p95 Latency
- p99 Latency
- Throughput
- Transactions Per Second
- CPU Utilization
- Memory Usage
- Disk I/O
- Cache Hit Ratio
- Connection Count
- Replication Lag

---

# PART 6: BACKUP, RECOVERY AND REPLICATION

## 46. Backup Types

### Logical Backup
SQL objects ও data export করে।

Tools:
- pg_dump
- pg_restore

### Physical Backup
Database-এর physical files এবং প্রয়োজনীয় recovery information নিয়ে কাজ করে।

Learn:
- Base Backups
- WAL Archiving
- PITR
- Backup Retention
- Restore Verification

## 47. RPO and RTO

RPO (Recovery Point Objective): সর্বোচ্চ কতটা data loss গ্রহণযোগ্য।

RTO (Recovery Time Objective): কত সময়ের মধ্যে service restore করতে হবে।

## 48. Replication

Replication হলো এক database server থেকে অন্য server-এ database changes replicate করা।

Types:
- Streaming Replication
- Synchronous Replication
- Asynchronous Replication
- Logical Replication

## 49. High Availability

Learn:
- Primary and Standby
- Failover
- Switchover
- Replication Lag
- Failure Detection
- Split-Brain Prevention
- Recovery Testing

---

# PART 7: DATABASE SECURITY

## 50. Security Fundamentals

- Authentication
- Authorization
- Least Privilege
- Roles and Permissions
- TLS
- Secrets Management
- Encryption at Rest
- Audit Logging
- SQL Injection Prevention
- Row-Level Security
- Backup Security

## 51. SQL Injection Prevention

Parameterized queries ব্যবহার করো।

Python example:

```python
cursor.execute(
    "SELECT * FROM users WHERE email = %s",
    (email,)
)
```

User input-কে SQL string-এর সঙ্গে সরাসরি concatenate করা উচিত নয়।

---

# PART 8: NOSQL AND DISTRIBUTED SYSTEMS

## 52. Redis

Learn:
- Key-Value Storage
- Strings
- Hashes
- Lists
- Sets
- Sorted Sets
- TTL
- Eviction Policies
- Caching
- Persistence
- Replication

## 53. MongoDB

Learn:
- Documents
- Collections
- BSON
- Schema Design
- Embedding
- Referencing
- Indexes
- Aggregation Pipeline
- Replica Sets
- Sharding

## 54. Distributed Systems

Learn:
- Partitioning
- Replication
- Sharding
- Consistency Models
- Eventual Consistency
- CAP Theorem
- Quorums
- Leader Election
- Distributed Transactions
- Idempotency
- Retries and Timeouts

## 55. Other Technologies

- Apache Kafka: Event Streaming
- Apache Cassandra: Distributed Database
- ClickHouse: Analytical Database
- Elasticsearch: Search and Analytics
- DuckDB: Analytical SQL Engine
- Vector Databases: Similarity Search

---

# PART 9: LINUX, DOCKER AND CLOUD

## 56. Linux

Learn:
- Filesystem
- Permissions
- Users and Groups
- Processes
- Memory
- Disk Space
- Networking
- TCP/IP
- DNS
- Logs
- Bash Scripting
- Systemd

## 57. Docker

Learn:
- Images
- Containers
- Dockerfile
- Docker Compose
- Volumes
- Networks
- Environment Variables
- Health Checks
- Persistent Storage
- Container Recovery

## 58. AWS

Learn:
- Amazon RDS
- Amazon Aurora
- Amazon DynamoDB
- IAM
- VPC
- Subnets
- Security Groups
- CloudWatch
- Automated Backups
- Snapshots
- Read Replicas
- Multi-AZ Deployments

Resource:
https://aws.amazon.com/rds/

## 59. Infrastructure Automation

Learn:
- Git and GitHub
- CI/CD
- Terraform
- Infrastructure as Code
- Configuration Management
- Secrets Management
- Automated Backup Verification
- Monitoring and Alerting

---

# PART 10: PYTHON DATABASE AUTOMATION

## 60. Python Database Skills

Learn:
- psycopg
- SQLAlchemy
- Django ORM
- Database Connections
- Transactions
- Connection Pooling
- Parameterized Queries
- Database Migrations
- Error Handling
- Retry Logic
- Logging
- Data Validation

## 61. Automation Projects

- Database Health Checker
- Backup Verification Script
- Slow Query Report Generator
- Database Monitoring Script
- Data Quality Checker
- Migration Validation Tool

---

# PART 11: PORTFOLIO PROJECTS

## Project 1: E-commerce Database

Features:
- Customers
- Products
- Orders
- Payments
- Inventory
- Constraints
- Relationships
- Indexes
- Transactions
- Sales Reports

## Project 2: Performance Optimization

Features:
- Large Dataset
- Slow Query Analysis
- Index Optimization
- EXPLAIN ANALYZE
- Benchmarking
- Performance Report

## Project 3: PostgreSQL Reliability

Features:
- Primary and Standby
- Replication
- Backup
- Restore
- PITR
- Monitoring
- Failover Testing
- Disaster Recovery Guide

## Project 4: Django + PostgreSQL + Redis

Features:
- Django REST Framework
- PostgreSQL
- Redis Caching
- Database Migrations
- Connection Pooling
- Docker
- Security
- Monitoring

## GitHub Requirements

প্রতিটি project-এ রাখবে:
- README.md
- ER Diagram
- Architecture Diagram
- SQL Scripts
- Sample Data
- Setup Instructions
- Benchmark Results
- Security Notes
- Backup and Recovery Guide

---

# PART 12: INTERVIEW PREPARATION

## SQL Questions
- Explain JOINs.
- Explain GROUP BY vs HAVING.
- Find the second-highest salary.
- Find duplicate records.
- Explain CTEs.
- Explain Window Functions.
- Find top 3 records per group.

## Database Design Questions
- What is normalization?
- Explain primary and foreign keys.
- What is referential integrity?
- When should denormalization be used?
- How would you design an e-commerce database?

## Performance Questions
- What is an index?
- How does a B-tree work?
- Why can a query ignore an index?
- How do you analyze a slow query?
- What is a composite index?
- What is EXPLAIN ANALYZE?

## Transaction Questions
- Explain ACID.
- What is MVCC?
- What are isolation levels?
- What causes deadlocks?
- How do you prevent lost updates?

## Administration Questions
- Explain backup and restore.
- What is PITR?
- What is replication?
- What is failover?
- How do you monitor database health?
- How do you recover from a failure?

## Distributed Systems Questions
- Replication vs Sharding
- Strong vs Eventual Consistency
- Explain the CAP Theorem.
- What is partitioning?
- What is idempotency?

---

# PART 13: WEEK-BY-WEEK STUDY PLAN

Week 1: DBMS and RDBMS Fundamentals

Week 2: ER Diagrams, Keys, Relationships, Normalization

Week 3: Basic SQL

Week 4: DDL, DML and Constraints

Week 5: JOINs and Aggregations

Week 6: Subqueries and CTEs

Week 7: Window Functions and SQL Problems

Week 8: PostgreSQL Installation and Tools

Week 9: Schema Design and Indexes

Week 10: Transactions and Isolation Levels

Week 11: Views, Functions and Migrations

Week 12: Storage, Pages, B-Tree and WAL

Week 13: Index Design and EXPLAIN ANALYZE

Week 14: Query Optimization

Week 15: MVCC, Locks and Deadlocks

Week 16: Performance Benchmarking

Week 17: Security and Permissions

Week 18: Backup and Restore

Week 19: PITR and Replication

Week 20: Monitoring and High Availability

Week 21: Redis and Caching

Week 22: MongoDB

Week 23: Sharding and Consistency

Week 24: Distributed Systems Project

Week 25: Linux and Networking

Week 26: Docker and Docker Compose

Week 27: AWS RDS and Cloud Networking

Week 28: Python Automation

Week 29: Advanced Architecture

Week 30: Partitioning, CDC and OLTP/OLAP

Week 31: Portfolio Projects

Week 32: Interview Preparation and Job Applications

---

# FINAL ROADMAP SUMMARY

Recommended Learning Order:

1. Database Fundamentals
2. SQL Mastery
3. PostgreSQL
4. Database Design and Normalization
5. Transactions and ACID
6. Indexing and Query Optimization
7. Database Internals
8. Backup, Recovery and Replication
9. Database Security
10. Linux and Networking
11. Docker and Cloud
12. Python Automation
13. NoSQL and Distributed Systems
14. Advanced Database Architecture
15. Portfolio Projects
16. Interview Preparation

**Final Goal:** Become capable of designing, optimizing, securing, monitoring, backing up, recovering, and operating reliable databases in real-world applications.

**Study Strategy:** প্রতিটি topic-এর জন্য Theory + Notes + SQL Practice + Practical Lab + Project অনুসরণ করো। শুধু notes পড়লে হবে না; নিজে database তৈরি করে query execute এবং error debug করতে হবে।