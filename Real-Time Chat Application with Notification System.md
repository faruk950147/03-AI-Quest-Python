# Real-Time Chat Application with Notification System
## Complete Backend Development Notes

**Technology Stack:** Python, Django, Django REST Framework, Django Channels, WebSockets, Redis, PostgreSQL, JWT, JavaScript

---

# 1. Project Overview

A Real-Time Chat Application allows users to communicate with each other instantly without refreshing the webpage.

A notification system informs users when important events happen, such as:

- Receiving a new message.
- Receiving a message while offline.
- Getting a new friend request.
- Being added to a group.
- Receiving a message in a group.
- Receiving a mention.
- Getting an unread message reminder.

### Main Features

1. User Registration and Login.
2. JWT Authentication.
3. One-to-One Chat.
4. Group Chat.
5. Real-Time Messaging.
6. Message Delivery Status.
7. Message Read Status.
8. Typing Indicators.
9. Online/Offline Status.
10. Real-Time Notifications.
11. Unread Message Count.
12. Message History.
13. Pagination.
14. File and Image Sharing.
15. Push Notifications.
16. Notification Read/Unread Status.

---

# 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Backend framework |
| Django REST Framework | REST APIs |
| Django Channels | Asynchronous communication |
| WebSocket | Real-time communication |
| Redis | Channel layer and temporary data |
| PostgreSQL | Database |
| JWT | Authentication |
| JavaScript | Frontend interaction |
| HTML/CSS | User interface |
| Celery | Background tasks |
| Firebase Cloud Messaging | Push notifications |

### Why Django Channels?

Traditional HTTP requests follow a request-response model.

For example:

1. Client sends a request.
2. Server processes the request.
3. Server sends a response.
4. Connection ends.

This is not ideal for real-time chat.

WebSocket maintains a persistent, two-way connection between client and server.

Django Channels allows Django applications to handle WebSocket connections.

---

# 3. HTTP vs WebSocket

## HTTP

- Client sends a request.
- Server returns a response.
- Connection is generally short-lived.
- Useful for CRUD operations.

Example:

GET /api/messages/

## WebSocket

- Client connects to the server.
- Connection stays open.
- Both client and server can send messages.
- Ideal for chat and live notifications.

Example:

ws://localhost:8000/ws/chat/1/

### Communication Flow

Client → WebSocket Connection → Django Channels → Redis → Other Connected Clients

---

# 4. Project Architecture

```text
Frontend (HTML / CSS / JavaScript)
              |
              |
        REST API / WebSocket
              |
              |
        Django Backend
              |
       -----------------
       |               |
       |               |
 Django REST       Django Channels
 Framework              |
       |                 |
       |                Redis
       |                 |
       |          WebSocket Groups
       |                 |
       -----------------
              |
          PostgreSQL
              |
       Chat / Messages /
       Notifications /
       Users
```

### Architecture Responsibilities

**Django REST Framework**
- Registration.
- Login.
- User profiles.
- Chat creation.
- Message history.
- Notification history.

**Django Channels**
- Real-time messaging.
- Typing indicators.
- Online status events.
- Read receipts.
- Real-time notifications.

**Redis**
- Channel layer.
- Cross-process message delivery.
- Temporary online presence.
- Caching.

**PostgreSQL**
- Persistent messages.
- Users.
- Conversations.
- Notifications.
- Message status.

---

# 5. Project Setup

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

## Install Packages

```bash
pip install django
pip install djangorestframework
pip install channels
pip install channels-redis
pip install djangorestframework-simplejwt
pip install psycopg[binary]
pip install pillow
pip install celery
pip install redis
```

## Create Django Project

```bash
django-admin startproject config .
```

Create applications:

```bash
python manage.py startapp accounts
python manage.py startapp chat
python manage.py startapp notifications
```

### Suggested Folder Structure

```text
realtime_chat/
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
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── consumers.py
│
├── chat/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── consumers.py
│   ├── routing.py
│   └── urls.py
│
├── notifications/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── consumers.py
│   └── urls.py
│
├── templates/
├── static/
├── media/
├── manage.py
└── requirements.txt
```

