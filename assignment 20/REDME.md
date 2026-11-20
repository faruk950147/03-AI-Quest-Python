# Django Real-Time Chat Application — Complete Bangla Explanation

## 1. Project Overview

এই Project-এ Django এবং Django Channels ব্যবহার করে একটি Real-Time Chat Application তৈরি করা হয়েছে।

এখানে ব্যবহার করা হয়েছে:

- Python
- Django
- Django Channels
- WebSocket
- HTML
- Bootstrap
- JavaScript
- Database ORM

### Application কীভাবে কাজ করে?

ধরো, Faruk এবং Rahim একই Chat Room-এ আছে।

Faruk একটি Message পাঠাল:

```text
Hello Rahim!
```

তাহলে:

1. Faruk Message লিখবে।
2. JavaScript WebSocket দিয়ে Message পাঠাবে।
3. Django Channels Message Receive করবে।
4. Consumer Message Validate করবে।
5. Database-এ Message Save হবে।
6. Channel Layer Message Broadcast করবে।
7. একই Room-এর Connected User-রা Message পাবে।
8. JavaScript HTML-এর মধ্যে নতুন Message দেখাবে।

এখানে Page Reload করার প্রয়োজন নেই।

---

# 2. models.py — Database Model

```python
from django.conf import settings
from django.db import models


class Messages(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    room_name = models.CharField(max_length=100)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    class Meta:

        db_table = "chat_messages"

        verbose_name_plural = "messages"

        ordering = ["id"]


    @classmethod
    def last_5_messages(cls, room_name):

        return (
            cls.objects.filter(room_name=room_name)
            .select_related("user")
            .order_by("-id")[:5]
        )


    def __str__(self):

        return self.user.username
```

## Model Explanation

### ForeignKey

```python
user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="messages"
)
```

একটি Message কোন User পাঠিয়েছে সেটি সংরক্ষণ করে।

- `settings.AUTH_USER_MODEL`: Django User Model।
- `on_delete=models.CASCADE`: User Delete হলে তার Messages-ও Delete হবে।
- `related_name="messages"`: User থেকে তার Messages Access করা যাবে।

Example:

```python
user.messages.all()
```

### room_name

```python
room_name = models.CharField(max_length=100)
```

কোন Chat Room-এ Message পাঠানো হয়েছে সেটি সংরক্ষণ করে।

Example:

```text
general
django
python
```

### content

```python
content = models.TextField()
```

Message-এর মূল Text সংরক্ষণ করে।

### created_at

```python
created_at = models.DateTimeField(auto_now_add=True)
```

Message তৈরি হওয়ার সময় Automatically Save হয়।

### updated_at

```python
updated_at = models.DateTimeField(auto_now=True)
```

Message Update হলে Automatically Time Update হয়।

### Meta Class

```python
class Meta:

    db_table = "chat_messages"

    verbose_name_plural = "messages"

    ordering = ["id"]
```

- `db_table`: Database Table-এর নাম নির্ধারণ করে।
- `verbose_name_plural`: Admin Panel-এ Plural Name দেখায়।
- `ordering`: Default Ordering নির্ধারণ করে।

### last_5_messages()

```python
@classmethod
def last_5_messages(cls, room_name):

    return (
        cls.objects.filter(room_name=room_name)
        .select_related("user")
        .order_by("-id")[:5]
    )
```

এই Method নির্দিষ্ট Room-এর সর্বশেষ ৫টি Message নিয়ে আসে।

- `filter()`: নির্দিষ্ট Room-এর Message Filter করে।
- `select_related()`: User-এর Data একই Database Query-তে নিয়ে আসে।
- `order_by("-id")`: সর্বশেষ Message আগে আনে।
- `[:5]`: শুধু ৫টি Message নেয়।

যেহেতু Query সর্বশেষ থেকে পুরোনো ক্রমে আসে, তাই Display করার আগে Reverse করতে হবে।

---

# 3. admin.py — Django Admin Configuration

