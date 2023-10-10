from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary to store player information by session code
player_data = {}

@app.route('/')
def hello():
    return 'Hello, Farm Desktop App!'

@app.route('/players/<session_code>', methods=['GET'])
def get_players(session_code):
    players = player_data.get(session_code, [])
    return jsonify({'players': players})

@app.route('/join', methods=['POST'])
def join_game():
    player_name = request.form.get('player_name')
    session_code = request.form.get('session_code')

    if player_name and session_code:
        # Create a new list for the session code if it doesn't exist
        if session_code not in player_data:
            player_data[session_code] = []

        # Add player to the list for the session code
        player_data[session_code].append(player_name)

        return jsonify({'message': 'Join request received.'})
    else:
        return jsonify({'error': 'Invalid player_name or session_code.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
