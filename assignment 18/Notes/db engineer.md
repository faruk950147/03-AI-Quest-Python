# Database Engineer Roadmap (Beginner to Advanced)

## 1. Database Fundamentals (Week 1–2)

### 1.1 Database Basics
- What is Data?
- What is a Database?
- What is DBMS?
- What is RDBMS?
- Relational vs Non-relational Database
- Database Schema and Instance
- Tables, Rows, Columns, Records, Fields
- Data Types
- Primary Key
- Foreign Key
- Candidate Key
- Composite Key
- Unique Key
- Constraints
- NULL Values

### 1.2 Database Relationships
- One-to-One Relationship
- One-to-Many Relationship
- Many-to-Many Relationship
- Entity-Relationship (ER) Diagram
- Entities and Attributes
- Referential Integrity

### 1.3 Database Theory
- Functional Dependency
- Super Key and Candidate Key
- Normalization
- First Normal Form (1NF)
- Second Normal Form (2NF)
- Third Normal Form (3NF)
- Boyce-Codd Normal Form (BCNF)
- Denormalization

### Practice Project
- Student Management Database
- Library Management Database
- University Management Database

---

## 2. SQL Mastery (Week 3–7)

### 2.1 Basic SQL
- SELECT
- FROM
- WHERE
- DISTINCT
- ORDER BY
- LIMIT
- OFFSET
- INSERT
- UPDATE
- DELETE
- CREATE
- ALTER
- DROP
- TRUNCATE
- Data Types
- Type Casting
- AND, OR, NOT
- IN, BETWEEN, LIKE
- IS NULL

### 2.2 Intermediate SQL
- Aggregate Functions
- COUNT()
- SUM()
- AVG()
- MIN()
- MAX()
- GROUP BY
- HAVING
- INNER JOIN
- LEFT JOIN
- RIGHT JOIN
- FULL OUTER JOIN
- CROSS JOIN
- SELF JOIN
- Subqueries
- Correlated Subqueries
- CASE
- COALESCE
- NULLIF
- UNION
- UNION ALL
- INTERSECT
- EXCEPT

### 2.3 Advanced SQL
- Common Table Expressions (CTE)
- Recursive CTE
- Window Functions
- ROW_NUMBER()
- RANK()
- DENSE_RANK()
- LAG()
- LEAD()
- Running Totals
- Conditional Aggregation
- EXISTS
- NOT EXISTS
- Date and Time Functions
- JSON/JSONB Queries

### 2.4 SQL Problem Solving
- Easy SQL Problems
- Intermediate SQL Problems
- Advanced SQL Problems
- Interview-Focused SQL Problems
- Top-N Queries
- Second-Highest Salary
- Duplicate Records
- Ranking and Aggregation Problems

### Practice Platforms
- SQLBolt: https://sqlbolt.com/
- HackerRank SQL: https://www.hackerrank.com/domains/sql
- LeetCode Database: https://leetcode.com/problemset/database/

### Milestone
- Solve 50–100 SQL problems.
- Build tables and relationships independently.
- Write complex queries using JOINs, CTEs, and Window Functions.

---

## 3. PostgreSQL (Week 8–11)

### 3.1 PostgreSQL Fundamentals
- PostgreSQL Installation
- PostgreSQL Architecture
- psql Command-Line Tool
- pgAdmin
- DBeaver
- Database Creation
- Schema Creation
- Table Creation
- Data Types
- Constraints
- Sequences
- Identity Columns

### 3.2 PostgreSQL Database Objects
- Tables
- Views
- Materialized Views
- Indexes
- Functions
- Stored Procedures
- Triggers
- Schemas
- Temporary Tables
- Generated Columns
- JSONB
- Arrays

### 3.3 PostgreSQL Transactions
- BEGIN
- COMMIT
- ROLLBACK
- SAVEPOINT
- ACID Properties
- Transaction Isolation Levels
- Read Committed
- Repeatable Read
- Serializable
- Locking
- Deadlocks
- Concurrent Transactions

### 3.4 Database Migrations
- Schema Migrations
- Forward Migrations
- Rollback Migrations
- Version-Controlled Schema
- Safe Schema Changes
- Backward-Compatible Migrations
- Django Migrations
- Alembic
- Zero-Downtime Migration Concepts

### Practice Project
Build a University Management Database using PostgreSQL.

Include:
- Students
- Departments
- Teachers
- Courses
- Enrollments
- Constraints
- Relationships
- Views
- Transactions
- Migration Scripts

Official Documentation:
https://www.postgresql.org/docs/current/

---

## 4. Database Internals (Week 12–16)

### 4.1 Storage Internals
- Database Pages
- Heap Tables
- Disk Storage
- B-Tree Data Structure
- Buffer Cache
- Shared Buffers
- Write-Ahead Logging (WAL)
- Checkpoints
- MVCC
- Vacuum
- Autovacuum
- Database Statistics
- Query Planner

