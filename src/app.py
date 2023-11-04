import random
import time

from flask import Flask
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TFONTF'  # Change this to a random secret key
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

players_per_session = {}
session_data = {}


@app.route('/')
def hello():
    return 'Hello, Farm Desktop App!'


def generate_session_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))


@socketio.on('get_session_code')
def get_session_code():
    session_code = generate_session_code()
    join_room(session_code)
    players_per_session[session_code] = []
    session_data[session_code] = {}
    emit('session_code', session_code, room=session_code)


@socketio.on('request_join')
def join_game(data):
    player = {
        'code': data.get('session_code'),
        'name': data.get('player_name')
    }
    if player['code'] not in players_per_session.keys():
        # Add emit here to communicate error to client
        # sessions[player['code']] = []
        return

    players_per_session[player['code']].append(player['name'])
    print(players_per_session)
    join_room(player['code'])
    emit('player_joined', player, room=player['code'])
    emit('join_approve' + player['name'], player, room=player['code'])
    time.sleep(2)
    emit('update_lobby', players_per_session[player['code']], room=player['code'])


@socketio.on('leave_game')
def leave_game(data):
    player = {
        'code': data.get('session_code'),
        'name': data.get('player_name')
    }
    players_per_session[player['code']].remove(player['name'])
    emit('player_left', player, room=player['code'])
    time.sleep(2)
    emit('update_lobby', players_per_session[player['code']], room=player['code'])


@socketio.on('join')
def join(data):
    code = data.get('session_code')
    name = data.get('player_name')
    join_room(code)
    emit('update_lobby', players_per_session[code], room=code)


@socketio.on('session_start')
def session_start(session):
    session_data[session['session_code']] = session
    #print(session_data)
    data_to_send = {
        "players": list(session['players'].items())
    }
    print(data_to_send)
    emit('move_to_forecast', data_to_send, room=session['session_code'])
    # probably move these from here
    # time.sleep(2)
    # emit('test_event', 'test_data', room=session['session_code'])


@socketio.on('publish_forecasts')
def publish_forecasts(data):
    # 65% 55% 35%
    code = data['code']
    print(session_data[code])
    players_in_session = data['player_names']
    curr_round = session_data[code]['round']
    events = session_data[code]['events'][curr_round:curr_round + 3]
    event_pool = ['Normal', 'Drought', 'Rain', 'Hail']
    print("Actual: " + str(events))
    print("===========")
    forecast = [None] * 3
    for i, chance in enumerate([0.85, 0.70, 0.55]):
        rem = (1 - chance) / 3
        weights = [rem, rem, rem, rem]
        weights[event_pool.index(events[i])] = chance
        print(weights)
        forecast[i] = random.choices(event_pool, weights=weights, k=1)[0]
    print(forecast)
    emit('clear_forecast', room=code)
    for player in players_in_session:
        emit('distribute_forecast' + player, forecast, room=code)


@socketio.on('advance_round')
def advance_round(session):
    session_data[session['session_code']] = session
    emit('advance_client_round', session['round'], room=session['session_code'])



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
