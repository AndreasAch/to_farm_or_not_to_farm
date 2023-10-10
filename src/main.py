import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget
from PyQt5.QtCore import QTimer

from flask import Flask

players = []  # Initialize an empty list to store player data

class FarmApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Farm Desktop App')
        self.setGeometry(300, 300, 400, 300)

        self.label = QLabel('Farm Desktop App', self)
        self.label.move(50, 50)

        self.session_label = QLabel('Session Code: ABCD', self)
        self.session_label.move(50, 100)

        self.players_label = QLabel('Players:', self)
        self.players_label.move(50, 150)

        self.shutdown_btn = QPushButton('Shutdown', self)
        self.shutdown_btn.move(250, 250)
        self.shutdown_btn.clicked.connect(self.shutdown)

        self.player_list_widget = QListWidget(self)
        self.player_list_widget.setGeometry(50, 180, 150, 100)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(1000)  # Update every 1 second

        self.show()

    def handle_new_player(self, player_name, session_code):
        # Update your GUI to display the new player
        self.player_list_widget.addItem(f'{player_name} ({session_code})')

    def start_notification_listener(self):
        app = Flask(__name__)

        @app.route('/player_joined', methods=['POST'])
        def player_joined():
            player_name = request.form['player_name']
            session_code = request.form['session_code']
            self.handle_new_player(player_name, session_code)
            return jsonify({'message': 'Notification received.'})

        app.run(host='0.0.0.0', port=12345)  # Use a port that your PyQt5 app will listen on

    def update_gui(self):
        # Fetch the updated player list
        player_list = self.fetch_player_list()
        self.update_players(player_list)

    def shutdown(self):
        # Add shutdown logic here
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    farm_app = FarmApp()
    sys.exit(app.exec_())
