# Django WebSocket + Channels — Complete Notes

---

# 1. WebSocket কী?

**WebSocket** হলো এমন একটি communication protocol যা client এবং server-এর মধ্যে **persistent, full-duplex (bidirectional) connection** তৈরি করে।

একবার connection তৈরি হওয়ার পর client এবং server উভয় পক্ষই প্রয়োজন অনুযায়ী data পাঠাতে পারে।

সহজভাবে:

```text
Client  ←────────────→  Server
       Persistent
       Connection
```

WebSocket-এর সবচেয়ে বড় সুবিধা হলো **প্রতিবার নতুন HTTP request করার প্রয়োজন হয় না**।

---

# 2. Django-তে WebSocket কেন ব্যবহার করা হয়?

Django application-এ WebSocket ব্যবহার করা হয় **real-time communication**-এর জন্য।

অর্থাৎ, server থেকে নতুন data এলে page reload না করেই client-এ data পাঠানো যায়।

### Common Use Cases

```text
Live Chat
Real-time Notifications
Real-time Dashboard
Online User Status
Live Tracking
Gaming
Live Updates
Collaborative Applications
```

### Example

একজন user chat message পাঠাল:

```text
User A
   ↓
WebSocket
   ↓
Server
   ↓
WebSocket
   ↓
User B
```

User B-এর browser refresh করার প্রয়োজন নেই।

---

# 3. WebSocket কীভাবে কাজ করে?

প্রথমে সাধারণত HTTP connection-এর মাধ্যমে WebSocket connection establish করার জন্য handshake করা হয়।

তারপর connection WebSocket protocol-এ upgrade হয়।

Basic flow:

```text
Client
   │
   │ WebSocket Handshake
   ▼
Server
   │
   │ Connection Established
   ▼
WebSocket Connection
   │
   ├──────────────→ Client
   │
   ←────────────── Server
   │
   └──────────────→ Client
```

Connection খোলা থাকা অবস্থায় দুই দিক থেকেই message পাঠানো যায়।

---

# 4. HTTP vs WebSocket

| বিষয়                            | HTTP                                      | WebSocket                         |
| ------------------------------- | ----------------------------------------- | --------------------------------- |
| Connection                      | Request/response ভিত্তিক                  | Persistent connection             |
| Communication                   | Request → Response                        | Bidirectional                     |
| Server নিজে message পাঠাতে পারে | সাধারণ request-এর response হিসেবে         | হ্যাঁ                             |
| Real-time communication         | সাধারণভাবে polling/other techniques দরকার | হ্যাঁ                             |
| Common use                      | REST API, Web pages                       | Chat, notifications, live updates |

### HTTP

```text
Client
   ↓ Request
Server
   ↓ Response
Client
```

প্রয়োজন হলে আবার নতুন request:

```text
Client
   ↓ Request
Server
   ↓ Response
Client
```

### WebSocket

```text
Client
   ↕
   ↕ Persistent Connection
   ↕
Server
```

Connection established হওয়ার পর উভয় পক্ষ message পাঠাতে পারে।

---

# 5. Django কি সরাসরি WebSocket Support করে?

Traditional Django request/response framework মূলত HTTP-এর জন্য তৈরি।

WebSocket এবং অন্যান্য asynchronous protocols ব্যবহারের জন্য সাধারণত **Django Channels** ব্যবহার করা হয়।

## Django Channels

**Django Channels** Django application-কে WebSocket এবং অন্যান্য asynchronous communication use case handle করার ক্ষমতা দেয়।

Architecture:

```text
Browser
   ↓
WebSocket
   ↓
ASGI
   ↓
Django Channels
   ↓
Consumer
```

---

# 6. ASGI কী?

Django-এর traditional WSGI interface মূলত synchronous HTTP application-এর জন্য ব্যবহৃত হয়।

**ASGI (Asynchronous Server Gateway Interface)** asynchronous applications এবং WebSocket-এর মতো protocols support করার জন্য ব্যবহৃত হয়।