```python
from django.contrib import admin

from chat.models import Messages


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "room_name",
        "content",
        "created_at",
        "updated_at"
    )

    list_display_links = ("id", "user")

    list_filter = ("room_name", "created_at")

    search_fields = (
        "user__username",
        "room_name",
        "content"
    )

    ordering = ("-id",)

    readonly_fields = (
        "created_at",
        "updated_at"
    )

    list_per_page = 20
```

## Admin Explanation

### list_display

Admin Panel-এ কোন কোন Field দেখাবে সেটি নির্ধারণ করে।

### list_display_links

কোন Field-এ Click করলে Details Page Open হবে সেটি নির্ধারণ করে।

### list_filter

Room এবং Date অনুযায়ী Filter করার সুবিধা দেয়।

### search_fields

Message, Username এবং Room Name দিয়ে Search করা যায়।

### ordering

সর্বশেষ Message আগে দেখায়।

### readonly_fields

Created এবং Updated Time পরিবর্তন করা যাবে না।

### list_per_page

প্রতি Page-এ ২০টি Message দেখাবে।

---

# 4. routing.py — WebSocket URL Routing

```python
from django.urls import path

from chat.consumers import ChatConsumer


websocket_urlpatterns = [

    path(
        "ws/chat/<str:room_name>/",
        ChatConsumer.as_asgi()
    ),

]
```

## Routing Explanation

এটি WebSocket-এর URL নির্ধারণ করে।

Example:

```text
ws://127.0.0.1:8000/ws/chat/general/
```

এখানে:

- `ws://`: WebSocket Protocol।
- `chat`: Chat Endpoint।
- `general`: Room Name।

### Dynamic URL

```python
<str:room_name>
```

এটি Dynamic URL Parameter।

তাই নিচের সব URL একই Consumer ব্যবহার করতে পারবে:

```text
/ws/chat/general/
/ws/chat/django/
/ws/chat/python/
```

শুধু Room Name পরিবর্তন হবে।

### as_asgi()

```python
ChatConsumer.as_asgi()
```

Consumer-কে ASGI Application হিসেবে ব্যবহার করার জন্য প্রস্তুত করে।

---

# 5. views.py — Django HTTP View

```python
from django.shortcuts import render
from django.views import View

from chat.models import Messages


class HomeView(View):

    def get(self, request):

        messages = (
            Messages.objects
            .filter(room_name="general")
            .select_related("user")
            .order_by("-id")[:5]
        )

        context = {

            "messages": reversed(list(messages))

        }

        return render(
            request,
            "chat/home.html",
            context
        )
```

## View Explanation

যখন User Browser থেকে Home Page Visit করবে তখন এই View Execute হবে।

### get()

```python
def get(self, request):
```

Browser থেকে GET Request আসলে এই Method Execute হয়।

### Database Query

```python
messages = (
    Messages.objects
    .filter(room_name="general")
    .select_related("user")
    .order_by("-id")[:5]
)
```

এখানে:

1. General Room-এর Message Filter করা হয়েছে।
2. User-এর Data Load করা হয়েছে।
3. সর্বশেষ Message আগে নেওয়া হয়েছে।
4. সর্বশেষ ৫টি Message নেওয়া হয়েছে।

### Context

```python
context = {
    "messages": reversed(list(messages))
}
```

Python থেকে HTML Template-এ Data পাঠানোর জন্য Context ব্যবহার করা হয়।

Reverse করার কারণে পুরোনো Message আগে এবং নতুন Message পরে দেখাবে।

### render()

```python
return render(
    request,
    "chat/home.html",
    context
)
```

HTML Template Browser-এ Render করে।

---

# 6. urls.py — Django URL Configuration

```python
from django.urls import path

from chat.views import HomeView


urlpatterns = [

    path(
        "",
        HomeView.as_view(),
        name="home"
    ),

]
```

## Explanation

এখানে Home Page-এর URL তৈরি করা হয়েছে।

```python
HomeView.as_view()
```

Class-Based View-কে URL-এর সঙ্গে Connect করে।

---

# 7. consumers.py — Main Chat Engine

এটি পুরো Real-Time Chat Application-এর সবচেয়ে গুরুত্বপূর্ণ অংশ।

Django View সাধারণত HTTP Request Handle করে।

