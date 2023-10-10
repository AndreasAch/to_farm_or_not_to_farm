import requests

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Farm Desktop App!'

players = []  # List to store player information

@app.route('/join', methods=['POST'])
def join_game():
    player_name = request.form['player_name']
    session_code = request.form['session_code']

    # Add player to the list
    players.append({'player_name': player_name, 'session_code': session_code})

    # Notify the PyQt5 app of the new player
    send_player_info_to_pyqt(player_name, session_code)

    return jsonify({'message': 'Join request received.'})

def send_player_info_to_pyqt(player_name, session_code):
    # Replace with the appropriate URL for your PyQt5 app
    url = 'http://localhost:12345/player_joined'
    data = {'player_name': player_name, 'session_code': session_code}
    requests.post(url, data=data)