### 4.2 Database Indexing
- B-Tree Index
- Hash Index
- Composite Index
- Partial Index
- Expression Index
- Covering Index
- INCLUDE Index
- GIN Index
- GiST Index
- BRIN Index
- Index Selectivity
- Index-Only Scan
- Index Maintenance
- Indexing Best Practices

### 4.3 Query Optimization
- EXPLAIN
- EXPLAIN ANALYZE
- Sequential Scan
- Index Scan
- Index-Only Scan
- Nested Loop Join
- Hash Join
- Merge Join
- Cardinality Estimation
- Table Statistics
- Query Planner
- Join Optimization
- Sort Optimization
- Aggregate Optimization
- Slow Query Analysis
- N+1 Query Problem
- Connection Pooling

### 4.4 Concurrency Control
- Shared Locks
- Exclusive Locks
- Row-Level Locks
- Table-Level Locks
- Deadlocks
- Dirty Reads
- Non-Repeatable Reads
- Phantom Reads
- Lost Updates
- Optimistic Concurrency
- Pessimistic Concurrency
- Serialization Failures
- Transaction Retry Handling

### 4.5 Performance Benchmarking
- Dataset Generation
- pgbench
- Query Latency
- Throughput
- Transactions Per Second (TPS)
- p50, p95, p99 Latency
- CPU Monitoring
- Memory Monitoring
- Disk I/O Monitoring
- Benchmarking Before and After Optimization

### Practice Project
Database Performance Optimization Lab.

Tasks:
- Create a large orders table.
- Identify slow queries.
- Analyze execution plans.
- Create appropriate indexes.
- Optimize SQL queries.
- Compare query performance before and after optimization.
- Document benchmark results.

---

## 5. Database Administration and Reliability (Week 17–20)

### 5.1 Database Security
- Authentication
- Database Users and Roles
- GRANT
- REVOKE
- Least-Privilege Principle
- Schema Permissions
- Row-Level Security (RLS)
- SSL/TLS
- Secrets Management
- Encryption at Rest
- SQL Injection Prevention
- Audit Logging

### 5.2 Backup and Recovery
- Logical Backup
- Physical Backup
- pg_dump
- pg_restore
- SQL Dumps
- Base Backups
- WAL Archiving
- Point-in-Time Recovery (PITR)
- Recovery Point Objective (RPO)
- Recovery Time Objective (RTO)
- Backup Retention
- Restore Testing
- Disaster Recovery

### 5.3 Replication and High Availability
- Streaming Replication
- Primary and Standby Servers
- Synchronous Replication
- Asynchronous Replication
- Replication Lag
- WAL Shipping
- Failover
- Switchover
- Replication Slots
- Read Replicas
- Split-Brain Risks
- High Availability Architecture
- Failover Testing

### 5.4 Database Maintenance
- VACUUM
- ANALYZE
- Autovacuum Tuning
- Table Bloat
- Index Bloat
- Connection Limits
- Connection Pool Sizing
- Disk Capacity Planning
- Log Rotation
- Database Upgrades
- Maintenance Windows
- Monitoring
- Alerting

### 5.5 Monitoring Tools
- pg_stat_activity
- pg_stat_statements
- PostgreSQL Logs
- Prometheus
- Grafana
- Metrics Collection
- Alert Configuration
- Database Health Checks

### Practice Project
Build a Reliable PostgreSQL Infrastructure.

Tasks:
- Configure PostgreSQL primary and standby servers.
- Implement backup and restore.
- Practice point-in-time recovery.
- Test replication and failover.
- Configure monitoring.
- Create a disaster recovery runbook.

---

## 6. NoSQL and Distributed Databases (Week 21–24)

### 6.1 Redis
- Key-Value Data Model
- Strings
- Hashes
- Lists
- Sets
- Sorted Sets
- TTL
- Eviction Policies
- Cache-Aside Pattern
- Cache Invalidation
- Cache Stampede Prevention
- Persistence
- Replication

### 6.2 MongoDB
- Documents
- Collections
- BSON Data Types
- Schema Design
- Embedding vs Referencing
- Indexes
- Aggregation Pipeline
- Replica Sets
- Sharding
- MongoDB Transactions

### 6.3 Distributed Systems
- Distributed Database Concepts
- Replication Strategies
- Partitioning
- Sharding
- Consistency Models
- Eventual Consistency
- CAP Theorem
- Quorums
- Leader Election
- Distributed Transactions
- Idempotency
- Retry Strategies
- Timeouts
- Duplicate Event Handling

### 6.4 Advanced Database Technologies
- Apache Cassandra
- ClickHouse
- Elasticsearch
- Apache Kafka
- DuckDB
- Vector Databases

### Practice Project
Implement Redis caching in a Django application.

