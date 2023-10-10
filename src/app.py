import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

lobby_players = []  # List to store player information

@app.route('/')
def hello():
    return 'Hello, Farm Desktop App!'

@app.route('/lobby_players', methods=['GET'])
def get_lobby_players():
    return jsonify({'lobby_players': lobby_players})

@app.route('/join', methods=['POST'])
def join_game():
    player_name = request.form['player_name']
    session_code = request.form['session_code']

    # Add player to the list
    lobby_players.append(player_name)

    return jsonify({'message': 'Join request received.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
