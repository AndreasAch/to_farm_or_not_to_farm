import random
import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton
from socketio import Client


class FarmApp(QWidget):
    def __init__(self):
        super().__init__()
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
        self.initUI()
        self.session_code = ""
        # self.retry_interval = 3000  # 3 seconds
        self.connect_to_server()

    def initUI(self):

        self.setWindowTitle('Farm Desktop App')
        # Load the custom font
        font_id = QFontDatabase.addApplicationFont("../assets/fonts/Righteous.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        self.retry_button = QPushButton('Retry Connection', self)
        self.retry_button.setObjectName("retry_button")
        self.retry_button.setGeometry(942, 313, 269, 51)
        font = QFont(font_family, 18)
        self.retry_button.setFont(font)
        self.retry_button.clicked.connect(self.connect_to_server)
        self.retry_button.setVisible(False)
        # self.layout.addWidget(self.retry_button)

        self.setWindowTitle('To Farm Or Not to Farm')
        self.setWindowIcon(QtGui.QIcon('../assets/leaf.ico'))
        self.setFixedSize(1280, 720)

        # Display session code with custom font
        self.session_code_label = QLabel('Session Code: Fetching...', self)
        font = QFont(font_family, 30)
        self.session_code_label.setFont(font)
        self.session_code_label.setGeometry(0, 0, 1280, 80)
        self.session_code_label.setAlignment(Qt.AlignCenter)
        # self.layout.addWidget(self.session_code_label)

        # Create the QLabel and add it to the parent QWidget
        self.players_list = QLabel('', self)
        self.players_list.setAlignment(Qt.AlignCenter)
        self.players_list.setObjectName("players_list")
        self.players_list.setGeometry(436, 89, 407, 542)

        font = QFont(font_family, 24)
        self.players_list.setFont(font)
        # Add a border to see the bounds of the QLabel
        self.players_list.setStyleSheet("border: 1px solid red;")

        # Start game button
        self.start_game_button = QPushButton('Start Game', self)
        self.start_game_button.setObjectName("start_button")
        self.start_game_button.setGeometry(507, 662, 269, 51)
        font = QFont(font_family, 18)
        self.start_game_button.setFont(font)
        self.start_game_button.clicked.connect(self.start_game)
        self.start_game_button.setVisible(True)

        # self.setLayout(self.layout)
        self.show()

    def connect_to_server(self):
        # Connect to the SocketIO server
        self.socket = Client()

        # Listen for 'session_code' event
        @self.socket.event
        def connect():
            print('Connected to server')
            self.socket.emit('get_session_code')
            self.retry_button.setVisible(False)

        @self.socket.on('session_code')
        def on_session_code(session_code):
            print('Received session code:', session_code)
            self.session_code = session_code
            self.session['session_code'] = session_code
            self.session_code_label.setText(f'Session Code: {session_code}')

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
            # self.socket.connect('https://to-farm-or-not-tofarm.onrender.com')
            self.socket.connect('http://127.0.0.1:5000')
        except:
            print('Server is not running')
            self.session_code_label.setText('Server is not running')
            self.retry_button.setVisible(True)
            # QTimer.singleShot(self.retry_interval, self.connect_to_server)  # Retry after the interval

    def start_game(self):
        # Add logic to start the game when enough players have connected
        print("start game was clicked")
        self.generate_weather_events()
        print(self.session)
        self.socket.emit('session_start', data=self.session)
        # print(self.session['players'])
        # self.socket.to(self.session_code).emit('test_event', data='test message')
        # self.socket.emit('test_event' + self.session_code, data='test message')

    def update_player_list(self):
        self.players_list.setText("")
        strPlayers = ''
        for cls, player in self.session['players'].items():
            if player is not None:
                strPlayers += player + " (" + cls + ")" + "\n"
            else:
                continue
        self.players_list.setText(strPlayers)

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
        #print(self.session['players'])

    def generate_weather_events(self):
        available_events = ['event1', 'event2', 'event3', 'event4']
        num_events = 18
        self.session['events'] = random.choices(available_events, k=num_events)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open('../assets/mainApp.css', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    farm_app = FarmApp()
    sys.exit(app.exec_())
