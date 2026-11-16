import asyncio
from channels_redis.core import RedisChannelLayer


async def test_group():
    layer = RedisChannelLayer(hosts=["redis://127.0.0.1:6379/3"])

    channel = await layer.new_channel()
    group_name = "test_chat_group"

    try:
        # Add channel to group
        await layer.group_add(group_name, channel)
        print("Group Add: SUCCESS")

        # Send message to group
        await layer.group_send(
            group_name, {"type": "chat.message", "text": "Hello from Group!"}
        )
        print("Group Send: SUCCESS")

        # Receive message
        result = await layer.receive(channel)
        print("Group Received:", result)

        # Remove channel from group
        await layer.group_discard(group_name, channel)
        print("Group Discard: SUCCESS")

    finally:
        pass


if __name__ == "__main__":
    asyncio.run(test_group())