Architecture:

```text
Client
   ↓
ASGI Server
   ↓
Django / Channels
   ↓
Consumer
```

Django project-এ সাধারণত:

```python
ASGI_APPLICATION = "project_name.asgi.application"
```

ব্যবহার করা হয়।

---

# 7. Django Channels Install

Virtual environment activate করে:

```bash
pip install channels
```

Redis channel layer ব্যবহার করতে চাইলে:

```bash
pip install channels-redis
```

---

# 8. `settings.py` Configuration

`settings.py`-তে:

```python
INSTALLED_APPS = [
    # ...
    "channels",
]
```

এবং:

```python
ASGI_APPLICATION = "project_name.asgi.application"
```

### Important

`project_name`-এর জায়গায় আপনার Django project package-এর নাম দিতে হবে।

যেমন project-এর নাম যদি হয়:

```text
config
```

তাহলে:

```python
ASGI_APPLICATION = "config.asgi.application"
```

---

# 9. `asgi.py` Configuration

Project-এর:

```text
project_name/asgi.py
```

ফাইলে:

```python
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import app.routing


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "project_name.settings",
)


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),

        "websocket": AuthMiddlewareStack(
            URLRouter(
                app.routing.websocket_urlpatterns
            )
        ),
    }
)
```

---

# 10. `ProtocolTypeRouter` কী?

`ProtocolTypeRouter` incoming connection-এর protocol অনুযায়ী request সঠিক application-এর কাছে পাঠায়।

Example:

```text
             Client
                │
                ▼
      ProtocolTypeRouter
          /           \
         /             \
       HTTP         WebSocket
        │               │
        ▼               ▼
     Django          Channels
```

Configuration:

```python
ProtocolTypeRouter(
    {
        "http": get_asgi_application(),

        "websocket": ...,
    }
)
```

অর্থাৎ:

```text
HTTP       → Django
WebSocket  → Channels
```

---

# 11. `AuthMiddlewareStack` কী?

```python
AuthMiddlewareStack(...)
```

WebSocket connection-এর সঙ্গে Django authentication/session information ব্যবহারের সুবিধা দেয়।

এটি ব্যবহার করলে consumer-এ authenticated user পাওয়া যায়:

```python
self.scope["user"]
```

Example:

```python
def connect(self):
    user = self.scope["user"]

    print(user)

    self.accept()
```

---

# 12. Routing

App-এর ভিতরে:

```text
app/
├── routing.py
├── consumers.py
└── ...
```

`routing.py`:

```python
from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path(
        "ws/chat/",
        consumers.ChatConsumer.as_asgi(),
    ),
]
```

এখানে:

```text
/ws/chat/
```

হলো WebSocket endpoint।

---

# 13. Consumer কী?

**Consumer** হলো WebSocket-এর মূল application logic যেখানে connection, incoming message এবং disconnect handle করা হয়।

সহজভাবে:

```text
WebSocket Request
       ↓
    Consumer
       ↓
Connection / Message Logic
```

---

# 14. `WebsocketConsumer`

একটি basic synchronous consumer:

```python
import json

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)

        message = data["message"]

        self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )
```

---

# 15. `connect()` Method

```python
def connect(self):
    self.accept()
```

Client WebSocket connection তৈরি করলে:

```text
Client
   ↓
connect()
   ↓
accept()
   ↓
Connection Established
```

`accept()` connection গ্রহণ করে।

---

# 16. `receive()` Method

Client থেকে message এলে:

```python
def receive(self, text_data):
```

এই method call হয়।

Example incoming JSON:

```json
{
    "message": "Hello Server"
}
```

Python-এ:

```python
data = json.loads(text_data)

message = data["message"]
```

---

# 17. `send()` Method

Server থেকে client-এ message পাঠাতে:

```python
self.send(
    text_data=json.dumps(
        {
            "message": message,
        }
    )
)
```

