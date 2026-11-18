# Django Channels – Complete Private Chat Application Notes
## Beginner to Advanced | Production Level
Django Channels – Project Types List
    Chat Application Types
1. Private Chat (One-to-One)
2. Group Chat
3. Public Chat Room
4. Team Chat
5. Customer Support Chat
6. Anonymous Chat
7. Broadcast Chat
8. Community Chat
9. Encrypted Chat
10. Live Chat
2. Chat Features
11. Real-Time Messaging
12. Typing Indicator
13. Online / Offline Status
14. Last Seen
15. Message Sent Status
16. Message Delivered Status
17. Message Seen Status
18. Unread Message Counter
19. Message Reply
20. Message Forward
21. Message Reaction
22. Message Edit
23. Message Delete
24. Message Search
25. Image Sharing
26. File Sharing
27. Audio Message
28. Video Sharing
29. Voice Calling
30. Video Calling
3. Real-Time Applications
31. Real-Time Notification System
32. Live Dashboard
33. Live Data Monitoring
34. Live Stock Dashboard
35. Live Cryptocurrency Tracker
36. Live Auction System
37. Live Bidding System
38. Live Polling System
39. Live Voting System
40. Real-Time Analytics
4. Collaboration Applications
41. Collaborative Document Editor
42. Collaborative Code Editor
43. Real-Time Whiteboard
44. Team Collaboration System
45. Project Management System
46. Live Task Management
47. Shared Workspace
48. Collaborative Drawing App
5. Location-Based Applications
49. Live Location Tracking
50. Real-Time Vehicle Tracking
51. Food Delivery Tracking
52. Ride Sharing Tracking
53. Courier Tracking
6. Other Applications
54. Multiplayer Online Game
55. Live Quiz Application
56. Online Examination Monitoring
57. Live Sports Scoreboard
58. Real-Time Customer Support Dashboard
59. IoT Device Monitoring
60. Smart Home Monitoring System

মোট: ৬০টি Project Type / Feature Idea

পরামর্শ: প্রথমে ১–১০ নম্বর Chat Application তৈরি করো। এরপর ৩১–৬০ নম্বর Real-Time Application নিয়ে কাজ করো।
---

# 1. Project Overview

Django Channels ব্যবহার করে একটি Real-Time Private Chat Application তৈরি করব।

### Main Features

- User Registration
- User Login / Logout
- One-to-One Private Chat
- Real-Time Messaging
- Message History
- Online / Offline Status
- Typing Indicator
- Message Sent Status
- Message Delivered Status
- Message Seen Status
- Unread Message Count
- User Search
- Image Sharing
- File Sharing
- Message Editing
- Message Deletion
- Real-Time Notifications
- Multiple Device Support
- Secure WebSocket Connection

---

# 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Django | Backend Framework |
| Django Channels | WebSocket Management |
| ASGI | Async Server Interface |
| WebSocket | Real-Time Communication |
| Redis | Channel Layer |
| PostgreSQL | Database |
| JavaScript | WebSocket Client |
| HTML | Structure |
| Bootstrap 5 | UI |
| Docker | Containerization |
| Nginx | Reverse Proxy |
| Daphne / Uvicorn | ASGI Server |

---

# 3. Types of Chat Applications

### 3.1 Private Chat
- One-to-One Messaging
- User A to User B
- Private Room
- Message History

### 3.2 Group Chat
- Multiple Users
- Group Creation
- Add / Remove Members
- Group Admin
- Group Messages

### 3.3 Public Chat
- Public Rooms
- Anyone Can Join
- Live Messaging

### 3.4 Customer Support Chat
- Customer and Agent
- Agent Assignment
- Support Tickets
- Live Communication

---

# 4. Complete Learning Roadmap

## Phase 1 – Django Foundation

1. Django Project Setup
2. Django Apps
3. Custom User Model
4. Authentication
5. Django Models
6. ForeignKey Relationships
7. Database Migrations
8. Django ORM
9. User Permissions

## Phase 2 – WebSocket Fundamentals

1. HTTP vs WebSocket
2. What is ASGI?
3. What is WSGI?
4. What is Django Channels?
5. WebSocket Handshake
6. WebSocket Connection
7. WebSocket Disconnect
8. Async and Await
9. Consumer
10. WebSocket Routing

## Phase 3 – Private Chat

1. Chat Room Model
2. Chat Participant Model
3. Message Model
4. Private Room Creation
5. WebSocket Authentication
6. Private Room Authorization
7. AsyncWebsocketConsumer
8. Channel Layer
9. Group Add
10. Group Send
11. Group Discard
12. Database Message Saving
13. Message History

## Phase 4 – Intermediate Features

1. Online / Offline Status
2. Typing Indicator
3. Message Sent Status
4. Message Delivered Status
5. Message Seen Status
6. Unread Message Count
7. User Search
8. Message Pagination
9. Notification System

## Phase 5 – Advanced Features