Tasks:
- Cache frequently requested data.
- Configure TTL.
- Implement cache invalidation.
- Measure cache hit ratio.
- Compare response latency with and without caching.

---

## 7. Linux, Cloud and DevOps (Week 25–28)

### 7.1 Linux Fundamentals
- Linux Filesystem
- File Permissions
- Users and Groups
- Processes and Signals
- grep
- find
- tail
- less
- awk
- ps
- top
- free
- df
- du
- Networking Commands
- TCP/IP
- DNS
- Ports and Firewalls
- TLS
- Systemd
- Service Logs
- Bash Scripting

### 7.2 Docker
- Docker Images
- Docker Containers
- Docker Compose
- Persistent Volumes
- Environment Variables
- Container Networking
- Health Checks
- Resource Limits
- Database Initialization
- Persistent Storage
- Container Recovery

### 7.3 AWS Cloud Database
- Amazon RDS
- Amazon Aurora
- Amazon DynamoDB
- Read Replicas
- Multi-AZ Deployments
- VPC
- Subnets
- Security Groups
- IAM
- CloudWatch
- Snapshots
- Automated Backups
- Database Monitoring

AWS RDS:
https://aws.amazon.com/rds/

AWS Skill Builder:
https://skillbuilder.aws/

### 7.4 Infrastructure Automation
- Git
- GitHub
- CI/CD
- Terraform Basics
- Infrastructure as Code
- Secrets Management
- Automated Migrations
- Backup Verification
- Monitoring Alerts
- Configuration Management

### 7.5 Python Database Automation
- Database Health-Check Scripts
- Backup Verification
- Slow Query Report Generation
- Database Connection Monitoring
- Data Quality Checks
- Migration Validation
- Scheduled Maintenance Scripts

### Practice Project
Deploy PostgreSQL in a cloud environment.

Include:
- Secure Database Access
- Automated Backups
- Monitoring and Alerts
- Database Migrations
- Recovery Instructions
- Infrastructure Documentation

---

## 8. Advanced Database Engineering (Week 29–30 and Beyond)

### 8.1 Data Architecture
- OLTP vs OLAP
- Data Warehouses
- Data Lakes
- Star Schema
- Snowflake Schema
- Fact Tables
- Dimension Tables
- Slowly Changing Dimensions (SCD)
- ETL vs ELT
- Change Data Capture (CDC)
- Event-Driven Architecture
- Data Reconciliation

### 8.2 Large-Scale Database Design
- Vertical Scaling
- Horizontal Scaling
- Read Scaling
- Write Scaling
- Partitioning Strategies
- Sharding Strategies
- Hot Partitions
- Multi-Tenant Database Design
- Distributed Transactions
- Connection Pooling at Scale
- Cost and Latency Trade-Offs

### 8.3 Advanced PostgreSQL
- WAL Internals
- Checkpoint Tuning
- Logical Replication
- Replication Slots
- Declarative Partitioning
- Advanced Index Types
- Query Planner Statistics
- PostgreSQL Extensions
- Major Version Upgrades
- PostgreSQL Source Code Fundamentals

---

## 9. Portfolio Projects (Week 31–32)

### Project 1: E-commerce Database
- Database Schema Design
- ER Diagram
- Customers, Products, Orders and Payments
- Normalization
- Foreign Keys and Constraints
- Indexes
- Complex SQL Queries
- Sales Reports
- Transaction Management

### Project 2: Database Performance Optimization
- Large Sample Dataset
- Slow Query Identification
- Query Execution Plan Analysis
- Index Optimization
- SQL Query Optimization
- Before-and-After Benchmarks
- Performance Report

### Project 3: Reliable PostgreSQL Infrastructure
- Primary and Standby Replication
- Backup and Restore
- Point-in-Time Recovery
- Failure Simulation
- Recovery Testing
- Monitoring
- Access Control
- Disaster Recovery Documentation

### Project 4: Production-Style Backend Database
- Django REST Framework
- PostgreSQL
- Redis Caching
- Connection Pooling
- Safe Database Migrations
- Docker Deployment
- Database Monitoring
- Security and Performance Testing

### GitHub Portfolio Requirements
- README.md
- Architecture Diagram
- ER Diagram
- SQL Scripts
- Sample Dataset Instructions
- Setup Guide
- Deployment Guide
- Benchmark Results
- Backup and Recovery Guide
- Security Considerations

---

## 10. Complete 32-Week Study Plan

