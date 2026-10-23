# Database Engineer Roadmap with Questions and Answers
## Beginner to Advanced — Bangla + English

# PART 1: DATABASE FUNDAMENTALS

## 1. What is Data?

**Answer:** Data হলো raw facts and figures, যা processing-এর আগে সব সময় meaningful information নাও হতে পারে।

**Example:**
- Name: Faruk
- Age: 25
- Department: CSE

## 2. What is a Database?

**Answer:** A database is an organized collection of related data that can be stored, accessed, managed, and updated efficiently.

**Example:** A university database stores students, teachers, courses, and results.

## 3. What is DBMS?

**Answer:** DBMS (Database Management System) হলো software, যার মাধ্যমে database তৈরি, সংরক্ষণ, query, update এবং manage করা যায়।

**Examples:** PostgreSQL, MySQL, SQLite, Oracle Database.

## 4. What is RDBMS?

**Answer:** RDBMS (Relational Database Management System) হলো DBMS-এর একটি ধরন, যেখানে data relational tables-এর মাধ্যমে সংরক্ষণ করা হয়।

**Examples:** PostgreSQL, MySQL, Microsoft SQL Server.

## 5. DBMS vs RDBMS

**Answer:**

| DBMS | RDBMS |
|---|---|
| Database manage করার general software category | Relational model ব্যবহার করে |
| Different data models support করতে পারে | Data tables ও relationships-এর মাধ্যমে organize করে |
| সব DBMS relational নয় | RDBMS relational DBMS |
| Example: Document-oriented DBMS | PostgreSQL, MySQL |

## 6. What are the main components of a database?

**Answer:**
- **Table:** Rows এবং columns-এ data রাখে।
- **Row:** একটি record।
- **Column:** একটি attribute বা field।
- **Schema:** Database objects-এর structure।
- **Query:** Database-এর কাছে request বা operation।
- **Constraint:** Data validity বজায় রাখার rule।
- **Index:** Data search দ্রুত করতে সাহায্য করে।

## 7. What is a Primary Key?

**Answer:** A primary key uniquely identifies each row in a table.

Properties:
- Duplicate value থাকতে পারবে না।
- NULL হতে পারবে না।
- একটি table-এ একটি primary-key constraint থাকে; সেটি এক বা একাধিক column নিয়ে তৈরি হতে পারে।

```sql
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
```

## 8. What is a Foreign Key?

**Answer:** A foreign key হলো এক বা একাধিক column-এর constraint, যা অন্য table-এর referenced key-এর সঙ্গে relationship ও referential integrity বজায় রাখে।

```sql
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id)
);
```

## 9. What is the difference between Primary Key and UNIQUE?

**Answer:**

| Primary Key | UNIQUE |
|---|---|
| প্রতিটি row uniquely identify করে | Duplicate values প্রতিরোধ করে |
| NULL allowed নয় | NULL handling database অনুযায়ী ভিন্ন হতে পারে |
| একটি table-এ একটি primary-key constraint | একাধিক UNIQUE constraint থাকতে পারে |

## 10. What is a Candidate Key?

**Answer:** A candidate key হলো minimal set of columns, যা প্রতিটি row uniquely identify করতে পারে।

একটি candidate key-এর কোনো column বাদ দিলে যদি uniqueness বজায় না থাকে, তাহলে সেটি minimal।

## 11. What is a Composite Key?

**Answer:** A composite key হলো দুই বা তার বেশি columns নিয়ে তৈরি key।

```sql
CREATE TABLE student_courses (
    student_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY (student_id, course_id)
);
```

এখানে student_id ও course_id একসঙ্গে একটি row uniquely identify করে।

## 12. What are Database Relationships?

**Answer:**

- **One-to-One:** একজন person-এর একটি passport record।
- **One-to-Many:** একটি department-এর অনেক students।
- **Many-to-Many:** অনেক students অনেক courses-এ enroll করতে পারে।

Many-to-many relationship সাধারণত junction table দিয়ে implement করা হয়।

## 13. What is Normalization?