Flow:

```text
Client
   │
   │ "Hello"
   ▼
Server
   │
   │ "Hello"
   ▼
Client
```

---

# 18. `disconnect()` Method

Client connection বন্ধ করলে:

```python
def disconnect(self, close_code):
    pass
```

এই method call হয়।

`close_code` connection কেন বন্ধ হয়েছে তার code ধারণ করতে পারে।

---

# 19. Frontend JavaScript

Browser থেকে WebSocket connection তৈরি:

```javascript
const socket = new WebSocket(
    "ws://127.0.0.1:8000/ws/chat/"
);
```

---

# 20. `onopen`

Connection successfully established হলে:

```javascript
socket.onopen = function () {
    socket.send(
        JSON.stringify({
            message: "Hello Server",
        })
    );
};
```

Flow:

```text
Browser
   ↓
WebSocket Connect
   ↓
Server accepts
   ↓
onopen()
   ↓
Send message
```

---

# 21. `onmessage`

Server থেকে message এলে:

```javascript
socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    console.log(data.message);
};
```

Server যদি পাঠায়:

```json
{
    "message": "Hello Client"
}
```

Browser:

```text
Hello Client
```

দেখাবে।

---

# 22. Complete Basic WebSocket Flow

```text
                 Browser
                    │
                    │ WebSocket
                    ▼
                Django ASGI
                    │
                    ▼
              Protocol Router
                    │
                    ▼
                Consumer
                    │
             ┌──────┴──────┐
             │             │
          Receive         Send
             │             │
             ▼             ▼
          Message        Response
             │             │
             └──────┬──────┘
                    ▼
                 Browser
```

---

# 23. Complete Example

## `consumers.py`

```python
import json

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)

        message = data["message"]

        self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )
```

## `routing.py`

```python
from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path(
        "ws/chat/",
        consumers.ChatConsumer.as_asgi(),
    ),
]
```

## `asgi.py`

```python
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import app.routing


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "project_name.settings",
)


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),

        "websocket": AuthMiddlewareStack(
            URLRouter(
                app.routing.websocket_urlpatterns
            )
        ),
    }
)
```

## `settings.py`

```python
INSTALLED_APPS = [
    # ...
    "channels",
]

ASGI_APPLICATION = "project_name.asgi.application"
```

## Frontend JavaScript

```javascript
const socket = new WebSocket(
    "ws://127.0.0.1:8000/ws/chat/"
);

socket.onopen = function () {
    socket.send(
        JSON.stringify({
            message: "Hello Server",
        })
    );
};

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    console.log(data.message);
};
```

---

# 24. Important Limitation of This Basic Example

উপরের `ChatConsumer` শুধু **যে client message পাঠিয়েছে, সেই client-কে response পাঠাচ্ছে**।

অর্থাৎ:

```text
User A
   ↓
Consumer
   ↓
User A
```

এটি এখনো real multi-user chat নয়।

Multi-user chat-এর জন্য **Channel Layer এবং Groups** ব্যবহার করা হয়।

---

# 25. Channel Layer কী?

Channel Layer হলো একটি communication system যা বিভিন্ন consumer/process-এর মধ্যে message পাঠাতে সাহায্য করে।

Production environment-এ Redis-এর মাধ্যমে Channel Layer ব্যবহার করা খুব common।

Architecture:

```text
Consumer A
    │
    ▼
Channel Layer
    │
    ▼
Redis
    │
    ▼
Channel Layer
    │
    ▼
Consumer B
```

---

# 26. Redis + Channels

Install:

```bash
pip install channels-redis
```

`settings.py`:

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": (
            "channels_redis.core.RedisChannelLayer"
        ),
        "CONFIG": {
            "hosts": [
                ("127.0.0.1", 6379),
            ],
        },
    },
}
```

Architecture:

```text
Browser
   ↓
WebSocket
   ↓
Django Channels
   ↓
