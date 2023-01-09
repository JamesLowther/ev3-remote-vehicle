import asyncio
import json
import websockets
import moves

class WebsocketsServer():

    def __init__(self, port, move_state):
        self._port = port
        self._move_state = move_state

        self._connections = []

    async def get_moves(self, websocket):
        while True:
            state_json = await websocket.recv()
            user_state = json.loads(state_json)

            print(user_state)

            self._move_state.update(user_state)


    async def handler(self, websocket):

        message = await websocket.recv()
        event = json.loads(message)

        assert event["type"] == "init"

        if len(self._connections) == 0:
            self._connections.append(websocket)

            try:
                print("Websockets client connected!")
                await websocket.send(json.dumps({"message": "connected"}))

                await self.get_moves(websocket)
            except websockets.exceptions.ConnectionClosedOK:
                print("Websockets client lost connection!")
            finally:
                self._connections.clear()
        else:
            await websocket.send(json.dumps({"message": "Vehicle already in control by someone else"}))

    async def start_server(self):
        print(f"Starting websockets server on 0.0.0.0:{self._port}...")
        async with websockets.serve(self.handler, "", self._port):
            await asyncio.Future()

    def start(self):
        asyncio.run(self.start_server())
