import random
import time

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TFONTF'  # Change this to a random secret key
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

players = []

@app.route('/')
def hello():
    return 'Hello, Farm Desktop App!'

@app.route('/players')
def get_players():
    return jsonify({'players': list(players)})

def notify_desktop_app(message):
    socketio.emit('message', {'message': message}, broadcast=True)

def generate_session_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))

@socketio.on('get_session_code')
def get_session_code():
    session_code = generate_session_code()
    emit('session_code', session_code)

@socketio.on('join_game')
def join_game(data):
    player_name = data.get('player_name')
    session_code = data.get('session_code')
    players.append(player_name)
    emit('player_joined' + session_code, player_name, broadcast=True)
    time.sleep(1)
    emit('update_lobby' + session_code, players, broadcast=True)

@socketio.on('leave_game')
def leave_game(data):
    player_name = data.get('player_name')
    session_code = data.get('session_code')
    players.remove(player_name)
    emit('player_left' + session_code, player_name, broadcast=True)
    time.sleep(1)
    emit('update_lobby' + session_code, players, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