Redis Channel Layer
   ↓
Other Consumers
```

---

# 27. Groups

একটি chat room-এর users-দের একই group-এ রাখা যায়।

Example:

```text
Chat Room: "room1"

       Redis
         │
    ┌────┼────┐
    ▼    ▼    ▼
 User A User B User C
```

যখন User A message পাঠায়:

```text
User A
   ↓
Consumer
   ↓
room1 group
   ↓
User B
User C
```

User A-সহ group-এর সবাই message পেতে পারে, যদি application logic অনুযায়ী broadcast করা হয়।

---

# 28. Group-based Chat Consumer

একটি simplified synchronous example:

```python
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = "chat_room"

        async_to_sync(
            self.channel_layer.group_add
        )(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, close_code):

        async_to_sync(
            self.channel_layer.group_discard
        )(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data):

        data = json.loads(text_data)

        message = data["message"]

        async_to_sync(
            self.channel_layer.group_send
        )(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
            },
        )

    def chat_message(self, event):

        message = event["message"]

        self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )
```

এখানে:

```python
group_add()
```

consumer-কে group-এ যোগ করে।

```python
group_discard()
```

consumer-কে group থেকে সরিয়ে দেয়।

```python
group_send()
```

group-এর consumers-দের message পাঠায়।

---

# 29. Async Consumer

Channels-এ asynchronous consumer-ও ব্যবহার করা যায়।

Example:

```python
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)

        message = data["message"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )
```

---

# 30. Sync vs Async Consumer

### `WebsocketConsumer`

```python
class ChatConsumer(WebsocketConsumer):
```

Synchronous style।

### `AsyncWebsocketConsumer`

```python
class ChatConsumer(AsyncWebsocketConsumer):
```

Asynchronous style।

Async consumer বিশেষভাবে useful যখন application-এ asynchronous operations বেশি থাকে।

> শুধু `AsyncWebsocketConsumer` ব্যবহার করলেই সব ক্ষেত্রে performance automatically ভালো হবে—এমন নয়। Async code-এর সুবিধা আসে যখন workload এবং I/O operations asynchronousভাবে handle করা হয়।

---

# 31. WebSocket URL

Development-এ:

```javascript
const socket = new WebSocket(
    "ws://127.0.0.1:8000/ws/chat/"
);
```

Production-এ HTTPS ব্যবহার করলে সাধারণত:

```javascript
const socket = new WebSocket(
    "wss://example.com/ws/chat/"
);
```

### Difference

```text
ws://
→ WebSocket

wss://
→ Secure WebSocket
```

`wss://` সাধারণত TLS/HTTPS-এর মতো encrypted connection ব্যবহার করে।

---

# 32. Real-Time Notification Example

একটি notification system:

```text
Database Event
      ↓
Django
      ↓
Channel Layer
      ↓
Redis
      ↓
WebSocket
      ↓
Browser
      ↓
New Notification
```

Browser page reload না করেই notification পেতে পারে।

---

# 33. Online User Status

WebSocket connection ব্যবহার করে online/offline status track করা যেতে পারে।

Example:

```text
User A connects
      ↓
WebSocket connected
      ↓
User A = Online
```

Connection বন্ধ হলে:

```text
WebSocket disconnected
      ↓
User A = Offline
```

Production system-এ online presence design করার সময় reconnects, multiple tabs/devices, timeouts এবং stale connections বিবেচনা করতে হয়।

---

# 34. Production Architecture

একাধিক Django/Channels instance থাকলে Redis Channel Layer ব্যবহার করা যেতে পারে।

```text
                    Load Balancer
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Django/Channels 1      Django/Channels 2
             │                       │
             └───────────┬───────────┘
                         ▼
                       Redis
                         │
                Channel Layer
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
          Client A                Client B
```

Redis helps different application instances communicate through the channel layer.

---

# 35. Important Production Considerations

Production WebSocket systems should consider:

```text
Redis
ASGI server
Reverse proxy
TLS / WSS
Authentication
Authorization
Connection management
Reconnection handling
Scaling
Monitoring
Logging
Resource limits
```

WebSocket application-এর ক্ষেত্রে সাধারণ HTTP request-এর পাশাপাশি **long-lived connections** manage করতে হয়।

---

# 36. WebSocket Security

WebSocket application-এ authentication এবং authorization গুরুত্বপূর্ণ।

শুধু connection establish হলেই user-এর সব resource access করার অনুমতি দেওয়া উচিত নয়।

Example:

```text
Authenticated User
        ↓
WebSocket Connection
        ↓
Authorization Check
        ↓
Allowed Resource
```

Sensitive chat room বা private notification system হলে user কোন room/resource access করতে পারবে তা server-side verify করা উচিত।

---

# 37. Common Mistakes

## Mistake 1 — শুধু `channels` install করলেই সব হয়ে যাবে ভাবা

প্রয়োজন হতে পারে:

```text
channels
ASGI configuration
routing
consumer
frontend WebSocket code
```

আর multi-instance/group communication-এর জন্য:

```text
channels-redis
Redis
```

---

## Mistake 2 — Redis ছাড়া multi-instance architecture চালানোর চেষ্টা

Single-process development-এ simple setup সম্ভব হলেও production multi-instance Channels deployment-এর জন্য shared channel layer প্রয়োজন হতে পারে।

Redis একটি common choice।

---

## Mistake 3 — WebSocket এবং HTTP এক জিনিস ভাবা

HTTP:

```text
Request → Response
```

WebSocket:

```text
Persistent Connection
        ↕
Bidirectional Messages
```

---

## Mistake 4 — Basic consumer-কে full chat system ভাবা

এই code:

```python
self.send(...)
```

মূলত current WebSocket connection-এ response পাঠায়।

Multi-user chat-এর জন্য সাধারণত:

```text
Channel Layer
+
Groups
+
Redis
```

প্রয়োজন হয়।

---

# 38. Complete Architecture

```text
                         Browser
                            │
                            │ WebSocket
                            ▼
                    Reverse Proxy / Server
                            │
                            ▼
                    Django ASGI / Channels
                            │
                     ┌──────┴──────┐
                     │             │
                     ▼             ▼
                 Consumer       Consumer
                     │             │
                     └──────┬──────┘
                            ▼
                    Redis Channel Layer
                            │
                     ┌──────┴──────┐
                     ▼             ▼
                  Client A      Client B
```

---

# 39. Quick Revision

### WebSocket

```text
Persistent
Bidirectional
Real-time communication
```

### Django Channels

```text
Django
   ↓
ASGI
   ↓
Channels
   ↓
WebSocket
```

### Consumer

```text
WebSocket connection
        ↓
Consumer
        ↓
Application logic
```

### Channel Layer

```text
Consumer
   ↓
Channel Layer
   ↓
Other Consumers
```

### Redis

```text
Channels
   ↓
Redis Channel Layer
   ↓
Shared communication
```

### Group

```text
Group
 ├── User A
 ├── User B
 └── User C
```

A message can be broadcast to all members of the group.

---

# 40. One-Line Definitions

```text
WebSocket
→ A persistent, bidirectional communication protocol.

Django Channels
→ A Django project that adds support for WebSockets and other non-HTTP/asynchronous communication patterns.

ASGI
→ The interface used by Python applications/frameworks to communicate with asynchronous-capable servers and protocols.

Consumer
→ The application component that handles a WebSocket connection and its events.

Channel Layer
→ A communication layer that allows Channels consumers to exchange messages.

Redis
→ A common backend for the Channels channel layer.

Group
→ A named collection of channel connections that can receive broadcast messages.

ws://
→ WebSocket connection.

wss://
→ Secure WebSocket connection.
```

---

# Final Mental Model