1. Image Sharing
2. File Sharing
3. Audio Sharing
4. Message Editing
5. Message Deletion
6. Multiple Device Support
7. WebSocket Reconnection
8. Connection Management
9. Message Ordering
10. Error Handling

## Phase 6 – Production Level

1. Redis Configuration
2. PostgreSQL Optimization
3. WebSocket Security
4. Authentication and Authorization
5. Rate Limiting
6. Input Validation
7. Logging
8. Testing
9. Docker
10. Nginx
11. Daphne / Uvicorn
12. HTTPS / WSS
13. Production Deployment
14. Monitoring
15. Scaling

---

# 5. HTTP vs WebSocket

## HTTP

HTTP follows a Request-Response model.

Example:

1. Client sends request.
2. Server receives request.
3. Server processes request.
4. Server sends response.
5. Connection generally closes or is reused.

## WebSocket

WebSocket provides persistent, two-way communication.

Example:

1. Client connects to server.
2. Server accepts connection.
3. Client sends message.
4. Server receives message.
5. Server broadcasts message to another connected client.

### Difference

| HTTP | WebSocket |
|---|---|
| Request-Response | Two-way Communication |
| Traditional Web APIs | Real-Time Applications |
| Client Initiates Request | Both Can Send Data |
| Short-lived Request | Persistent Connection |

---

# 6. What is Django Channels?

Django Channels extends Django to support asynchronous protocols such as WebSockets.

### Main Components

- ASGI Application
- Consumer
- Routing
- Channel Layer
- Redis
- WebSocket

### Architecture

Client A → WebSocket → Consumer → Channel Layer → Consumer → WebSocket → Client B

---

# 7. Project Structure

```text
private_chat/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── chat/
│   ├── models.py
│   ├── consumers.py
│   ├── routing.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── templates/
│   ├── base.html
│   ├── accounts/
│   └── chat/
│       └── private_chat.html
│
├── static/
│   ├── css/
│   └── js/
│       └── chat.js
│
├── media/
│
├── requirements.txt
└── manage.py
```

---

# 8. Installation

```bash
mkdir private_chat
cd private_chat

python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install packages:

```bash
pip install django
pip install channels
pip install channels-redis
pip install daphne
pip install psycopg
pip install pillow
```

Create project:

```bash
django-admin startproject config .
```

Create apps:

```bash
python manage.py startapp accounts
python manage.py startapp chat
```

---

# 9. Django Settings

In settings.py:

```python
INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "channels",

    "accounts",
    "chat",
]
```

Configure ASGI:

```python
ASGI_APPLICATION = "config.asgi.application"
```

Redis Channel Layer:

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

---

# 10. Important Django Channels Concepts

## ASGI

Asynchronous Server Gateway Interface.

It allows Django to handle asynchronous communication, including WebSockets.

## Consumer

Consumer handles WebSocket events.

Important methods:

- connect()
- disconnect()
- receive()
- receive_json()
- send()
- send_json()

## Routing

Routing determines which Consumer handles a WebSocket URL.

## Channel Layer

Channel Layer allows different Consumers to communicate with each other.

## Redis

Redis is commonly used as a production-capable Channel Layer backend.

---

# 11. WebSocket Routing

chat/routing.py:

```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/chat/(?P<room_id>\d+)/$",
        consumers.PrivateChatConsumer.as_asgi()
    ),
]
```

---

# 12. ASGI Configuration

config/asgi.py:

```python
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,

    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
```

---

# 13. Database Design

## User

Use Django's Custom User Model or the built-in User Model.

Fields:

- id
- username
- email
- password

## ChatRoom

Fields:

- id
- room_type
- created_at

## ChatParticipant

Fields:

- id
- room
- user
- joined_at

## Message

Fields:

- id
- room
- sender
- content
- timestamp
- is_read

### Relationships

```text
User
  |
  | One-to-Many
  |
ChatParticipant
  |
  | Many-to-One
  |
ChatRoom
  |
  | One-to-Many
  |
Message
```

A private room should have exactly two authorized participants.

---

# 14. Consumer Architecture

A PrivateChatConsumer should handle:

1. WebSocket Connection
2. Authentication
3. Room Authorization
4. Group Membership
5. Message Receiving
6. Message Saving
7. Message Broadcasting
8. Disconnect Handling

### Important Channel Layer Methods

```python
await self.channel_layer.group_add(
    self.room_group_name,
    self.channel_name
)
```

```python
await self.channel_layer.group_send(
    self.room_group_name,
    {
        "type": "chat_message",
        "message": "Hello"
    }
)
```

```python
await self.channel_layer.group_discard(
    self.room_group_name,
    self.channel_name
)
```

---

# 15. Private Chat Message Flow

```text
User A
  |
  | WebSocket Connection
  |
PrivateChatConsumer
  |
  | Authentication
  |
Room Authorization
  |
  | Group Add
  |
Redis Channel Layer
  |
  | Group Send
  |
User B Consumer
  |
  | WebSocket
  |
