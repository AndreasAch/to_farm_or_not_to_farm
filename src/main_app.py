import random
import sys

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton
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
            "round": 0,
            "events": []
        }
        self.session_code = ""
        # self.retry_interval = 3000  # 3 seconds
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
            self.socket.connect('https://to-farm-or-not-tofarm.onrender.com')
            # self.socket.connect('http://127.0.0.1:5000')
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
        ####
        self.socket.emit('session_start', data=self.session)
        ####
        self.load_ui_screen('./scenes/main_screen.ui')
        # print(self.session['players'])
        # self.socket.to(self.session_code).emit('test_event', data='test message')
        # self.socket.emit('test_event' + self.session_code, data='test message')

    def update_player_list(self):
        self.current_widget.players_list.setText("")
        str_players = ''
        for cls, player in self.session['players'].items():
            if player is not None:
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
        available_events = ['event1', 'event2', 'event3', 'event4']
        num_events = 18
        self.session['events'] = random.choices(available_events, k=num_events)

    def publish_forecasts(self):
        self.socket.emit('publish_forecasts', data=self.session_code)
        self.current_widget.reveal_weather_button.setEnabled(True)
        self.current_widget.instruction_label.setText(
            "DECISION TIME: " + "\n" + "Each player takes a turn to complete their actions")
        self.current_widget.forecast_button.setEnabled(False)

    def reveal_weather_event(self):
        self.current_widget.reveal_weather_button.setEnabled(False)
        self.current_widget.instruction_label.setText(
            "WEATHER EVENT: " + "\n" + self.session['events'][self.session['round']])
        self.current_widget.advance_round_button.setEnabled(True)

    def advance_round(self):
        self.current_widget.advance_round_button.setEnabled(False)
        self.current_widget.instruction_label.setText("")
        self.current_widget.forecast_button.setEnabled(True)
        self.session['round'] += 1
        self.current_widget.round_label.setText("ROUND: " + str(self.session['round']))
        self.socket.emit('advance_round', data=self.session)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    farm_app = FarmApp()
    sys.exit(app.exec_())
