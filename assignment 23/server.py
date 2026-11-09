
import asyncio
import websockets


async def handle_client(websocket):
    print("Client connected!")

    try:
        async for message in websocket:
            print(f"Received: {message}")

            await websocket.send(
                f"Server received: {message}"
            )

    finally:
        print("Client disconnected!")


async def main():
    async with websockets.serve(
        handle_client,
        "localhost",
        8765
    ):
        print("WebSocket server running...")
        await asyncio.Future()


asyncio.run(main())
