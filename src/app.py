import os
import random
import asyncio
import websockets
from flask import Flask, request, jsonify

app = Flask(__name__)
players = set()
desktop_app_websocket = "wss://to-farm-or-not-tofarm.onrender.com"

def generate_session_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))

@app.route('/session_code', methods=['GET'])
def get_session_code():
    session_code = generate_session_code()
    return jsonify({'session_code': session_code})

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
