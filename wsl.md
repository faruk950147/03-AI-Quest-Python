# Redis Server Setup Using WSL (Windows + Django)

## Introduction

আপনি যদি Windows ব্যবহার করেন এবং Django Project-এ Redis ব্যবহার করতে চান, তাহলে WSL (Windows Subsystem for Linux)-এর ভিতরে Ubuntu ইনস্টল করে Redis Server চালাতে পারবেন।

এতে Windows-এর VS Code, CMD বা Cmder থেকে Django Project চালিয়েও WSL-এর Redis Server ব্যবহার করা সম্ভব।

---

## Step 1: Open WSL / Ubuntu Terminal

Windows CMD, PowerShell অথবা Cmder খুলুন।

```powershell
wsl
```

Ubuntu Terminal ওপেন হবে।

Ubuntu ইনস্টল করা না থাকলে:

```powershell
wsl --install -d Ubuntu
```

ইনস্টলেশন শেষে প্রয়োজনে Windows Restart করুন।

WSL version চেক করুন:

```powershell
wsl --list --verbose
```

---

## Step 2: Update Ubuntu Packages

Ubuntu Terminal-এ রান করুন:

```bash
sudo apt update
```

এরপর:

```bash
sudo apt upgrade -y
```

---

## Step 3: Install Redis Server

```bash
sudo apt install redis-server -y
```

Redis ইনস্টল হয়েছে কিনা চেক করুন:

```bash
redis-server --version
```

---

## Step 4: Start Redis Server

Redis চালু করুন:

```bash
sudo service redis-server start
```

Redis Status চেক করুন:

```bash
sudo service redis-server status
```

Expected status:

```text
active (running)
```

---

## Step 5: Test Redis Connection

Redis CLI ওপেন করুন:

```bash
redis-cli
```

Redis-এর মধ্যে লিখুন:

```redis
PING
```

Expected output:

```text
PONG
```

একটি value Set করুন:

```redis
SET name "Faruk"
```

Value Get করুন:

```redis
GET name
```

Output:

```text
"Faruk"
```

Redis CLI থেকে বের হতে:

```redis
EXIT
```

---

## Step 6: Redis Host and Port

Redis-এর Default Configuration:

| Configuration | Value |
|---|---|
| Host | 127.0.0.1 |
| Port | 6379 |
| Password | None (default configuration) |
| Database | 0 |

Redis URL:

```text
redis://127.0.0.1:6379/0
```

Windows থেকে WSL Redis ব্যবহার করতে সাধারণত localhost forwarding কাজ করে।

---

## Step 7: Install Redis Packages in Django

প্রথমে Django Project-এর Virtual Environment Activate করুন।

Windows CMD / Cmder:

```bash
venv\Scripts\activate
```

Redis Python Client Install:

```bash
pip install redis
```

Django Redis Backend Install:

```bash
pip install django-redis
```

Installed Packages Check:

```bash
pip show redis
pip show django-redis
```

---

## Step 8: Configure Redis in Django settings.py

Django Project-এর settings.py ফাইলে নিচের Configuration যোগ করুন।

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 300,
    }
}
```

### Configuration Explanation

| Setting | Description |
|---|---|
| BACKEND | Django Redis Cache Backend |
| LOCATION | Redis Server URL |
| 127.0.0.1 | Redis Host |
| 6379 | Redis Port |
| /1 | Redis Database Number |
| TIMEOUT | Cache Expiration in Seconds |

---

## Step 9: Test Redis in Django

Django Shell ওপেন করুন:

```bash
python manage.py shell
```

Redis Cache Test:

```python
from django.core.cache import cache

cache.set("username", "Faruk", timeout=300)

cache.get("username")
```

Expected Output:

```python
'Faruk'
```

আরেকটি Test:

```python
cache.set("age", 25)

cache.get("age")
```

Expected Output:

```python
25
```

Delete Cache:

```python
cache.delete("username")
```

Check:

```python
cache.get("username")
```

Expected Output:

```python
None
```

---

## Step 10: Common Redis Commands

| Command | Description |
|---|---|
| PING | Check Redis Connection |
| SET key value | Save Data |
| GET key | Get Data |
| DEL key | Delete Data |
| EXISTS key | Check Key Exists |
| EXPIRE key 60 | Set Expiration |
| TTL key | Check Remaining Time |
| DBSIZE | Count Database Keys |
| INFO | Redis Server Information |
| FLUSHDB | Delete Current Database Data |
| FLUSHALL | Delete All Database Data |
| EXIT | Exit Redis CLI |

### Command Examples

```redis
PING

SET name "Faruk"

GET name

EXISTS name

EXPIRE name 60

TTL name

DEL name

DBSIZE

INFO