---

# 6. Configure Django Settings

Add applications to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "channels",

    "accounts",
    "chat",
    "notifications",
]
```

Configure ASGI:

```python
ASGI_APPLICATION = "config.asgi.application"
```

Configure Redis Channel Layer:

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

Configure JWT:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

---

# 7. Database Models

## User Model

Use Django's custom user model for long-term flexibility.

```python
# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    is_online = models.BooleanField(default=False)

    last_seen = models.DateTimeField(
        blank=True,
        null=True
    )
```

In settings.py:

```python
AUTH_USER_MODEL = "accounts.User"
```

Important: Configure the custom user model before creating your initial migrations.

## Conversation Model

```python
# chat/models.py

from django.conf import settings
from django.db import models


class Conversation(models.Model):

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations"
    )

    is_group = models.BooleanField(default=False)

    name = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
```

## Message Model

```python
class Message(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    content = models.TextField(blank=True)

    attachment = models.FileField(
        upload_to="chat_files/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_edited = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]
```

## Message Status Model

A message can have different delivery and read states for different recipients.

```python
class MessageStatus(models.Model):

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="statuses"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    is_delivered = models.BooleanField(default=False)

    delivered_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_read = models.BooleanField(default=False)

    read_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["message", "user"],
                name="unique_message_recipient_status"
            )
        ]
```

---

# 8. Notification System

## What Is a Notification?

A notification is an event that informs a user about an activity.

Examples:

- New message received.
- Friend request received.
- Group invitation.
- User mentioned in a message.
- Message reply.

## Notification Model

```python
# notifications/models.py

from django.conf import settings
from django.db import models


class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ("message", "New Message"),
        ("friend_request", "Friend Request"),
        ("group_invite", "Group Invitation"),
        ("mention", "Mention"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPES
    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
```

### Notification Model Explanation

| Field | Purpose |
|---|---|
| recipient | User receiving notification |
| sender | User triggering notification |
| notification_type | Type of event |
| title | Notification title |
| message | Notification description |
| is_read | Read/unread status |
| created_at | Notification creation time |

---

# 9. Django Channels Configuration

## ASGI Configuration

```python
# config/asgi.py

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from chat.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": django_asgi_app,

    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
```

For JWT-authenticated WebSockets, implement custom authentication middleware rather than assuming the default session middleware authenticates JWT tokens.

## WebSocket Routing

```python
# chat/routing.py

from django.urls import path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path(
        "ws/chat/<int:conversation_id>/",
        ChatConsumer.as_asgi()
    ),
]
```

---

# 10. Real-Time Chat Consumer

A Consumer handles WebSocket connections and events.

```python
# chat/consumers.py

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.conversation_id = self.scope["url_route"]["kwargs"][
            "conversation_id"
        ]

        self.room_group_name = f"chat_{self.conversation_id}"

        user = self.scope["user"]

        if not user.is_authenticated:
            await self.close()
            return

        # Verify that this user belongs to this conversation.
        from .models import Conversation

        allowed = await self.user_is_member(
            self.conversation_id,
            user.id
        )

        if not allowed:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)

        message = data.get("message")

        if not message:
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
            }
        )

    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                "message": event["message"]
            })
        )

    @staticmethod
    @database_sync_to_async
    def user_is_member(conversation_id, user_id):

        from .models import Conversation

        return Conversation.objects.filter(
            id=conversation_id,
            participants__id=user_id
        ).exists()
```

Add the missing import:

```python
from channels.db import database_sync_to_async
```

**Important:** This is a basic broadcasting example. A production implementation must save messages to the database, validate message content, create recipient statuses, and broadcast only after the database transaction commits.

---

# 11. Real-Time Message Flow

```text
User A sends message
        |
        v
WebSocket receives message
        |
        v
Validate authentication
        |
        v
Check conversation membership
        |
        v
Validate message content
        |
        v
Save message in PostgreSQL
        |
        v
