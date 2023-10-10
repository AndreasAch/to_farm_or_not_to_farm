import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget
from PyQt5.QtCore import QTimer

class FarmApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_lobby_players)
        self.timer.start(5000)  # Update player list every 5 seconds

    def initUI(self):
        self.setWindowTitle('Farm Desktop App')
        self.setGeometry(300, 300, 400, 400)  # Increased height for the lobby

        self.label = QLabel('Farm Desktop App', self)
        self.label.move(50, 50)

        self.session_label = QLabel('Session Code: ABCD', self)
        self.session_label.move(50, 100)

        self.players_label = QLabel('Players:', self)
        self.players_label.move(50, 150)

        self.player_list_widget = QListWidget(self)
        self.player_list_widget.setGeometry(20, 250, 200, 100)

        self.lobby_message = QLabel('Waiting for the game to start...', self)
        self.lobby_message.move(50, 380)  # Position the lobby message

        self.refresh_button = QPushButton('Refresh', self)
        self.refresh_button.move(250, 300)  # Adjust position for the refresh button
        self.refresh_button.clicked.connect(self.update_lobby_players)

        self.show()

    def enter_lobby(self):
        self.refresh_button.setVisible(True)  # Show the refresh button

    def fetch_lobby_players(self):
        url = 'http://localhost:5000/lobby_players'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                lobby_players = response.json().get('lobby_players', [])
                return lobby_players
            else:
                print('Failed to fetch lobby players. Status code:', response.status_code)
        except requests.exceptions.RequestException as e:
            print('Error:', e)

    def update_lobby_players(self):
        lobby_players = self.fetch_lobby_players()
        if lobby_players:
            self.player_list_widget.clear()
            self.player_list_widget.addItems(lobby_players)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    farm_app = FarmApp()
    sys.exit(app.exec_())
