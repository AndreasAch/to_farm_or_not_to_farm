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
    player_name = request.form['player_name']
    session_code = request.form['session_code']

    players.append({'name': player_name, 'session_code': session_code})

    # Notify the PyQt5 app of the new player
    send_player_info_to_pyqt(player_name, session_code)

    return jsonify({'message': 'Join request received.'})

def send_player_info_to_pyqt(player_name, session_code):
    # Implement this to notify the PyQt5 app
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