Create recipient status records
        |
        v
Broadcast through Redis
        |
        v
User B receives message
        |
        v
Update delivery status
        |
        v
User B opens conversation
        |
        v
Update read status
```

### Important Concept

Saving messages in the database is essential.

WebSocket broadcasting alone does not guarantee message persistence.

If a user is offline, the message must still be available when they reconnect.

---

# 12. Real-Time Notification Consumer

Notifications can use a separate WebSocket connection for each authenticated user.

## Notification Routing

```python
# notifications/routing.py

from django.urls import path

from .consumers import NotificationConsumer

websocket_urlpatterns = [
    path(
        "ws/notifications/",
        NotificationConsumer.as_asgi()
    ),
]
```

## Notification Consumer

```python
# notifications/consumers.py

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        user = self.scope["user"]

        if not user.is_authenticated:
            await self.close()
            return

        self.user_group_name = f"user_{user.id}"

        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        if hasattr(self, "user_group_name"):

            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )

    async def send_notification(self, event):

        await self.send_json({
            "type": "notification",
            "notification": event["notification"]
        })
```

Add notification routing to the main ASGI router alongside chat routing.

---

# 13. Sending Notifications

Create a reusable notification service.

```python
# notifications/services.py

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from .models import Notification


def create_notification(
    recipient,
    sender,
    notification_type,
    title,
    message
):

    notification = Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        title=title,
        message=message
    )

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{recipient.id}",
        {
            "type": "send_notification",
            "notification": {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "type": notification.notification_type,
                "is_read": notification.is_read,
                "created_at": notification.created_at.isoformat()
            }
        }
    )

    return notification
```

Usage:

```python
create_notification(
    recipient=user_b,
    sender=user_a,
    notification_type="message",
    title="New Message",
    message="You received a new message."
)
```

Call this service after successfully saving the message.

For reliable production delivery, use `transaction.on_commit()` or a transactional outbox pattern so notifications are not sent for rolled-back database transactions.

---

# 14. Notification API

## Serializer

```python
# notifications/serializers.py

from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification

        fields = [
            "id",
            "sender",
            "notification_type",
            "title",
            "message",
            "is_read",
            "created_at"
        ]
```

## Notification List API

```python
# notifications/views.py

from rest_framework.generics import ListAPIView

from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListAPIView(ListAPIView):

    serializer_class = NotificationSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Notification.objects.filter(
            recipient=self.request.user
        )
```

## Mark Notification as Read

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, pk):

    updated = Notification.objects.filter(
        id=pk,
        recipient=request.user
    ).update(is_read=True)

    if not updated:
        return Response(
            {"error": "Notification not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response({
        "message": "Notification marked as read"
    })
```

## Unread Notification Count

```python
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unread_notification_count(request):

    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    return Response({
        "unread_count": count
    })
```

---

# 15. Frontend WebSocket Connection

## Chat WebSocket

```javascript
const conversationId = 1;

const socket = new WebSocket(
    `ws://localhost:8000/ws/chat/${conversationId}/`
);

socket.onopen = function () {
    console.log("Chat connected");
};

socket.onmessage = function (event) {

    const data = JSON.parse(event.data);

    console.log("New message:", data.message);
};

socket.onclose = function () {
    console.log("Chat disconnected");
};

socket.onerror = function (error) {
    console.error("WebSocket error:", error);
};

function sendMessage(message) {

    if (socket.readyState === WebSocket.OPEN) {

        socket.send(JSON.stringify({
            message: message
        }));

    }
}
```

## Notification WebSocket

```javascript
const notificationSocket = new WebSocket(
    "ws://localhost:8000/ws/notifications/"
);