কিন্তু Django Channels Consumer WebSocket Connection Handle করে।

```python
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

import json

from chat.models import Messages


class ChatConsumer(AsyncConsumer):


    # 1. Handle WebSocket Connection
    async def websocket_connect(self, event):

        user = self.scope["user"]

        if not user.is_authenticated:

            await self.send({
                "type": "websocket.close"
            })

            return


        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        self.room_group_name = f"chat_{self.room_name}"


        await self.channel_layer.group_add(

            self.room_group_name,

            self.channel_name

        )


        await self.send({

            "type": "websocket.accept"

        })


        # Get Chat History
        history = await self.get_chat_history()


        await self.send({

            "type": "websocket.send",

            "text": json.dumps({

                "type": "chat_history",

                "messages": history

            })

        })


    # 2. Handle Incoming Messages
    async def websocket_receive(self, event):

        try:

            user = self.scope["user"]

            data = json.loads(
                event.get("text") or "{}"
            )

            message = data.get("message", "")


            if not isinstance(message, str) or not message.strip():

                await self.send_error(
                    "Message cannot be empty"
                )

                return


            message = message.strip()


            if len(message) > 2000:

                await self.send_error(
                    "Message is too long"
                )

                return


            # Save Message
            saved_message = await self.save_message(

                user.id,

                self.room_name,

                message

            )


            # Broadcast Message
            await self.channel_layer.group_send(

                self.room_group_name,

                {

                    "type": "chat.message",

                    "message": saved_message

                }

            )


        except json.JSONDecodeError:

            await self.send_error(
                "Invalid JSON format"
            )


    # 3. Handle Group Messages
    async def chat_message(self, event):

        await self.send({

            "type": "websocket.send",

            "text": json.dumps({

                "type": "chat_message",

                "message": event["message"]

            })

        })


    # 4. Get Chat History
    @database_sync_to_async
    def get_chat_history(self):

        messages = Messages.last_5_messages(
            self.room_name
        )

        return [

            {

                "id": msg.id,

                "user_id": msg.user_id,

                "username": msg.user.username,

                "room_name": msg.room_name,

                "content": msg.content,

                "created_at": msg.created_at.strftime("%I:%M %p")

            }

            for msg in reversed(list(messages))

        ]


    # 5. Save Message
    @database_sync_to_async
    def save_message(self, user_id, room_name, content):

        message = Messages.objects.create(

            user_id=user_id,

            room_name=room_name,

            content=content

        )


        return {

            "id": message.id,

            "user_id": message.user_id,

            "username": message.user.username,

            "room_name": message.room_name,

            "content": message.content,

            "created_at": message.created_at.strftime("%I:%M %p")

        }


    # 6. Send Error
    async def send_error(self, error):

        await self.send({

            "type": "websocket.send",

            "text": json.dumps({

                "type": "error",

                "error": error

            })

        })


    # 7. Handle WebSocket Disconnect
    async def websocket_disconnect(self, event):

        if hasattr(self, "room_group_name"):

            await self.channel_layer.group_discard(

                self.room_group_name,

                self.channel_name

            )
```

---

# 8. Consumer-এর প্রতিটি Method বিস্তারিত

## Step 1: websocket_connect()

```python
async def websocket_connect(self, event):
```

যখন Browser WebSocket Connection তৈরি করবে তখন এই Method Execute হবে।

### User Authentication

```python
user = self.scope["user"]
```

এখানে WebSocket Connection-এর সঙ্গে যুক্ত User পাওয়া যায়।

```python
if not user.is_authenticated:
```

User Login করা আছে কি না Check করে।

Login না থাকলে:

```python
await self.send({
    "type": "websocket.close"
})
```

WebSocket Connection বন্ধ করে।

## Step 2: Room Name

```python
self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
```

URL থেকে Room Name সংগ্রহ করে।

যেমন:

```text
ws/chat/general/
```

তাহলে:

```python
self.room_name = "general"
```

## Step 3: Room Group Name

```python
self.room_group_name = f"chat_{self.room_name}"
```

Room-এর জন্য Channel Group তৈরি করার নাম নির্ধারণ করে।

Example:

```text
chat_general
chat_django
chat_python
```

## Step 4: group_add()

```python
await self.channel_layer.group_add(
    self.room_group_name,
    self.channel_name
)
```

বর্তমান WebSocket Connection-কে নির্দিষ্ট Group-এ Join করায়।

ধরো:

- Faruk General Room-এ Join করেছে।
- Rahim General Room-এ Join করেছে।
- Karim Django Room-এ Join করেছে।

তাহলে:

```text
chat_general

Faruk
Rahim


chat_django

Karim
```

একই Group-এর সবাই Broadcast Message পাবে।

## Step 5: websocket.accept

```python
await self.send({
    "type": "websocket.accept"
})
```

WebSocket Connection Accept করে।

## Step 6: Chat History

```python
history = await self.get_chat_history()
```

Database থেকে আগের Message নিয়ে আসে।

এরপর:

```python
await self.send({
    "type": "websocket.send",
    "text": json.dumps({
        "type": "chat_history",
        "messages": history
    })
})
```

Browser-এ Chat History পাঠায়।

## Step 7: websocket_receive()

```python
async def websocket_receive(self, event):
```

Browser থেকে নতুন Message আসলে এই Method Execute হয়।

JavaScript থেকে পাঠানো Data:

```javascript
chatSocket.send(JSON.stringify({
    message: "Hello Rahim"
}));
```

Consumer এটি Receive করবে।

### JSON Loads

```python
data = json.loads(event.get("text") or "{}")
```

JSON String-কে Python Dictionary-তে Convert করে।

### Message Get

```python
message = data.get("message", "")
```

Dictionary থেকে Message বের করে।

### Message Validation

```python
if not isinstance(message, str) or not message.strip():

    await self.send_error(
        "Message cannot be empty"
    )

    return
```

Check করে:

- Message String কি না।
- Message Empty কি না।
- শুধু Space দেওয়া হয়েছে কি না।

### strip()

```python
message = message.strip()
```

Message-এর সামনে এবং পেছনের Extra Space সরিয়ে দেয়।

### Maximum Length

```python
if len(message) > 2000:
```

২০০০ Character-এর বেশি Message পাঠানো বন্ধ করে।

## Step 8: save_message()

```python
saved_message = await self.save_message(
    user.id,
    self.room_name,
    message
)
```

Message Database-এ Save করার জন্য Method Call করে।

### database_sync_to_async

```python
@database_sync_to_async
```

Django ORM Synchronous হওয়ায় Async Consumer থেকে Database Query চালানোর জন্য এটি ব্যবহার করা হয়।

### Database Create

```python
message = Messages.objects.create(

    user_id=user_id,

    room_name=room_name,

    content=content

)
```

Database-এ নতুন Message তৈরি করে।

### Return Data

```python
return {

    "id": message.id,

    "user_id": message.user_id,

    "username": message.user.username,

    "room_name": message.room_name,

    "content": message.content,

    "created_at": message.created_at.strftime("%I:%M %p")

}
```

Save করা Message-এর তথ্য Dictionary হিসেবে Return করে।

## Step 9: group_send()

```python
await self.channel_layer.group_send(

    self.room_group_name,

    {

        "type": "chat.message",

        "message": saved_message

    }

)
```

এটি একই Group-এর সব Connected User-এর কাছে Message Broadcast করে।

এখানে:

- `room_group_name`: কোন Group-এ পাঠাবে।
- `type`: কোন Consumer Handler Execute হবে।
- `message`: কী Data পাঠাবে।

## Step 10: chat_message()

```python
async def chat_message(self, event):
```

Group থেকে Broadcast Event আসলে এই Method Execute হয়।

```python
await self.send({
    "type": "websocket.send",
    "text": json.dumps({
        "type": "chat_message",
        "message": event["message"]
    })
})
```

প্রতিটি Connected Browser-এ Message পাঠায়।

### গুরুত্বপূর্ণ বিষয়

```python
"type": "chat.message"
```

এটি Channel Layer Event Type।

আর:

```python
async def chat_message(self, event):
```

এটি Consumer Handler Method।