**Answer:** Normalization হলো database design-এর process, যা unnecessary duplication এবং insertion, update, deletion anomalies কমাতে সাহায্য করে।

### 1NF — First Normal Form
প্রতিটি cell-এ একটি atomic value থাকবে এবং repeating groups থাকবে না।

### 2NF — Second Normal Form
Table 1NF-এ থাকবে এবং কোনো non-prime attribute composite candidate key-এর proper subset-এর ওপর নির্ভর করবে না।

### 3NF — Third Normal Form
প্রতিটি non-trivial functional dependency `X → A`-এর ক্ষেত্রে X superkey হবে, অথবা A prime attribute হবে। সহজভাবে, non-key attributes-এর অনুপযুক্ত transitive dependency দূর করা হয়।

### BCNF — Boyce-Codd Normal Form
প্রতিটি non-trivial functional dependency-তে determinant অবশ্যই superkey হবে।

## 14. What is Denormalization?

**Answer:** Denormalization হলো query performance উন্নত করার জন্য ইচ্ছাকৃতভাবে কিছু data duplication বা precomputed data রাখা।

**Example:** Frequently accessed report-এর জন্য summary table তৈরি করা।

**Trade-off:** Read performance বাড়তে পারে, তবে storage ও data consistency maintain করার complexity বাড়ে।

## 15. What is an ER Diagram?

**Answer:** An Entity-Relationship Diagram হলো database-এর entities, attributes এবং relationships-এর visual representation।

**Example:** Student → Enrollment → Course.

# PART 2: SQL QUESTIONS AND ANSWERS

## 16. What is SQL?

**Answer:** SQL (Structured Query Language) হলো relational databases-এ data query, manipulation এবং database objects define করার language।

## 17. What are the main SQL command categories?

**Answer:**

| Category | Commands | Purpose |
|---|---|---|
| DQL | SELECT | Data retrieve |
| DML | INSERT, UPDATE, DELETE | Data manipulate |
| DDL | CREATE, ALTER, DROP | Structure define |
| DCL | GRANT, REVOKE | Permissions manage |
| TCL | BEGIN, COMMIT, ROLLBACK | Transactions manage |

এই classification প্রচলিত teaching convention; SQL command categorization বিভিন্ন source-এ কিছুটা ভিন্ন হতে পারে।

## 18. What is the difference between WHERE and HAVING?

**Answer:**
- `WHERE` grouping-এর আগে individual rows filter করে।
- `HAVING` grouping-এর পরে groups filter করে।

```sql
SELECT department, COUNT(*) AS total
FROM students
WHERE status = 'active'
GROUP BY department
HAVING COUNT(*) > 5;
```

এখানে WHERE active students filter করে, আর HAVING পাঁচটির বেশি active student থাকা departments নির্বাচন করে।

## 19. What is GROUP BY?

**Answer:** `GROUP BY` একই value-যুক্ত rows-কে group করে, যাতে aggregate calculations করা যায়।

```sql
SELECT department, COUNT(*) AS total_students
FROM students
GROUP BY department;
```

## 20. What are Aggregate Functions?

**Answer:** Aggregate functions একাধিক row থেকে একটি summary value বা প্রতিটি group-এর summary value তৈরি করে।

- `COUNT()` — Count
- `SUM()` — Total
- `AVG()` — Average
- `MIN()` — Minimum
- `MAX()` — Maximum

Note: `COUNT(column_name)` NULL values গণনা করে না; `COUNT(*)` rows গণনা করে।

## 21. What is a JOIN?

**Answer:** JOIN ব্যবহার করে দুই বা তার বেশি tables-এর related rows একসঙ্গে query করা হয়।

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
দুই table-এর matching ও unmatched rows ফেরত দেয়।

### CROSS JOIN
দুই table-এর Cartesian product তৈরি করে।

### SELF JOIN
একটি table-কে নিজের সঙ্গে join করে।

## 22. What is a Subquery?

**Answer:** A subquery হলো একটি SQL query-এর মধ্যে থাকা আরেকটি query।

```sql
SELECT name
FROM students
WHERE student_id IN (
    SELECT student_id
    FROM enrollments
);
```

