# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QListWidget
# from socketio import Client
#
#
# class FarmApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.players = []
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Farm Desktop App')
#         self.setGeometry(300, 300, 400, 200)
#
#         layout = QVBoxLayout()
#
#         self.label = QLabel('Farm Desktop App', self)
#         layout.addWidget(self.label)
#
#         self.session_label = QLabel('Session Code: Fetching...', self)
#         layout.addWidget(self.session_label)
#
#         self.players_list = QListWidget(self)
#         layout.addWidget(self.players_list)
#
#         self.setLayout(layout)
#         self.show()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     farm_app = FarmApp()
#
#     # Connect to the SocketIO server
#     socket = Client()
#
#     # Listen for 'session_code' event
#     @socket.event
#     def connect():
#         print('Connected to server')
#         socket.emit('get_session_code')
#
#     @socket.on('session_code')
#     def on_session_code(session_code):
#         print('Received session code:', session_code)
#         farm_app.session_label.setText(f'Session Code: {session_code}')
#
#     @socket.on('player_joined')
#     def on_player_join(player_name):
#         print(f'Player joined: {player_name}')
#         farm_app.players.append(player_name)
#         farm_app.players_list.clear()
#         farm_app.players_list.addItems(farm_app.players)
#
#
#     @socket.on('player_left')
#     def on_player_leave(player_name):
#         print(f'Player left: {player_name}')
#         farm_app.players.remove(player_name)
#         farm_app.players_list.clear()
#         farm_app.players_list.addItems(farm_app.players)
#
#
#     socket.connect('https://to-farm-or-not-tofarm.onrender.com')
#
#     sys.exit(app.exec_())
#
#
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QListWidget, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QTimer
from socketio import Client

class FarmApp(QWidget):
    def __init__(self):
        super().__init__()
        self.socket = None
        self.players = []
        self.initUI()
        self.session_code = ""
        #self.retry_interval = 3000  # 3 seconds
        self.connect_to_server()

    def initUI(self):
        self.setWindowTitle('Farm Desktop App')
        self.setGeometry(300, 300, 400, 200)

        self.layout = QVBoxLayout()

        self.label = QLabel('Farm Desktop App', self)
        self.layout.addWidget(self.label)

        self.session_label = QLabel('Session Code: Fetching...', self)
        self.layout.addWidget(self.session_label)

        self.players_list = QListWidget(self)
        self.layout.addWidget(self.players_list)

        self.retry_button = QPushButton('Retry Connection', self)
        self.retry_button.clicked.connect(self.connect_to_server)
        self.retry_button.setStyleSheet('background-color: lightblue')
        self.retry_button.setVisible(False)
        self.layout.addWidget(self.retry_button)

        self.setLayout(self.layout)
        self.show()

    def connect_to_server(self):
        # Connect to the SocketIO server
        self.socket = Client()

        # Listen for 'session_code' event
        @self.socket.event
        def connect():
            print('Connected to server')
            self.socket.emit('get_session_code')
            self.label.setText('Connected to server')
            self.label.setStyleSheet('color: black')
            self.retry_button.setVisible(False)

        @self.socket.on('session_code')
        def on_session_code(session_code):
            print('Received session code:', session_code)
            self.session_code = session_code
            self.session_label.setText(f'Session Code: {session_code}')

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
            self.socket.connect('https://to-farm-or-not-tofarm.onrender.com')
            #self.socket.connect('http://127.0.0.1:5000')
        except:
            print('Server is not running')
            self.label.setText('Server is not running')
            self.label.setStyleSheet('color: red')
            self.retry_button.setVisible(True)
            #QTimer.singleShot(self.retry_interval, self.connect_to_server)  # Retry after the interval

    def update_player_list(self):
        self.players_list.clear()
        self.players_list.addItems(self.players)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    farm_app = FarmApp()
    sys.exit(app.exec_())
