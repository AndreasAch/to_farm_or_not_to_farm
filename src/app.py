import os
import random

from flask import Flask, request, jsonify

app = Flask(__name__)

players = []

@app.route('/')
def hello():
    return 'Hello, Farm Desktop App!'

@app.route('/players')
def get_players():
    return jsonify({'players': [player['name'] for player in players]})

@app.route('/join', methods=['POST'])
def join_game():
    data = request.get_json()
    player_name = data.get('player_name')
    session_code = data.get('session_code')

    # Add player to the list
    players.append({'name': player_name, 'session_code': session_code})

    return jsonify({'message': 'Join request received.'})

def send_player_info_to_pyqt(player_name, session_code):
    # Implement this to notify the PyQt5 app
    pass

@app.route('/session_code', methods=['GET'])
def get_session_code():
    session_code = generate_session_code()
    return jsonify({'session_code': session_code})

def generate_session_code():
    # Generate a random session code (e.g., 'ABCD123')
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
