import os
import random
import asyncio
import websockets
from flask import Flask, request, jsonify

app = Flask(__name__)
players = set()

@app.route('/')
def hello():
    return 'Hello, Farm Desktop App!'

@app.route('/players')
def get_players():
    return jsonify({'players': list(players)})

@app.route('/join', methods=['POST'])
def join_game():
    data = request.get_json()
    player_name = data.get('player_name')
    session_code = data.get('session_code')

    # Add player to the set
    players.add(player_name)

    # Notify the desktop app about the player joining
    notify_desktop_app(f'Player joined: {player_name}')

    return jsonify({'message': 'Join request received.'})

@app.route('/leave', methods=['POST'])
def leave_game():
    data = request.get_json()
    player_name = data.get('player_name')

    # Remove player from the set
    players.remove(player_name)

    # Notify the desktop app about the player leaving
    notify_desktop_app(f'Player left: {player_name}')

    return jsonify({'message': 'Leave request received.'})

def notify_desktop_app(message):
    asyncio.get_event_loop().run_until_complete(
        send_message_to_desktop_app(message)
    )

async def send_message_to_desktop_app(message):
    async with websockets.connect('ws://to-farm-or-not-tofarm.onrender.com/') as websocket:
        await websocket.send(message)

def generate_session_code():
    # Generate a random session code (e.g., 'ABCD123')
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))

@app.route('/session_code', methods=['GET'])
def get_session_code():
    session_code = generate_session_code()
    return jsonify({'session_code': session_code})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
