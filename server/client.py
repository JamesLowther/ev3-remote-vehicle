import asyncio
import websockets
import json

async def hello():
    async with websockets.connect("ws://24.199.72.202:6666") as websocket:
        await websocket.send(json.dumps({"type": "init"}))
        await websocket.send(json.dumps({"forward": True}))
        input()

def main():
    asyncio.run(hello())

if __name__ == "__main__":
    main()