EXIT
```

**Warning:** FLUSHDB এবং FLUSHALL ব্যবহার করলে Redis-এর Data Delete হয়ে যাবে।

---

## Step 11: Redis Start, Stop and Restart

### Start Redis

```bash
sudo service redis-server start
```

### Stop Redis

```bash
sudo service redis-server stop
```

### Restart Redis

```bash
sudo service redis-server restart
```

### Check Redis Status

```bash
sudo service redis-server status
```

### Check Redis Process

```bash
ps aux | grep redis
```

### Check Redis Port

```bash
sudo ss -ltnp | grep 6379
```

---

## Step 12: Common Problems and Solutions

### Problem 1: Redis Connection Refused

Error:

```text
redis.exceptions.ConnectionError:
Error 111 connecting to 127.0.0.1:6379.
Connection refused.
```

Solution:

```bash
sudo service redis-server start
```

তারপর Redis পরীক্ষা করুন:

```bash
redis-cli ping
```

Expected:

```text
PONG
```

### Problem 2: Redis Port Already in Use

Error:

```text
Could not create server TCP listening socket
*:6379: bind: Address already in use
```

Check:

```bash
sudo ss -ltnp | grep 6379
```

কোনো Redis instance আগে থেকেই চলছে কিনা দেখুন।

### Problem 3: Redis Server Not Running

Redis Restart করুন:

```bash
sudo service redis-server restart
```

এরপর:

```bash
redis-cli ping
```

### Problem 4: Check Redis Logs

```bash
sudo tail -f /var/log/redis/redis-server.log
```

### Problem 5: Windows Django Cannot Connect to WSL Redis

প্রথমে WSL Ubuntu Terminal-এ পরীক্ষা করুন:

```bash
redis-cli ping
```

এরপর Redis listening address পরীক্ষা করুন:

```bash
sudo ss -ltnp | grep 6379
```

Windows PowerShell থেকে পরীক্ষা করুন:

```powershell
Test-NetConnection 127.0.0.1 -Port 6379
```

যদি `TcpTestSucceeded : True` আসে, তাহলে Windows থেকে Redis Port-এ Connection সম্ভব।

Django settings.py-তে ব্যবহার করুন:

```python
"LOCATION": "redis://127.0.0.1:6379/1"
```

---

## Step 13: Recommended Daily Workflow

### 1. Open Cmder / PowerShell

```powershell
wsl
```

### 2. Start Redis in Ubuntu

```bash
sudo service redis-server start
```

### 3. Verify Redis

```bash
redis-cli ping
```

Expected:

```text
PONG
```

### 4. Open Django Project in Windows

VS Code অথবা Cmder থেকে Django Project ওপেন করুন।

### 5. Activate Virtual Environment

```bash
venv\Scripts\activate
```

### 6. Run Django Server

```bash
python manage.py runserver
```

### 7. Use Redis from Django

```text
redis://127.0.0.1:6379/1
```

---

## Step 14: Complete Installation Commands

Ubuntu Terminal-এ নিচের সব কমান্ড একসঙ্গে চালাতে পারবেন:

```bash
sudo apt update && \
sudo apt upgrade -y && \
sudo apt install redis-server -y && \
sudo service redis-server start && \
redis-cli ping
```

Expected Output:

```text
PONG
```

---

## Step 15: Complete Django Installation Commands

Windows CMD / Cmder-এ Django Project-এর Virtual Environment Activate করে রান করুন:

```bash
pip install redis django-redis
```

তারপর:

```bash
pip freeze > requirements.txt
```

---

## Step 16: Final Checklist

- [ ] WSL Installed
- [ ] Ubuntu Installed
- [ ] Ubuntu Packages Updated
- [ ] Redis Server Installed
- [ ] Redis Server Running
- [ ] Redis CLI Working
- [ ] PING Returns PONG
- [ ] Python Redis Package Installed
- [ ] Django Redis Package Installed
- [ ] Redis Configured in settings.py
- [ ] Django Successfully Connected to Redis
- [ ] Windows Can Access Redis Port 6379

---

## Important Notes

1. Redis Server WSL-এর Ubuntu-তে চলে।
2. Django Project Windows-এ চলতে পারে।
3. WSL-এর localhost forwarding সাধারণত Windows থেকে Redis Access করতে দেয়।
4. Redis-এর Default Port হলো 6379।
5. WSL বন্ধ বা Shutdown হলে Redis Server বন্ধ হয়ে যেতে পারে।
6. WSL আবার চালু করে Redis Status পরীক্ষা করুন।
7. Production Environment-এ Redis-কে Public Network-এ Expose করবেন না।
8. Redis Password এবং Network Security Production-এ সঠিকভাবে Configure করুন।

---

## Final Result

```text
Windows
   |
   |-- Cmder / VS Code
   |
   |-- Django Project
   |      |
   |      |-- django-redis
   |      |
   |      |-- redis-py
   |
   |-- WSL
          |
          |-- Ubuntu
                 |
                 |-- Redis Server
                        |
                        |-- Host: 127.0.0.1
                        |-- Port: 6379
                        |-- Database: 1
```

**Congratulations!**

আপনার Windows + WSL + Ubuntu + Redis + Django Development Environment প্রস্তুত।
