import json
import os
import random
import asyncio
import websockets
from flask import Flask, request, jsonify

app = Flask(__name__)
players = set()
desktop_app_websocket = None

def generate_session_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))

@app.websocket("/ws")
async def websocket_handler(websocket):
    try:
        while True:
            message = await websocket.receive_text()
            message_data = json.loads(message)

            if message_data["type"] == "getSessionCode":
                session_code = generate_session_code()
                response_message = {
                    "type": "sessionCode",
                    "sessionCode": session_code
                }
                await websocket.send_text(json.dumps(response_message))

    except websockets.exceptions.ConnectionClosed:
        # Handle the connection closed event
        pass

if __name__ == '__main__':
    # ... existing code ...

    async def websocket_handler(websocket, path):
        global desktop_app_websocket
        desktop_app_websocket = websocket
        try:
            while True:
                await asyncio.sleep(10)  # Keep the WebSocket connection alive
        except websockets.exceptions.ConnectionClosed:
            pass

    start_server = websockets.serve(websocket_handler, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
