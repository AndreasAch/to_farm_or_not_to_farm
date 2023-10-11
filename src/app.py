import os
import random
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TFONTF'  # Change this to a random secret key
socketio = SocketIO(app)

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

    players.add(player_name)

    notify_desktop_app(f'Player joined: {player_name}')

    return jsonify({'message': 'Join request received.'})

@app.route('/leave', methods=['POST'])
def leave_game():
    data = request.get_json()
    player_name = data.get('player_name')

    players.remove(player_name)

    notify_desktop_app(f'Player left: {player_name}')

    return jsonify({'message': 'Leave request received.'})

def notify_desktop_app(message):
    socketio.emit('message', {'message': message}, broadcast=True)

def generate_session_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))

@socketio.on('get_session_code')
def get_session_code():
    session_code = generate_session_code()
    emit('session_code', session_code)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