User B
```

### Message Flow

1. User A opens a private conversation.
2. WebSocket connects to the private room.
3. Server authenticates User A.
4. Server verifies room membership.
5. User A sends a message.
6. Consumer validates the message.
7. Message is saved to PostgreSQL.
8. Channel Layer broadcasts the event.
9. User B receives the message.
10. User A and User B can see the updated conversation.

---

# 16. JavaScript WebSocket

```javascript
const protocol = window.location.protocol === "https:"
    ? "wss:"
    : "ws:";

const chatSocket = new WebSocket(
    `${protocol}//${window.location.host}/ws/chat/1/`
);

chatSocket.onopen = function () {
    console.log("Connected");
};

chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log(data);
};

chatSocket.onclose = function () {
    console.log("Disconnected");
};

chatSocket.onerror = function (error) {
    console.error("WebSocket Error:", error);
};
```

Send message:

```javascript
chatSocket.send(JSON.stringify({
    "message": "Hello"
}));
```

---

# 17. Message Status System

A Messenger-like application can implement these states:

| Status | Meaning |
|---|---|
| Sent | Message saved successfully |
| Delivered | Recipient's client received it |
| Seen | Recipient opened or read it |

Important: Sent, Delivered, and Seen should be implemented as separate states. Saving a message does not automatically mean it has been delivered or seen.

---

# 18. Online / Offline Status

Possible implementation:

- Track active WebSocket connections.
- Maintain per-user connection state.
- Update online status when the first connection opens.
- Update offline status when the last connection closes.
- Use Redis for shared presence state in multiple server instances.

Do not mark a user offline just because one of their devices disconnects.

---

# 19. Typing Indicator

Example WebSocket event:

```json
{
    "type": "typing",
    "is_typing": true
}
```

When typing stops:

```json
{
    "type": "typing",
    "is_typing": false
}
```

Typing events should not be saved as chat messages.

---

# 20. Security

Production applications must implement:

- Authenticated WebSocket Connections
- Room Membership Validation
- Origin Validation
- HTTPS / WSS
- Input Validation
- Message Length Limits
- File Upload Validation
- Rate Limiting
- Permission Checks
- Secure Session Cookies
- Protection Against Unauthorized Room Access

Never trust a room ID supplied by the frontend without checking the current user's membership.

---

# 21. Production Deployment

### Production Stack

```text
Browser
   |
   | HTTPS / WSS
   |
Nginx
   |
   | Reverse Proxy
   |
Daphne / Uvicorn
   |
Django ASGI
   |
   |----------------|
   |                |
PostgreSQL        Redis
   |
Media Storage
```

### Production Checklist

- DEBUG = False
- Configure ALLOWED_HOSTS
- Configure trusted CSRF origins
- Configure WebSocket origin validation
- Use PostgreSQL
- Use Redis
- Configure HTTPS
- Configure Secure Cookies
- Configure Static Files
- Configure Media Storage
- Set up Logging
- Set up Monitoring
- Run Database Migrations
- Test WebSocket Connections
- Configure Backups
- Configure Docker
- Configure Nginx

---

# 22. Testing

Test these scenarios:

1. User A connects successfully.
2. User B connects successfully.
3. User A sends a private message.
4. User B receives the message.
5. Unauthorized User C cannot access the room.
6. Messages persist after reconnecting.
7. Offline User B receives unread messages after reconnecting.
8. Multiple devices work correctly.
9. Invalid messages are rejected.
10. WebSocket reconnects after network failure.

---

# 23. Final Project Milestones

| Level | Project |
|---|---|
| Beginner | Basic WebSocket Chat |
| Beginner | Private Chat |
| Intermediate | Message History |
| Intermediate | Online Status |
| Intermediate | Typing Indicator |
| Advanced | Read Receipts |
| Advanced | Media Sharing |
| Advanced | Notifications |
| Production | Redis |
| Production | PostgreSQL |
| Production | Docker |
| Production | Nginx |
| Production | Deployment |

---

# 24. Official Documentation

- Django: https://docs.djangoproject.com/
- Django Channels: https://channels.readthedocs.io/
- Redis: https://redis.io/docs/latest/
- PostgreSQL: https://www.postgresql.org/docs/
- Docker: https://docs.docker.com/
- MDN WebSocket: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket

---

# Final Goal

Build a complete, secure, scalable, production-ready Private Chat Application using:

Python + Django + Django Channels + WebSocket + Redis + PostgreSQL + JavaScript.

Learning approach:

1. Understand the concept.
2. Write the code.
3. Understand every line.
4. Test the feature.
5. Handle errors.
6. Add security.
7. Optimize performance.
8. Deploy to production.

**Important:** এই Notes হলো সম্পূর্ণ Project-এর Master Roadmap। প্রতিটি Phase-এর বাস্তব কোড, Models, Consumers, Routing, JavaScript এবং Tests আলাদাভাবে Implement করতে হবে।