Django Channels Dot (`.`) কে Underscore (`_`) দিয়ে পরিবর্তন করে Handler খুঁজে নেয়।

## Step 11: websocket_disconnect()

```python
async def websocket_disconnect(self, event):
```

যখন User Disconnect করবে তখন এই Method Execute হবে।

```python
await self.channel_layer.group_discard(
    self.room_group_name,
    self.channel_name
)
```

User-কে Group থেকে Remove করে।

---

# 9. home.html — Frontend Structure

HTML Template-এর মূল Layout চারটি অংশে বিভক্ত।

1. Left Sidebar
2. Chat Header
3. Chat Messages
4. Message Footer

## Template Inheritance

```django
{% extends "base.html" %}
```

এটি Base Template Inherit করে।

```django
{% block title %}Chat Room{% endblock title %}
```

Page Title নির্ধারণ করে।

```django
{% block content %}
```

Main Content শুরু করে।

## Left Sidebar

```html
<aside class="col-4 col-lg-3">
```

এটি Chat Application-এর বাম পাশের Sidebar।

এখানে রয়েছে:

- Messages Header
- Search Input
- Conversation List
- User Profile

### Search Input

```html
<input
    type="text"
    id="search-conversations"
    placeholder="Search..."
>
```

Conversation Search করার জন্য Input।

বর্তমানে এটি শুধু HTML Element; Search Functionality তৈরি করতে JavaScript প্রয়োজন।

### Conversation List

Sarah Ahmed, John Smith এবং Emma Wilson বর্তমানে Static HTML Data।

অর্থাৎ এগুলো Database থেকে আসছে না।

## Chat Header

```html
<header>
```

এখানে রয়েছে:

- General Chat Name
- Connection Status
- Call Button
- Video Call Button
- More Options Button

## Chat Messages

```html
<div id="chat-messages">
```

এখানে সব Message Display হবে।

### Django For Loop

```django
{% for message in messages %}
```

View থেকে পাঠানো Messages-এর ওপর Loop চালায়।

### Own Message Check

```django
{% if message.user_id == request.user.id %}
```

বর্তমান Login করা User-এর ID এবং Message-এর User ID একই কি না Check করে।

একই হলে নিজের Message ডান পাশে দেখাবে।

```html
<div class="d-flex justify-content-end mb-3">
```

অন্য User-এর Message হলে বাম পাশে দেখাবে।

```html
<div class="d-flex justify-content-start mb-3">
```

### Empty Message

```django
{% empty %}
```

Database-এ কোনো Message না থাকলে এটি Execute হবে।

তখন:

```text
No messages yet
Start a conversation!
```

দেখাবে।

## Message Footer

```html
<form id="form">
```

এখানে Message Input এবং Send Button রয়েছে।

### Message Input

```html
<input
    type="text"
    id="message-input"
    maxlength="2000"
>
```

User এখানে Message লিখবে।

### Send Button

```html
<button
    type="submit"
    id="send-button"
    disabled
>
```

Message পাঠানোর Button।

`disabled` থাকার কারণে JavaScript থেকে Enable না করা পর্যন্ত Click করা যাবে না।

### CURRENT_USER_ID

```django
<script>
    const CURRENT_USER_ID = {{ request.user.id }};
</script>
```

Django Template থেকে বর্তমান Login করা User-এর ID JavaScript-এ পাঠানো হয়।

JavaScript নিজের Message এবং অন্যের Message আলাদা করতে এটি ব্যবহার করতে পারে।

---

# 10. Complete Message Flow

ধরো Faruk একটি Message পাঠাল:

```text
Hello Rahim!
```

পুরো Process:

### 1. HTML

Faruk Message Input-এ লিখবে।

### 2. JavaScript

JavaScript Message-কে JSON হিসেবে WebSocket দিয়ে পাঠাবে।

```javascript
chatSocket.send(JSON.stringify({
    message: "Hello Rahim!"
}));
```

### 3. Consumer

`websocket_receive()` Message Receive করবে।

### 4. Validation

Message Empty কি না এবং Length ঠিক আছে কি না Check করবে।

### 5. Database

`save_message()` Database-এ Message Save করবে।