```text
                     USER BROWSER
                          │
                          │ WebSocket
                          ▼
                    Django ASGI
                          │
                          ▼
                  Django Channels
                          │
                          ▼
                      Consumer
                          │
                          ▼
                  Channel Layer
                          │
                          ▼
                        Redis
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
          Consumer A              Consumer B
              │                       │
              ▼                       ▼
           User A                  User B
```

### Remember:

```text
HTTP
→ Request / Response

WebSocket
→ Persistent + Bidirectional

Channels
→ Django WebSocket handling

Consumer
→ WebSocket logic

Redis
→ Shared Channel Layer backend

Group
→ Broadcast communication

ASGI
→ WebSocket-capable application interface
```

1. Database Models (A to Z)
models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# User Profile for Online/Offline status
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"

# Room Model
class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('private', 'Private'),
        ('group', 'Group'),
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    participants = models.ManyToManyField(User, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.room_type == 'private':
            return f"Private Room ({self.id})"
        return self.name or f"Group Room ({self.id})"

# Message Model
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    delivered = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"

# Explanation:

Room → Private (1-to-1) এবং Group chat handle করবে।
participants → Room-এর সকল user থাকবে।
Message → content, sender, delivered, seen, timestamp track করবে।
Profile → online/offline status track করবে।
2. Channels Routing
routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
3. WebSocket Consumer (A to Z)
consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Room, Message, Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.channel_layer.group_add('online_users', self.user.username)
        await self.accept()

        # Set user online
        await self.set_user_online(self.user)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.channel_layer.group_discard('online_users', self.user.username)
        await self.set_user_offline(self.user)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data['message']

        # Save message in DB
        message = await self.save_message(self.user, message_text, self.room_name)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender': self.user.username,
                'message_id': message.id,
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'message_id': event['message_id'],
        }))

    # Database operations
    @database_sync_to_async
    def save_message(self, sender, message_text, room_name):
        room = Room.objects.get(id=room_name)
        return Message.objects.create(room=room, sender=sender, content=message_text)

    @database_sync_to_async
    def set_user_online(self, user):
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.is_online = True
        profile.save()

    @database_sync_to_async
    def set_user_offline(self, user):
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.is_online = False
        profile.save()

# Explanation:

Connect → user join করবে room এবং online_users group-এ add হবে।
Disconnect → user leave করবে এবং offline set হবে।
Receive → message DB-এ save করে room group-এ পাঠানো হবে।
Seen / Delivered logic WebSocket মাধ্যমে real-time update করা যাবে।
4. Frontend (JavaScript + WebSocket)
<div id="chat-log"></div>
<input id="chat-message-input" type="text">
<button id="chat-message-send">Send</button>

<script>
let roomName = "{{ room.id }}";
let ws = new WebSocket('ws://' + window.location.host + '/ws/chat/' + roomName + '/');

ws.onmessage = function(e) {
    let data = JSON.parse(e.data);
    let log = document.getElementById('chat-log');
    log.innerHTML += `<b>${data.sender}:</b> ${data.message} <small id="msg_${data.message_id}">Delivered</small><br>`;
};

// Send message
document.getElementById('chat-message-send').onclick = function() {
    let input = document.getElementById('chat-message-input');
    ws.send(JSON.stringify({'message': input.value}));
    input.value = '';
};
</script>
Give feedback

# Explanation:

নতুন message আসলে log update হবে।
Delivered / Seen status track করা যাবে message ID দিয়ে।
Online users আলাদা API/WebSocket group দিয়ে দেখানো যাবে।

এইভাবে তুমি পুরো Private/Group chat system A to Z তৈরি করতে পারবে, যেটা WhatsApp-এর মতো:

DB save
Seen / Delivered
Online / Offline
Real-time WebSocket integration

Faruk, চাইলে আমি পরবর্তী step-এ দেখাতে পারি Group chat admin, emojis, notifications, typing indicator, একেবারে pro WhatsApp style। 🔥