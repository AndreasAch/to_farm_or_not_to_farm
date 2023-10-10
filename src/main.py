import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget
from PyQt5.QtCore import QTimer

class FarmApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Farm Desktop App')
        self.setGeometry(300, 300, 400, 400)

        self.label = QLabel('Farm Desktop App', self)
        self.label.move(50, 50)

        self.session_label = QLabel('Session Code: ABCD', self)
        self.session_label.move(50, 100)

        self.players_label = QLabel('Players:', self)
        self.players_label.move(50, 150)

        self.player_list_widget = QListWidget(self)
        self.player_list_widget.setGeometry(50, 200, 300, 150)

        self.refresh_button = QPushButton('Refresh Player List', self)
        self.refresh_button.move(50, 360)
        self.refresh_button.clicked.connect(self.update_gui)

        self.show()

    def fetch_player_list(self, session_code):
        url = f'http://localhost:5000/players/{session_code}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                players = response.json().get('players', [])
                return players
            else:
                print('Failed to fetch player list. Status code:', response.status_code)
        except requests.exceptions.RequestException as e:
            print('Error:', e)

    def update_gui(self):
        session_code = 'ABCD'  # Replace with the actual session code
        player_list = self.fetch_player_list(session_code)

        if player_list:
            self.player_list_widget.clear()
            for player in player_list:
                self.player_list_widget.addItem(player)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    farm_app = FarmApp()
    sys.exit(app.exec_())
