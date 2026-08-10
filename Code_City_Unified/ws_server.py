import asyncio
import websockets
import json
from boardroom_orchestrator import BoardroomOrchestrator

# Initialize Boardroom
boardroom = BoardroomOrchestrator()

async def ws_handler(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            response = boardroom.process(message)
            await websocket.send(json.dumps(response))
    except Exception as e:
        print(f"Error: {e}")

start_server = websockets.serve(ws_handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