notificationSocket.onmessage = function (event) {

    const data = JSON.parse(event.data);

    if (data.type === "notification") {

        console.log(
            "New notification:",
            data.notification
        );

    }
};
```

For JWT authentication, send the token through a secure, supported WebSocket authentication mechanism. Browser WebSocket APIs do not allow arbitrary Authorization headers. Avoid placing long-lived JWT tokens in query strings because URLs may be logged.

---

# 16. Typing Indicator

Typing indicators tell other users when someone is writing a message.

Client sends:

```javascript
socket.send(JSON.stringify({
    type: "typing",
    is_typing: true
}));
```

Consumer handles:

```python
if data.get("type") == "typing":

    await self.channel_layer.group_send(
        self.room_group_name,
        {
            "type": "typing_event",
            "user_id": self.scope["user"].id,
            "is_typing": data.get("is_typing", False)
        }
    )
```

Consumer event:

```python
async def typing_event(self, event):

    await self.send_json({
        "type": "typing",
        "user_id": event["user_id"],
        "is_typing": event["is_typing"]
    })
```

Use throttling or debouncing to avoid sending excessive typing events.

---

# 17. Online / Offline Status

Online status tells users whether another user is currently connected.

Possible statuses:

- Online.
- Offline.
- Last seen.

A simple approach:

1. User connects to WebSocket.
2. Track the user's active connections.
3. Set presence to online.
4. User disconnects.
5. Remove the connection.
6. Set offline only when no active connections remain.
7. Update last_seen.

For production systems, manage presence with Redis keys and expiration times.

Do not rely only on a database boolean because a user can have multiple devices or browser tabs.

---

# 18. Message Delivery and Read Receipts

Common chat status indicators:

| Status | Meaning |
|---|---|
| Sent | Message saved successfully |
| Delivered | Recipient device received the message |
| Read | Recipient opened or acknowledged the message |

### Example

```text
User A: Hello

✓  Sent
✓✓ Delivered
✓✓ Read
```

### Read Receipt Flow

1. User B opens conversation.
2. Frontend sends a read event.
3. Backend verifies conversation membership.
4. Backend updates MessageStatus.
5. Backend broadcasts read receipt.
6. User A receives the updated status.

Never trust a client-provided user ID for updating another user's read status. Derive the user from authenticated WebSocket scope.

---

# 19. Push Notifications

WebSocket notifications work while the user has an active connection.

But what happens when the user closes the browser?

Use push notifications.

### Firebase Cloud Messaging (FCM)

FCM can deliver notifications to supported browser and mobile clients.

Typical flow:

```text
New Message
    |
    v
Save Message
    |
    v
Check Recipient Presence
    |
    +------ Online ------> WebSocket Notification
    |
    +------ Offline -----> Push Notification
                              |
                              v
                         FCM Service
                              |
                              v
                         User Device
```

A production application should account for multiple devices, background delivery, notification permissions, invalid device tokens, and duplicate notifications.

---

# 20. API Endpoint Design

## Authentication

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/auth/register/ | Register |
| POST | /api/auth/login/ | Login |
| POST | /api/auth/token/refresh/ | Refresh JWT |
| GET | /api/auth/profile/ | User profile |

## Chat

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/conversations/ | List conversations |
| POST | /api/conversations/ | Create conversation |
| GET | /api/conversations/{id}/ | Conversation details |
| GET | /api/conversations/{id}/messages/ | Message history |
| POST | /api/messages/ | Send message |
| PATCH | /api/messages/{id}/ | Edit message |
| DELETE | /api/messages/{id}/ | Delete message |

## Notifications

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/notifications/ | List notifications |
| GET | /api/notifications/unread-count/ | Unread count |
| PATCH | /api/notifications/{id}/read/ | Mark as read |
| POST | /api/notifications/read-all/ | Mark all as read |

## WebSocket

```text
/ws/chat/<conversation_id>/
/ws/notifications/
```

---

# 21. Database Relationship

```text
User
 |
 |----< ConversationParticipant >---- Conversation
                                         |
                                         |
                                      Message
                                         |
                                         |
                                    MessageStatus
                                         |
                                         |
                                        User


User
 |
 |
Notification
 |
 |