এই query অন্তত একটি enrollment থাকা students-দের নাম ফেরত দেয়।

## 23. What is a CTE?

**Answer:** CTE (Common Table Expression) হলো `WITH` clause দিয়ে তৈরি named query result, যা একটি statement-এর মধ্যে ব্যবহার করা যায়।

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

## 24. What is a Window Function?

**Answer:** Window function related rows-এর ওপর calculation করে, কিন্তু সাধারণ GROUP BY-এর মতো প্রতিটি group-কে একটি row-তে collapse করে না।

```sql
SELECT
    student_id,
    score,
    RANK() OVER (ORDER BY score DESC) AS position
FROM results;
```

Important functions:
- `ROW_NUMBER()`
- `RANK()`
- `DENSE_RANK()`
- `LAG()`
- `LEAD()`
- `SUM() OVER()`

## 25. What is the difference between UNION and UNION ALL?

**Answer:**
- `UNION` combined result থেকে duplicate rows বাদ দেয়।
- `UNION ALL` duplicate rows-সহ সব rows রাখে।

```sql
SELECT email FROM customers
UNION ALL
SELECT email FROM suppliers;
```

Duplicate removal দরকার না হলে `UNION ALL` সাধারণত কম কাজ করে।

## 26. What is NULL in SQL?

**Answer:** NULL মানে value missing, unknown বা applicable নয়। এটি zero বা empty string-এর সমান নয়।

```sql
SELECT *
FROM students
WHERE email IS NULL;
```

NULL পরীক্ষা করতে `IS NULL` বা `IS NOT NULL` ব্যবহার করতে হয়; `= NULL` নয়।

## 27. What is a Transaction?

**Answer:** A transaction হলো database operations-এর একটি logical unit, যা সফলভাবে commit হয় অথবা প্রয়োজন হলে rollback করা হয়।

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

বাস্তব application-এ error হলে exception handling-এর মাধ্যমে rollback নিশ্চিত করতে হয়।

## 28. What are ACID Properties?

**Answer:**
- **Atomicity:** Transaction সম্পূর্ণ হবে অথবা rollback হবে।
- **Consistency:** Constraints ও database rules বজায় থাকবে।
- **Isolation:** Concurrent transactions-এর interaction নির্ধারিত isolation rules অনুযায়ী নিয়ন্ত্রিত হবে।
- **Durability:** Commit করা changes configured durability guarantees অনুযায়ী টিকে থাকবে।

## 29. What is the difference between DELETE, TRUNCATE and DROP?

**Answer:**

| Command | কাজ |
|---|---|
| DELETE | Selected rows বা WHERE না থাকলে সব rows মুছে দেয় |
| TRUNCATE | দ্রুত table-এর সব rows সরিয়ে দেয় |
| DROP | Database object-টি সরিয়ে দেয় |

PostgreSQL-এ TRUNCATE সাধারণত table-level lock নেয় এবং identity sequence reset করার option আছে। Transactional DDL support-এর কারণে transaction-এর মধ্যে rollback-ও করা যায়।

## 30. How do you find the second-highest salary?

**Answer:**

```sql
SELECT MAX(salary) AS second_highest_salary
FROM employees
WHERE salary < (
    SELECT MAX(salary)
    FROM employees
);
```

এই query দ্বিতীয় সর্বোচ্চ **distinct** salary ফেরত দেয়। কোনো second distinct salary না থাকলে result NULL হবে।

## 31. How do you find duplicate emails?

**Answer:**

```sql
SELECT email, COUNT(*) AS total
FROM users
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1;
```

এই query duplicate non-NULL email values শনাক্ত করে।

## 32. How do you find the top three salaries per department?

**Answer:**

```sql
WITH ranked_employees AS (
    SELECT
        employee_id,
        department_id,
        salary,
        DENSE_RANK() OVER (
            PARTITION BY department_id
            ORDER BY salary DESC
        ) AS salary_rank
    FROM employees
)
SELECT *
FROM ranked_employees
WHERE salary_rank <= 3;
```

