import random
import time

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TFONTF'  # Change this to a random secret key
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

sessions = {}


@app.route('/')
def hello():
    return 'Hello, Farm Desktop App!'


def generate_session_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))


@socketio.on('get_session_code')
def get_session_code():
    session_code = generate_session_code()
    join_room(session_code)
    emit('session_code', session_code, room=session_code)


@socketio.on('join_game')
def join_game(data):
    player = {
        'code': data.get('session_code'),
        'name': data.get('player_name')
    }
    if player['code'] not in sessions:
        sessions[player['code']] = []
    sessions[player['code']].append(player['name'])
    join_room(player['code'])
    emit('player_joined', player, room=player['code'])
    time.sleep(1)
    emit('update_lobby', player, room=player['code'])


@socketio.on('leave_game')
def leave_game(data):
    player = {
        'code': data.get('session_code'),
        'name': data.get('player_name')
    }
    sessions[player['code']].remove(player['name'])
    emit('player_left', player, room=player['code'])
    time.sleep(1)
    emit('update_lobby', player, room=player['code'])


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