Sender (User)
```

Recommended improvements:

- Use explicit conversation membership models when roles or join dates are needed.
- Add indexes for conversation messages and notification queries.
- Add unique constraints where duplicate relationships are not allowed.
- Use database transactions for message creation and recipient status creation.

---

# 22. Security Best Practices

Security is essential for chat applications.

### Authentication

- Use JWT authentication.
- Validate WebSocket connections.
- Use token expiration.
- Support token refresh.

### Authorization

- Check conversation membership.
- Users must not access other users' messages.
- Users must only read their own notifications.
- Validate group membership before broadcasting.

### Data Protection

- Use HTTPS and WSS in production.
- Validate user input.
- Restrict attachment file types and sizes.
- Store secrets in environment variables.
- Apply rate limiting.
- Avoid exposing private user data.

### WebSocket Security

- Validate the Origin header.
- Authenticate every connection.
- Authorize every conversation.
- Limit connection and message sizes.
- Handle disconnects correctly.
- Avoid trusting client-supplied sender IDs.

---

# 23. Performance Optimization

1. Use Redis for channel layers.
2. Use database indexes.
3. Use pagination for message history.
4. Use `select_related()` and `prefetch_related()`.
5. Use asynchronous consumers where appropriate.
6. Use background tasks for slow operations.
7. Compress and resize uploaded images.
8. Avoid broadcasting unnecessarily.
9. Use database connection pooling when appropriate.
10. Monitor WebSocket connections and Redis memory.

Example:

```python
messages = Message.objects.filter(
    conversation_id=conversation_id
).select_related(
    "sender",
    "conversation"
).order_by("-created_at")[:30]
```

---

# 24. Testing

Test the following:

### Authentication Tests

- User registration.
- Valid login.
- Invalid login.
- JWT expiration.
- Unauthorized WebSocket connection.

### Chat Tests

- Create conversation.
- Send message.
- Receive message.
- Retrieve message history.
- Edit message.
- Delete message.
- Prevent unauthorized access.

### Notification Tests

- Create notification.
- Receive real-time notification.
- Mark as read.
- Get unread count.
- Prevent access to another user's notifications.

### WebSocket Tests

- Connect successfully.
- Disconnect successfully.
- Broadcast to correct group.
- Reject unauthorized connections.
- Handle malformed JSON.
- Reconnect after connection failure.

Django Channels provides `WebsocketCommunicator` for testing WebSocket consumers.

---

# 25. Deployment

Production requirements:

- Django application server using ASGI.
- PostgreSQL database.
- Redis server.
- Nginx reverse proxy.
- HTTPS/WSS.
- Environment variables.
- Static and media storage.
- Logging and monitoring.
- Background workers if using Celery.

Example development commands:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Run Redis separately:

```bash
redis-server
```

For production, use an ASGI server such as Daphne or Uvicorn behind a properly configured reverse proxy.

---

# 26. Interview Questions and Answers

### Q1. What is real-time chat?

A system where users can exchange messages instantly without manually refreshing the page.

### Q2. What is WebSocket?

WebSocket is a communication protocol that provides persistent, bidirectional communication between client and server.

### Q3. What is Django Channels?

Django Channels extends Django to handle WebSockets and other asynchronous protocols.

### Q4. Why use Redis?

Redis is commonly used as a Channels channel layer to distribute events between application processes.

### Q5. What is a Consumer?

A Consumer handles WebSocket connection events, incoming messages, and outgoing events.

### Q6. What is a Channel Layer?

A channel layer allows different application instances and consumers to communicate.

### Q7. What is a WebSocket Group?

A group is a collection of channels that can receive the same broadcast event.

### Q8. How do notifications work?

The backend creates a persistent notification and sends a real-time event to the recipient's user-specific WebSocket group.

### Q9. How do you handle offline users?

Store messages and notifications in the database. When users reconnect, retrieve unread messages and notifications through APIs. Use push notifications for background delivery.

### Q10. What is the difference between sent, delivered, and read?

- Sent: message successfully stored.
- Delivered: recipient device received it.
- Read: recipient acknowledged or opened it.

### Q11. Why use PostgreSQL?

It provides reliable relational data storage, transactions, indexing, and data integrity.

### Q12. Why use Celery?

Celery handles background jobs such as sending emails, push notifications, and processing files.

### Q13. Can WebSocket replace REST API?

No. REST APIs are useful for CRUD operations and retrieving historical data. WebSockets are useful for real-time communication. Most applications benefit from using both.

### Q14. How do you secure a chat application?

Use authentication, authorization, conversation membership checks, HTTPS/WSS, validation, rate limiting, and secure file handling.

### Q15. What happens if Redis goes down?

Real-time group messaging may fail. Persistent database messages remain safe if they were committed. Monitoring, recovery, and retry mechanisms should restore event delivery.

---

# 27. Recommended Development Roadmap

## Phase 1: Foundation

- [ ] Create Django project.
- [ ] Configure PostgreSQL.
- [ ] Create custom User model.
- [ ] Implement registration.
- [ ] Implement JWT login.
- [ ] Create user profile API.

## Phase 2: Chat Backend

- [ ] Create Conversation model.
- [ ] Create Message model.
- [ ] Create MessageStatus model.
- [ ] Implement conversation API.
- [ ] Implement message API.
- [ ] Implement message history.
- [ ] Add pagination.

## Phase 3: Real-Time Communication

- [ ] Install Django Channels.
- [ ] Configure Redis.
- [ ] Configure ASGI.
- [ ] Create ChatConsumer.
- [ ] Implement WebSocket routing.
- [ ] Implement real-time message broadcasting.
- [ ] Implement typing indicators.
- [ ] Implement online/offline presence.

## Phase 4: Notification System

- [ ] Create Notification model.
- [ ] Create NotificationConsumer.
- [ ] Create notification service.
- [ ] Implement notification API.
- [ ] Implement unread notification count.
- [ ] Implement mark-as-read.
- [ ] Implement real-time notification delivery.

## Phase 5: Advanced Features

- [ ] Implement delivery receipts.
- [ ] Implement read receipts.
- [ ] Implement group chat.
- [ ] Implement file sharing.
- [ ] Implement push notifications.
- [ ] Implement message search.
- [ ] Implement message deletion and editing.

## Phase 6: Production

- [ ] Add automated tests.
- [ ] Improve security.
- [ ] Optimize database queries.
- [ ] Configure Redis production environment.
- [ ] Deploy ASGI application.
- [ ] Configure HTTPS/WSS.
- [ ] Add logging and monitoring.

---

# 28. Important Concepts to Remember

| Concept | Meaning |
|---|---|
| REST API | Request-response communication |
| WebSocket | Persistent bidirectional communication |
| ASGI | Asynchronous Server Gateway Interface |
| WSGI | Web Server Gateway Interface |
| Consumer | Handles WebSocket events |
| Channel | Communication endpoint |
| Channel Layer | Consumer-to-consumer communication |
| Group | Collection of channels |
| Redis | In-memory data store and channel layer backend |
| ORM | Object Relational Mapping |
| JWT | JSON Web Token |
| FCM | Firebase Cloud Messaging |
| Celery | Background task processing |
| Read Receipt | Indicates message has been read |
| Delivery Receipt | Indicates message has been delivered |

---

# 29. Final Project Goal

Build a production-oriented Real-Time Chat Application where:

1. Users can register and log in.
2. Users can create one-to-one conversations.
3. Users can create group conversations.
4. Users can exchange messages instantly.
5. Messages are stored in PostgreSQL.
6. Redis distributes real-time events.
7. Users receive notifications instantly.
8. Offline users can retrieve missed messages.
9. Users can track sent, delivered, and read messages.
10. Users can see online/offline status.
11. Users can receive push notifications.
12. All operations are properly authenticated and authorized.

**Final Architecture:**

Django + Django REST Framework + Django Channels + WebSocket + Redis + PostgreSQL + JWT + Celery + FCM.

**Core Principle:** PostgreSQL stores the permanent data, Redis distributes real-time events, WebSocket delivers instant updates, and REST APIs provide reliable access to historical data and application resources.

---

**End of Complete Notes**