`DENSE_RANK()` একই salary-কে একই rank দেয়। তাই ties থাকলে তিনটির বেশি rows আসতে পারে। ঠিক তিনটি row চাইলে `ROW_NUMBER()` ব্যবহার করা যায়।

# PART 3: POSTGRESQL QUESTIONS AND ANSWERS

## 33. What is PostgreSQL?

**Answer:** PostgreSQL হলো একটি open-source object-relational database management system, যা SQL, transactions, concurrency control, indexing এবং extensibility সমর্থন করে।

## 34. What are PostgreSQL data types?

**Answer:**
- Integers: `SMALLINT`, `INTEGER`, `BIGINT`
- Decimal: `NUMERIC`, `REAL`, `DOUBLE PRECISION`
- Text: `TEXT`, `VARCHAR`
- Boolean: `BOOLEAN`
- Date and time: `DATE`, `TIME`, `TIMESTAMP`, `TIMESTAMPTZ`
- Other: `UUID`, `JSON`, `JSONB`, `ARRAY`

Data type বাছাই করার সময় validation, precision, storage এবং query requirements বিবেচনা করতে হয়।

## 35. What is an Index?

**Answer:** An index হলো একটি data structure, যা উপযুক্ত query-তে rows দ্রুত খুঁজে পেতে সাহায্য করে।

```sql
CREATE INDEX idx_students_email
ON students(email);
```

**Advantages:** Read performance উন্নত হতে পারে।

**Disadvantages:** Extra storage লাগে এবং INSERT, UPDATE, DELETE-এর সময় maintenance overhead বাড়ে।

## 36. What is a Composite Index?

**Answer:** Composite index হলো একাধিক columns নিয়ে তৈরি index।

```sql
CREATE INDEX idx_orders_customer_date
ON orders(customer_id, created_at);
```

এই index `customer_id` দিয়ে filter এবং তার সঙ্গে `created_at`-ভিত্তিক query-তে কার্যকর হতে পারে। Column order গুরুত্বপূর্ণ।

## 37. What is a View?

**Answer:** A view হলো একটি named query definition, যা virtual table-এর মতো ব্যবহার করা যায়।

```sql
CREATE VIEW active_students AS
SELECT student_id, name
FROM students
WHERE status = 'active';
```

সাধারণ view-এর query result আলাদাভাবে materialize করে রাখা হয় না।

## 38. What is a Materialized View?

**Answer:** Materialized view query result সংরক্ষণ করে। তাই read দ্রুত হতে পারে, তবে data refresh করতে হয়।

```sql
REFRESH MATERIALIZED VIEW sales_summary;
```

## 39. What is the difference between JSON and JSONB?

**Answer:**
- `JSON` input text-এর মূল formatting ও key order সংরক্ষণ করে।
- `JSONB` data-কে decomposed binary representation-এ রাখে, যা সাধারণত query ও indexing-এর জন্য বেশি সুবিধাজনক।

JSONB duplicate object keys-এর original representation সংরক্ষণ করে না।

## 40. What is MVCC?

**Answer:** MVCC (Multi-Version Concurrency Control) হলো PostgreSQL-এর concurrency-control mechanism, যা transactions-কে উপযুক্ত row versions ও snapshots-এর মাধ্যমে data পড়তে সাহায্য করে।

Benefits:
- অনেক ক্ষেত্রে readers ও writers-এর blocking কমে।
- Concurrent transactions সমর্থন করে।
- Consistent snapshots প্রদান করে।

Obsolete row versions পরিষ্কার করার জন্য VACUUM গুরুত্বপূর্ণ।

## 41. What is WAL?

**Answer:** WAL (Write-Ahead Logging) database changes-এর log records সংরক্ষণ করে। Data pages disk-এ লেখার আগে প্রয়োজনীয় WAL durable হওয়ার ব্যবস্থা crash recovery-তে সাহায্য করে।

Uses:
- Crash recovery
- Replication
- WAL archiving
- Point-in-Time Recovery

## 42. What is EXPLAIN ANALYZE?

