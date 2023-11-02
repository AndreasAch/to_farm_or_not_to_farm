import random
import sys

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton, QListWidgetItem
from socketio import Client


class FarmApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_widget = None
        self.socket = None
        self.session = {
            "session_code": "",
            "players": {
                'class1': None,
                'class2': None,
                'class3': None,
                'class4': None,
                'class5': None,
                'class6': None,
            },
            "player_names": [],
            "round": 0,
            "events": []
        }
        self.session_code = ""
        # Rules for weather generation
        self.rules = {
            'Normal1': {'trigger': ['Normal', 'Normal'], 'outcome': 'Normal'},
            'Normal2': {'trigger': ['Normal', 'Hail'], 'outcome': 'Normal'},
            'Drought1': {'trigger': ['Drought', 'Drought'], 'outcome': 'Drought'},
            'Drought2': {'trigger': ['Drought', 'Rain'], 'outcome': 'Drought'},
            'Hail': {'trigger': ['Normal', 'Rain'], 'outcome': 'Hail'},
            'Rain': {'trigger': ['Normal', 'Drought'], 'outcome': 'Rain'}
        }

        font_id = QFontDatabase.addApplicationFont("../assets/fonts/Righteous.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        self.initUI()
        self.connect_to_server()

    def initUI(self):
        self.setWindowTitle('To Farm Or Not To Farm')
        self.setWindowIcon(QIcon('../assets/leaf.ico'))
        self.setFixedSize(1280, 720)

        self.layout = QVBoxLayout()

        # Load the initial UI screen
        self.load_ui_screen("./scenes/start_screen.ui")

        self.setLayout(self.layout)
        self.show()

    def load_ui_screen(self, ui_file):
        if self.current_widget:
            self.layout.removeWidget(self.current_widget)
            self.current_widget.deleteLater()

        self.current_widget = uic.loadUi(ui_file)
        self.layout.addWidget(self.current_widget)

        ### START SCREEN ###
        if hasattr(self.current_widget, "start_game_button"):
            self.current_widget.start_game_button.clicked.connect(self.start_game)
        if hasattr(self.current_widget, "retry_button"):
            self.current_widget.retry_button.clicked.connect(self.connect_to_server)

        ### MAIN SCREEN ###
        if hasattr(self.current_widget, "round_label"):
            self.current_widget.round_label.setText("ROUND: " + str(self.session['round']))
        if hasattr(self.current_widget, "forecast_button"):
            self.current_widget.forecast_button.clicked.connect(self.publish_forecasts)
        if hasattr(self.current_widget, "reveal_weather_button"):
            self.current_widget.reveal_weather_button.clicked.connect(self.reveal_weather_event)
        if hasattr(self.current_widget, "advance_round_button"):
            self.current_widget.advance_round_button.clicked.connect(self.advance_round)
        if hasattr(self.current_widget, "forecast_list"):
            self.forecast_list = self.current_widget.forecast_list
            for player_name in self.session['player_names']:
                item = QListWidgetItem(player_name)
                item.setCheckState(Qt.Unchecked)  # Add checkbox flag
                self.forecast_list.addItem(item)

    def connect_to_server(self):
        # Connect to the SocketIO server
        self.socket = Client()

        # Listen for 'session_code' event
        @self.socket.event
        def connect():
            print('Connected to server')
            self.socket.emit('get_session_code')
            self.current_widget.retry_button.setVisible(False)

        @self.socket.on('session_code')
        def on_session_code(session_code):
            print('Received session code:', session_code)
            self.session_code = session_code
            self.session['session_code'] = session_code
            self.current_widget.session_code_label.setText(f'Session Code: {session_code}')

        @self.socket.on('player_joined')
        def on_player_join(player):
            if player['code'] == self.session_code:
                print(f'Player joined: {player["name"]}')
                # Previous method
                # self.players.append(player['name'])
                self.assign_class(player['name'])
                self.update_player_list()

        @self.socket.on('player_left')
        def on_player_leave(player):
            print(f'Player left: {player["name"]}')
            # Find player that left and make their class available
            for cls, name in self.session['players'].items():
                if name == player['name']:
                    self.session['players'][cls] = None
            # self.players.remove(player['name'])
            self.update_player_list()

        try:
            #self.socket.connect('https://to-farm-or-not-tofarm.onrender.com')
            self.socket.connect('http://127.0.0.1:5000')
        except:
            print('Server is not running')
            self.current_widget.session_code_label.setText('Server is not running')
            self.current_widget.retry_button.setVisible(True)
            # QTimer.singleShot(self.retry_interval, self.connect_to_server)  # Retry after the interval

    def start_game(self):
        # Add logic to start the game when enough players have connected
        print("start game was clicked")
        self.generate_weather_events()
        print(self.session)
        self.socket.emit('session_start', data=self.session)
        self.load_ui_screen('./scenes/main_screen.ui')

        self.calculate_single_forecast()

        # print(self.session['players'])
        # self.socket.to(self.session_code).emit('test_event', data='test message')
        # self.socket.emit('test_event' + self.session_code, data='test message')

    def update_player_list(self):
        self.current_widget.players_list.setText("")
        str_players = ''
        self.session['player_names'] = []
        for cls, player in self.session['players'].items():
            if player is not None:
                self.session['player_names'].append(player)
                str_players += player + " (" + cls + ")" + "\n"
            else:
                continue
        self.current_widget.players_list.setText(str_players)

    def assign_class(self, player_name):
        # Store the available classes
        available_classes = []
        for c in self.session['players']:
            if self.session['players'][c] is None:
                available_classes.append(c)
        # Check that there are actually available classes
        if len(available_classes) != 0:
            # Assign player_name to a random available class
            cls = random.choice(available_classes)
            self.session['players'][cls] = player_name
        # print(self.session['players'])

    def generate_weather_events(self):
        # available_events = ['event1', 'event2', 'event3', 'event4']
        # num_events = 18
        # self.session['events'] = random.choices(available_events, k=num_events)
        generated_events = self.generate_weather_sequence()

        print(generated_events)
        self.session['events'] = generated_events

    def generate_weather_sequence(self):
        rules = {
            ('Normal', 'Normal'): 'Drought',
            ('Drought', 'Drought'): 'Rain',
            ('Normal', 'Rain'): 'Drought',
            ('Drought', 'Hail'): 'Normal',
            ('Rain', 'Rain'): 'Hail',
            ('Hail', 'Hail'): 'Normal'
        }

        available_events = ['Normal', 'Rain', 'Drought', 'Hail']

        while True:
            sequence = [random.choice(['Normal', 'Drought']), random.choice(available_events)]

            while len(sequence) < 12:
                if tuple(sequence[-2:]) in rules:
                    next_event = rules[tuple(sequence[-2:])]
                    sequence.append(next_event)
                else:
                    sequence.append(random.choice(available_events))

            unique_events = set(sequence)
            distinct_rules = set(rules.get((sequence[i], sequence[i + 1]), None) for i in range(len(sequence) - 1))

            # Check for distinct rules until the end of the sequence - 1
            if len(unique_events) == 4 and len([rule for i, rule in enumerate(distinct_rules) if i < len(sequence) - 2 and rule is not None]) >= 3:
                return sequence

    # NEEDS TO CHANGE TO SEND FORECAST ONLY TO THE PLAYERS THAT OPT-IN
    def publish_forecasts(self):
        self.current_widget.reveal_weather_button.setEnabled(True)
        self.current_widget.instruction_label.setText(
            "DECISION TIME: " + "\n" + "Each player takes a turn to complete their actions")
        self.current_widget.forecast_button.setEnabled(False)
        checked_items = []
        for i in range(self.forecast_list.count()):
            item = self.forecast_list.item(i)
            if item.checkState() == 2:  # 2 represents Checked, 0 represents Unchecked
                checked_items.append(item.text())
            item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)
        self.socket.emit('publish_forecasts', data={
            'code': self.session_code,
            'player_names': checked_items
        })

    def reveal_weather_event(self):
        self.current_widget.reveal_weather_button.setEnabled(False)
        self.current_widget.instruction_label.setText(
            "WEATHER EVENT: " + "\n" + self.session['events'][self.session['round']])
        self.current_widget.advance_round_button.setEnabled(True)

    def advance_round(self):
        self.current_widget.advance_round_button.setEnabled(False)
        self.current_widget.instruction_label.setText("")
        self.current_widget.forecast_button.setEnabled(True)
        for i in range(self.forecast_list.count()):
            item = self.forecast_list.item(i)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

        self.session['round'] += 1
        self.current_widget.round_label.setText("ROUND: " + str(self.session['round']))
        self.calculate_single_forecast()
        self.socket.emit('advance_round', data=self.session)

    def calculate_single_forecast(self):
        event_pool = ['Normal', 'Drought', 'Rain', 'Hail']
        weights = [0.15, 0.15, 0.15, 0.15]
        weights[event_pool.index(self.session['events'][self.session['round']])] = 0.55
        first_round_forecast = random.choices(event_pool, weights=weights, k=1)
        self.current_widget.instruction_label.setText("FORECASTED EVENT FOR THE ROUND:" + "\n" + first_round_forecast[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    farm_app = FarmApp()
    sys.exit(app.exec_())
