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
        self.players = []
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
        self.retry_button.clicked.connect(self.connect_to_server)
        self.retry_button.setStyleSheet('background-color: lightblue')
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
        # self.layout.addWidget(self.start_game_button)
        self.start_game_button.setVisible(True)  # Initially hidden

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
            self.session_code_label.setText(f'Session Code: {session_code}')

        @self.socket.on('player_joined')
        def on_player_join(player):
            if player['code'] == self.session_code:
                print(f'Player joined: {player["name"]}')
                self.players.append(player['name'])
                self.update_player_list()

        @self.socket.on('player_left')
        def on_player_leave(player):
            print(f'Player left: {player["name"]}')
            self.players.remove(player['name'])
            self.update_player_list()

        try:
            #self.socket.connect('https://to-farm-or-not-tofarm.onrender.com')
            self.socket.connect('http://127.0.0.1:5000')
        except:
            print('Server is not running')
            self.label.setText('Server is not running')
            self.label.setStyleSheet('color: red')
            self.retry_button.setVisible(True)
            # QTimer.singleShot(self.retry_interval, self.connect_to_server)  # Retry after the interval

    def start_game(self):
        # Add your logic to start the game when enough players have connected
        print("start game was clicked")
        self.socket.emit('test_event' + self.session_code, data='test message')

    def update_player_list(self):
        self.players_list.setText("")
        strPlayers = ''
        for player in self.players:
            strPlayers += player + "\n"
        self.players_list.setText(strPlayers)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open('../assets/mainApp.css', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    farm_app = FarmApp()
    sys.exit(app.exec_())
