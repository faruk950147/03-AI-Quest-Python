
from django.utils import timezone
from datetime import timedelta
from utils.redis import redis_client

ONLINE_TIMEOUT_SECONDS = 60
ACCOUNT_LOCK_MINUTES = 15
MAX_FAILED_ATTEMPTS = 5

def set_user_online(user_id):
    redis_client.setex(f"user:online:{user_id}", ONLINE_TIMEOUT_SECONDS, 1)

def is_user_online(user_id):
    return redis_client.exists(f"user:online:{user_id}") == 1

def refresh_last_seen(user_id):
    redis_client.set(f"user:last_seen:{user_id}", timezone.now().timestamp())
    set_user_online(user_id)

def get_last_seen(user_id):
    ts = redis_client.get(f"user:last_seen:{user_id}")
    if not ts:
        return None
    return timezone.datetime.fromtimestamp(float(ts), tz=timezone.utc)

def lock_user(user_id):
    unlock_time = timezone.now() + timedelta(minutes=ACCOUNT_LOCK_MINUTES)
    redis_client.set(f"user:lock:{user_id}", unlock_time.timestamp())

def is_user_locked(user_id):
    value = redis_client.get(f"user:lock:{user_id}")
    if not value:
        return False
    return timezone.now().timestamp() < float(value)

def add_failed_attempt(user_id):
    key = f"user:fail:{user_id}"
    attempts = redis_client.incr(key)
    if attempts == 1:
        redis_client.expire(key, 900)
    if attempts >= MAX_FAILED_ATTEMPTS:
        lock_user(user_id)

def reset_failed_attempts(user_id):
    redis_client.delete(f"user:fail:{user_id}")