**Answer:** PostgreSQL-এর `EXPLAIN` execution plan দেখায়। `EXPLAIN ANALYZE` query execute করে actual execution measurements সংগ্রহ করে।

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM orders
WHERE customer_id = 101;
```

এতে estimated cost, actual timing, row counts এবং buffer activity বিশ্লেষণ করা যায়।

**Warning:** `EXPLAIN ANALYZE` query execute করে। Data-modifying statements-এর ক্ষেত্রে database পরিবর্তিত হতে পারে।

## 43. What is VACUUM?

**Answer:** PostgreSQL-এর VACUUM obsolete row versions-এর storage space পুনর্ব্যবহারের উপযোগী করে এবং transaction ID wraparound prevention-এর মতো maintenance tasks-এ সাহায্য করে।

- `VACUUM`: সাধারণ maintenance।
- `VACUUM ANALYZE`: Vacuum-এর সঙ্গে planner statistics update করে।
- `VACUUM FULL`: Table rewrite করে space ফেরত দিতে পারে, তবে stronger locking লাগে।

## 44. What is Connection Pooling?

**Answer:** Connection pooling database connections পুনরায় ব্যবহার করে connection setup overhead কমায়।

**Example:** PgBouncer.

Benefits:
- Connection overhead কমে।
- Database connection সংখ্যা নিয়ন্ত্রণ করা যায়।
- High-concurrency applications পরিচালনা সহজ হয়।

# PART 4: PERFORMANCE ENGINEERING

## 45. How do you optimize a slow SQL query?

**Answer:**
1. Slow query শনাক্ত করো।
2. `EXPLAIN (ANALYZE, BUFFERS)` দিয়ে plan পরীক্ষা করো।
3. Estimated ও actual row counts তুলনা করো।
4. WHERE এবং JOIN conditions পরীক্ষা করো।
5. Appropriate indexes বিবেচনা করো।
6. অপ্রয়োজনীয় columns ও rows retrieve করা এড়াও।
7. N+1 queries শনাক্ত করো।
8. Realistic dataset দিয়ে benchmark করো।
9. পরিবর্তনের আগে ও পরে performance তুলনা করো।

## 46. Why might PostgreSQL not use an index?

**Answer:** সম্ভাব্য কারণ:
- Table ছোট হওয়ায় sequential scan সস্তা।
- Query-তে অনেক rows দরকার।
- Column statistics পুরোনো।
- Predicate index-এর সঙ্গে কার্যকরভাবে মেলে না।
- Column-এর ওপর function বা cast ব্যবহৃত হয়েছে এবং matching expression index নেই।
- Composite index-এর leading-column requirements পূরণ হচ্ছে না।

Index ব্যবহার না করলেই query ভুল—এমন নয়। Execution plan ও workload বিশ্লেষণ করতে হবে।

## 47. What is an N+1 Query Problem?

**Answer:** একটি initial query-এর পরে প্রতিটি record-এর জন্য আলাদা query চালানো হলে N+1 query problem তৈরি হয়।

**Example:** 100 students load করতে 1টি query এবং প্রতিটি student-এর courses-এর জন্য আরও 100টি query।

**Solution:**
- Appropriate JOIN
- Django ORM-এ `select_related()`
- Django ORM-এ `prefetch_related()`
- Batch loading

## 48. What is Query Latency?

**Answer:** Query latency হলো একটি query শুরু হওয়া থেকে তার result পাওয়া পর্যন্ত সময়।

Common metrics:
- p50: Median latency
- p95: 95% requests-এর latency এই মানের মধ্যে
- p99: 99% requests-এর latency এই মানের মধ্যে

এই metrics tail latency ও user experience বুঝতে সাহায্য করে।

## 49. What is a Deadlock?

**Answer:** Deadlock ঘটে যখন দুই বা তার বেশি transactions এমনভাবে একে অপরের locks-এর জন্য অপেক্ষা করে যে কোনো transaction আর এগোতে পারে না।

**Prevention:**
- Consistent order-এ resources lock করা।
- Transactions ছোট রাখা।
- Retry logic implement করা।
- Deadlock errors monitor করা।

Deadlock পুরোপুরি অসম্ভব করা যায় না; application-কে উপযুক্ত retry handling রাখতে হয়।

# PART 5: BACKUP, RECOVERY AND REPLICATION

## 50. What is a Database Backup?

**Answer:** Database backup হলো failure, corruption বা accidental deletion-এর পরে data restore করার জন্য সংরক্ষিত copy।

Types:
- Logical backup
- Physical backup
- Base backup
- WAL archive

Backup সফলভাবে তৈরি হওয়াই যথেষ্ট নয়; restore test-ও করতে হবে।

## 51. What is PITR?

**Answer:** PITR (Point-in-Time Recovery) হলো base backup এবং প্রয়োজনীয় WAL records ব্যবহার করে database-কে নির্দিষ্ট সময়ের অবস্থায় restore করার পদ্ধতি।

এটি accidental deletion বা unwanted database changes থেকে recovery-তে সাহায্য করে।

## 52. What are RPO and RTO?

**Answer:**
- **RPO:** কতটা data loss গ্রহণযোগ্য।
- **RTO:** কত সময়ের মধ্যে service restore করতে হবে।

Example:
RPO = 5 minutes এবং RTO = 30 minutes হলে লক্ষ্য হলো সর্বোচ্চ 5 মিনিটের data loss সীমার মধ্যে থাকা এবং 30 মিনিটের মধ্যে service restore করা।

## 53. What is Replication?

**Answer:** Replication হলো একটি database system-এর changes অন্য database server-এ পাঠানো ও প্রয়োগ করার প্রক্রিয়া।

Types:
- Streaming replication
- Synchronous replication
- Asynchronous replication
- Logical replication

Replication availability ও read scaling-এ সাহায্য করতে পারে, কিন্তু এটি backup-এর বিকল্প নয়।

## 54. What is High Availability?

**Answer:** High Availability (HA) হলো এমন architecture, যা server বা infrastructure failure হলেও service downtime কমানোর চেষ্টা করে।

Common components:
- Primary and standby
- Health monitoring
- Failover
- Replication
- Backup and recovery procedures
- Failure testing

# PART 6: DATABASE SECURITY

## 55. What is SQL Injection?

**Answer:** SQL Injection হলো এমন vulnerability, যেখানে untrusted input SQL query-এর structure পরিবর্তন করতে পারে।

**Unsafe approach:**

```python
query = (
    "SELECT * FROM users WHERE email = '"
    + email
    + "'"
)
```

**Safer approach using parameterized queries:**

```python
cursor.execute(
    "SELECT * FROM users WHERE email = %s",
    (email,)
)
```

Parameters দিয়ে values পাঠাতে হবে, SQL string-এর সঙ্গে user input concatenate করা উচিত নয়।

## 56. What is the Principle of Least Privilege?

**Answer:** প্রতিটি user বা service-কে তার কাজের জন্য যতটুকু permission প্রয়োজন, ততটুকুই দেওয়া।

Benefits:
- Unauthorized access-এর ঝুঁকি কমে।
- Accidental data modification সীমিত হয়।
- Security auditing সহজ হয়।

## 57. What is Row-Level Security (RLS)?

**Answer:** PostgreSQL Row-Level Security policies-এর মাধ্যমে নির্দিষ্ট user বা role কোন rows read বা modify করতে পারবে, তা নিয়ন্ত্রণ করা যায়।

RLS সঠিকভাবে configure করতে হবে এবং application authorization-এর সঙ্গে মিলিয়ে পরীক্ষা করতে হবে।

# PART 7: NOSQL AND DISTRIBUTED SYSTEMS

## 58. What is Redis?

**Answer:** Redis হলো একটি in-memory data store, যা caching, counters, queues এবং অন্যান্য low-latency use cases-এ ব্যবহৃত হয়।

Important concepts:
- Strings, Hashes, Lists, Sets
- Sorted Sets
- TTL
- Eviction policies
- Persistence
- Replication

## 59. What is MongoDB?

**Answer:** MongoDB হলো document-oriented database, যেখানে data BSON documents হিসেবে collections-এ সংরক্ষণ করা হয়।

Important concepts:
- Documents and Collections
- Schema Design
- Embedding and Referencing
- Indexes
- Aggregation Pipeline
- Replica Sets
- Sharding

## 60. SQL vs NoSQL

**Answer:**

| SQL Databases | NoSQL Databases |
|---|---|
| Relational model | Document, key-value, wide-column বা graph model হতে পারে |
| Structured schemas সাধারণ | Data model অনুযায়ী flexible schema হতে পারে |
| SQL query language | Database-specific APIs বা query languages |
| PostgreSQL, MySQL | MongoDB, Redis, Cassandra |

কোনো একটি সব ক্ষেত্রে সেরা নয়। Data relationships, consistency, query patterns এবং scaling requirements অনুযায়ী নির্বাচন করতে হয়।

## 61. What is Sharding?

**Answer:** Sharding হলো data-কে একাধিক database nodes-এ ভাগ করে সংরক্ষণ করা।

Benefits:
- Storage ও workload distribute করা যায়।
- বড় dataset scale করা সম্ভব হয়।

Challenges:
- Cross-shard queries
- Rebalancing
- Distributed transactions
- Hot partitions

## 62. What is the CAP Theorem?

**Answer:** CAP Theorem অনুযায়ী network partition-এর সময় distributed system-কে consistency এবং availability-এর মধ্যে trade-off করতে হয়।

- **Consistency:** সফল read-এ সর্বশেষ সফল write বা নির্ধারিত consistency guarantee অনুযায়ী result পাওয়া।
- **Availability:** প্রতিটি request একটি non-error response পায়।
- **Partition Tolerance:** Network partition হলেও system আচরণ করে।

বাস্তবে distributed systems-এ partition-এর সময় কোন guarantee অগ্রাধিকার পাবে, তা design অনুযায়ী নির্ধারিত হয়।

## 63. What is Idempotency?

**Answer:** কোনো operation idempotent হলে একই operation একাধিকবার execute করলেও তার intended final effect একই থাকে।

**Example:** নির্দিষ্ট resource-এর status `active`-এ set করা, সেটি আবার করলেও status `active` থাকে।

Payment systems-এ idempotency keys duplicate processing প্রতিরোধে সাহায্য করতে পারে।

# PART 8: LINUX, DOCKER AND CLOUD

## 64. Why should a Database Engineer learn Linux?

**Answer:** Database servers সাধারণত Linux-based environments-এ চলে। Linux knowledge দিয়ে processes, memory, storage, networking, permissions এবং logs troubleshoot করা যায়।

## 65. What is Docker?

**Answer:** Docker হলো containerization platform, যা applications ও dependencies-কে portable containers-এ package ও run করতে সাহায্য করে।

Important concepts:
- Images
- Containers
- Dockerfile
- Docker Compose
- Volumes
- Networks
- Health checks

Database-এর persistent data production environment-এ যথাযথ storage ও backup strategy দিয়ে পরিচালনা করতে হয়।

## 66. What is Amazon RDS?

**Answer:** Amazon RDS হলো AWS-এর managed relational database service, যা supported database engines-এর provisioning, backups, monitoring এবং maintenance-এর অনেক কাজ সহজ করে।

Related topics:
- Automated backups
- Read replicas
- Multi-AZ deployments
- VPC and security groups
- IAM integration
- CloudWatch monitoring

## 67. What is Infrastructure as Code (IaC)?

**Answer:** Infrastructure as Code হলো configuration files বা code ব্যবহার করে infrastructure define ও manage করার পদ্ধতি।

**Example:** Terraform দিয়ে database infrastructure, networking এবং permissions-এর configuration version control করা।

# PART 9: PYTHON DATABASE ENGINEERING

## 68. What is psycopg?

**Answer:** psycopg হলো Python-এর PostgreSQL adapter, যা Python applications-কে PostgreSQL database-এর সঙ্গে connect করে SQL execute করতে সাহায্য করে।

## 69. What is SQLAlchemy?

**Answer:** SQLAlchemy হলো Python SQL toolkit এবং ORM, যা SQL expression তৈরি, database connections পরিচালনা এবং object-relational mapping করতে সাহায্য করে।

## 70. What is Django ORM?

**Answer:** Django ORM হলো Django-এর object-relational mapping system, যার মাধ্যমে Python models ও QuerySets ব্যবহার করে database operations করা যায়।

Example:

```python
Student.objects.filter(
    department="CSE"
)
```

এটি matching students-এর QuerySet তৈরি করে।

## 71. What is a Database Migration?

**Answer:** Migration হলো database schema changes version-control করার এবং ধারাবাহিকভাবে apply করার পদ্ধতি।

Django example:

```bash
python manage.py makemigrations
python manage.py migrate
```

Production migration-এর আগে compatibility, backup, locking এবং rollback strategy বিবেচনা করতে হয়।

# PART 10: PORTFOLIO AND PRACTICAL PROJECTS

## 72. How would you design an e-commerce database?

**Answer:** প্রথমে entities ও relationships শনাক্ত করব।

Core tables:
- customers
- products
- orders
- order_items
- payments
- inventory

Design considerations:
1. Primary ও foreign keys define করা।
2. Appropriate constraints যোগ করা।
3. Monetary values-এর জন্য suitable decimal type ব্যবহার করা।
4. Order এবং order items-এর relationships design করা।
5. Frequently queried columns-এ indexes বিবেচনা করা।
6. Payment ও inventory operations-এ transaction handling করা।
7. Access control, audit এবং backup strategy তৈরি করা।

## 73. How would you optimize a database for a large dataset?

**Answer:**
1. Query workload বিশ্লেষণ করব।
2. Slow queries identify করব।
3. Execution plans inspect করব।
4. Appropriate indexes design করব।
5. Query ও schema optimization করব।
6. Connection pooling এবং caching বিবেচনা করব।
7. প্রয়োজন হলে partitioning ও read replicas evaluate করব।
8. Benchmark এবং monitoring দিয়ে ফলাফল যাচাই করব।

## 74. How would you ensure database reliability?

**Answer:**
- Automated backups configure করব।
- Restore এবং PITR test করব।
- Replication ও failover strategy তৈরি করব।
- Database health এবং replication lag monitor করব।
- Security permissions সীমিত রাখব।
- Recovery objectives define করব।
- Regular disaster recovery drills চালাব।

# PART 11: FINAL INTERVIEW CHECKLIST

## Beginner Level
- [ ] DBMS vs RDBMS
- [ ] Primary Key vs Foreign Key
- [ ] Database relationships
- [ ] Normalization
- [ ] SQL basics
- [ ] JOINs and aggregations

## Intermediate Level
- [ ] Subqueries and CTEs
- [ ] Window Functions
- [ ] Indexes and constraints
- [ ] Transactions and ACID
- [ ] PostgreSQL data types
- [ ] Views and migrations

## Advanced Level
- [ ] MVCC and WAL
- [ ] Query planner and EXPLAIN ANALYZE
- [ ] Locks and deadlocks
- [ ] Query optimization
- [ ] Backup and PITR
- [ ] Replication and high availability
- [ ] Security and monitoring
- [ ] Distributed systems and sharding

## Practical Preparation
- [ ] Solve 100 SQL problems.
- [ ] Build an e-commerce database.
- [ ] Optimize at least 5 slow queries.
- [ ] Practice PostgreSQL backup and restore.
- [ ] Build a Django + PostgreSQL + Redis project.
- [ ] Publish projects with README files on GitHub.
- [ ] Practice explaining technical decisions in interviews.

---

# Final Study Strategy

প্রতিটি topic-এর জন্য এই sequence অনুসরণ করো:

1. **Theory:** Concept বুঝো।
2. **Notes:** Definition ও important points লেখো।
3. **Questions and Answers:** Interview questions practice করো।
4. **SQL Practice:** নিজে queries লেখো।
5. **Practical Lab:** Database-এ hands-on কাজ করো।
6. **Project:** বাস্তব সমস্যায় concept apply করো।
7. **Revision:** Interview-এর জন্য নিজের ভাষায় explain করো।

**Goal:** Become capable of designing, optimizing, securing, monitoring, backing up, recovering, and operating reliable databases in real-world applications.
