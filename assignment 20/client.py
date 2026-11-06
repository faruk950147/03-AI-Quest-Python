
import asyncio
import websockets


async def main():
    async with websockets.connect(
        "ws://localhost:8765"
    ) as websocket:

        await websocket.send("Hello Server!")

        response = await websocket.recv()

        print(f"Server response: {response}")


asyncio.run(main())
