import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QListWidget
from socketio import Client


class FarmApp(QWidget):
    def __init__(self):
        super().__init__()
        self.players = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Farm Desktop App')
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Farm Desktop App', self)
        layout.addWidget(self.label)

        self.session_label = QLabel('Session Code: Fetching...', self)
        layout.addWidget(self.session_label)

        self.players_list = QListWidget(self)
        layout.addWidget(self.players_list)

        self.setLayout(layout)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    farm_app = FarmApp()

    # Connect to the SocketIO server
    socket = Client()

    # Listen for 'session_code' event
    @socket.event
    def connect():
        print('Connected to server')
        socket.emit('get_session_code')

    @socket.on('session_code')
    def on_session_code(session_code):
        print('Received session code:', session_code)
        farm_app.session_label.setText(f'Session Code: {session_code}')

    @socket.on('player_joined')
    def on_player_join(player_name):
        print(f'Player joined: {player_name}')
        farm_app.players.append(player_name)
        farm_app.players_list.clear()
        farm_app.players_list.addItems(farm_app.players)


    @socket.on('player_left')
    def on_player_leave(player_name):
        print(f'Player left: {player_name}')
        farm_app.players.remove(player_name)
        farm_app.players_list.clear()
        farm_app.players_list.addItems(farm_app.players)


    socket.connect('https://to-farm-or-not-tofarm.onrender.com')

    sys.exit(app.exec_())