| Week | Topics |
|---|---|
| 1 | DBMS, RDBMS, Database Concepts |
| 2 | ER Diagrams, Keys, Relationships, Normalization |
| 3 | SELECT, Filtering, Sorting, Data Types |
| 4 | DML, DDL, Constraints |
| 5 | JOINs and Aggregate Functions |
| 6 | Subqueries, CTEs, Set Operations |
| 7 | Window Functions and SQL Problems |
| 8 | PostgreSQL Installation and Tools |
| 9 | Schema Design and Constraints |
| 10 | Transactions and Isolation Levels |
| 11 | Views, Functions, Triggers, Migrations |
| 12 | Storage, Pages, B-Tree, WAL |
| 13 | Index Design and EXPLAIN ANALYZE |
| 14 | Query Plans, Joins, Statistics |
| 15 | MVCC, Locks, Deadlocks |
| 16 | Benchmarking and Performance Project |
| 17 | Database Security and Permissions |
| 18 | Backup and Restore |
| 19 | WAL, PITR, Replication |
| 20 | Monitoring, Failover, Maintenance |
| 21 | Redis and Caching |
| 22 | MongoDB and Data Modeling |
| 23 | Sharding and Consistency |
| 24 | Distributed Systems Project |
| 25 | Linux and Networking |
| 26 | Docker and Docker Compose |
| 27 | AWS RDS and Cloud Networking |
| 28 | Python Automation and Infrastructure |
| 29 | Advanced Database Architecture |
| 30 | Partitioning, CDC, OLTP/OLAP |
| 31 | Portfolio Projects and Documentation |
| 32 | SQL Interviews and Job Applications |

Estimated duration: 8 months at approximately 8–12 study hours per week. Adjust the schedule based on your current knowledge and project progress.

---

## 11. Daily Study Routine

Recommended daily schedule: 2 hours.

- 25 minutes: Theory and Documentation
- 45 minutes: SQL or Database Lab
- 30 minutes: Problem Solving and Debugging
- 20 minutes: Notes, GitHub and Revision

Weekly goals:
- Complete one practical task.
- Solve SQL problems.
- Review previous concepts.
- Document what you learned.
- Commit code and scripts to GitHub.

---

## 12. Free Learning Resources

### PostgreSQL
https://www.postgresql.org/docs/current/

### SQLBolt
https://sqlbolt.com/

### HackerRank SQL
https://www.hackerrank.com/domains/sql

### LeetCode Database
https://leetcode.com/problemset/database/

### Use The Index, Luke!
https://use-the-index-luke.com/

### CMU Database Systems Course
https://15445.courses.cs.cmu.edu/

### AWS RDS
https://aws.amazon.com/rds/

### AWS Skill Builder
https://skillbuilder.aws/

---

## 13. Database Engineer Interview Preparation

### SQL
- JOINs
- GROUP BY and HAVING
- Subqueries
- CTEs
- Window Functions
- Top-N Queries
- Second-Highest Salary
- Duplicate Records
- Ranking Problems

### Database Design
- Normalization
- Primary Key vs Unique Key
- Foreign Keys
- Referential Integrity
- Index Design
- Composite Index Column Order

### Database Internals
- B-Tree
- Index Scans
- Query Planner
- EXPLAIN ANALYZE
- MVCC
- WAL
- Vacuum and Autovacuum

### Transactions and Concurrency
- ACID Properties
- Isolation Levels
- Locks and Deadlocks
- Lost Updates
- Serialization Failures

### Database Operations
- Backup and Recovery
- PITR
- Replication
- Failover
- Monitoring
- Connection Pooling
- Database Security

### Distributed Systems
- Replication vs Sharding
- Consistency Models
- CAP Theorem
- Partitioning
- Idempotency
- Distributed Transactions

---

## 14. Recommended Career Path

### Database Engineer
Focus on:
- SQL
- PostgreSQL
- Database Design
- Query Optimization
- Database Internals
- Reliability

### Database Administrator (DBA)
Focus on:
- Backup and Recovery
- Replication
- Monitoring
- Security
- Availability
- Disaster Recovery

### Data Engineer
Focus on:
- Python
- SQL
- ETL/ELT
- Data Pipelines
- Apache Kafka
- Apache Spark
- Data Warehousing

### Cloud Database Engineer
Focus on:
- PostgreSQL
- AWS RDS
- Cloud Networking
- IAM
- Terraform
- Monitoring
- Replication
- Disaster Recovery

---

## 15. Final Learning Order

Follow this order for the best foundation:

1. SQL Mastery
2. PostgreSQL
3. Database Design and Normalization
4. Indexing and Query Optimization
5. Transactions and Concurrency
6. Database Internals
7. Backup, Recovery and Replication
8. Linux and Networking
9. Docker and Cloud Databases
10. Python Automation
11. Advanced Database Architecture
12. Real-World Projects
13. Interview Preparation
14. Job Applications

**Final Goal:** Build strong SQL skills, understand PostgreSQL deeply, create real-world database projects, demonstrate performance optimization, and develop reliable database operations skills.

Remember: Learn one database deeply before moving to multiple technologies. Practical labs, documentation and measurable project results are more valuable than simply completing courses.