### 6. Broadcast

`group_send()` একই Room-এর সবাইকে Message পাঠাবে।

### 7. Handler

`chat_message()` Group Event Receive করবে।

### 8. JavaScript

Browser-এর JavaScript `onmessage` Event দিয়ে Message Receive করবে।

### 9. HTML

JavaScript DOM Update করে নতুন Message Display করবে।

Page Reload করার প্রয়োজন নেই।

---

# 11. Important Django Channels Concepts

| Concept | কাজ |
|---|---|
| Consumer | WebSocket Request Handle করে |
| WebSocket | Persistent Connection তৈরি করে |
| Channel Layer | একাধিক Connection-এর মধ্যে Event আদান-প্রদান করে |
| Group | একাধিক Channel-কে একসঙ্গে রাখে |
| group_add() | Group-এ Join করে |
| group_send() | Group-এ Event Broadcast করে |
| group_discard() | Group থেকে Remove করে |
| self.scope | Connection সম্পর্কিত তথ্য রাখে |
| database_sync_to_async | Async Context থেকে Sync ORM চালায় |
| json.loads() | JSON থেকে Python Dictionary |
| json.dumps() | Python Dictionary থেকে JSON |

---

# 12. Important Improvements

তোমার বর্তমান Project-এ কয়েকটি বিষয় উন্নত করা প্রয়োজন।

## 1. Latest Messages

সর্বশেষ ৫টি Message নিতে:

```python
.order_by("-id")[:5]
```

Display করার আগে Reverse করতে হবে।

## 2. Room Filtering

HomeView-এ:

```python
Messages.objects.filter(room_name="general")
```

ব্যবহার করা উচিত।

এতে অন্য Room-এর Message চলে আসবে না।

## 3. Sidebar Dynamic করা

বর্তমানে Sidebar-এর Friend List Static HTML।

পরবর্তীতে Database থেকে Conversation List আনতে হবে।

## 4. Room Permission

শুধু Login করলেই যেকোনো Room-এ Join করার অনুমতি দেওয়া উচিত নয়।

প্রতিটি Room-এর Access Permission Check করতে হবে।

## 5. Username Query Optimization

Message Save করার পর `message.user.username` Access করলে অতিরিক্ত Database Query হতে পারে।

প্রয়োজনে User-কে `select_related()` দিয়ে Fetch করতে হবে।

## 6. Redis Channel Layer

Production Environment-এ Redis ব্যবহার করা উচিত।

বিশেষ করে একাধিক Django Worker বা Server থাকলে Redis Channel Layer প্রয়োজন।

## 7. Error Handling

Invalid JSON ছাড়াও Database Error, Connection Error এবং অন্যান্য Unexpected Error Handle করা উচিত।

---

# 13. Final Learning Roadmap

এই Project ভালোভাবে বুঝতে নিচের Order অনুসরণ করো।

- [ ] Python OOP
- [ ] Django Models
- [ ] Django ORM
- [ ] ForeignKey Relationship
- [ ] Django Views
- [ ] Django URL Routing
- [ ] Django Templates
- [ ] JavaScript DOM
- [ ] JavaScript JSON
- [ ] WebSocket Basics
- [ ] Django Channels
- [ ] Async and Await
- [ ] Channel Layer
- [ ] Group Broadcast
- [ ] Redis
- [ ] Authentication and Authorization

---

# Conclusion

এই Project-এর মূল উদ্দেশ্য হলো Django Channels এবং WebSocket ব্যবহার করে Real-Time Communication তৈরি করা।

সবচেয়ে গুরুত্বপূর্ণ Consumer Flow:

```text
websocket_connect()
        |
        v
group_add()
        |
        v
get_chat_history()
        |
        v
websocket_receive()
        |
        v
Message Validation
        |
        v
save_message()
        |
        v
group_send()
        |
        v
chat_message()
        |
        v
JavaScript onmessage
        |
        v
Update HTML DOM
```

এই Flow ভালোভাবে বুঝতে পারলে Django Channels ব্যবহার করে Real-Time Chat Application তৈরির মূল ধারণা পরিষ্কার হয়ে যাবে।