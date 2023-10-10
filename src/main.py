import sys
import requests

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from threading import Thread

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

        self.refresh_button = QPushButton('Refresh Player List', self)
        self.refresh_button.move(20, 200)
        self.refresh_button.clicked.connect(self.update_gui)

        self.show()

    def join_game(self, player_name, session_code):
        url = 'http://localhost:5000/join'  # Replace with the appropriate URL
        data = {'player_name': player_name, 'session_code': session_code}
        response = requests.post(url, data=data)

        if response.status_code == 200:
            print('Successfully joined the game!')
        else:
            print('Failed to join the game. Please check the session code and try again.')

    def handle_new_player(self, player_name, session_code):
        # Update your GUI to display the new player
        # For now, let's just print the player information
        print(f'New player joined: {player_name} ({session_code})')

    def start_notification_listener(self):
        app = Flask(__name__)

        @app.route('/player_joined', methods=['POST'])
        def player_joined():
            player_name = request.form['player_name']
            session_code = request.form['session_code']
            self.handle_new_player(player_name, session_code)
            return jsonify({'message': 'Notification received.'})

        app.run(host='0.0.0.0', port=12345)  # Use a port that your PyQt5 app will listen on


    def fetch_player_list(self):
        # Replace 'http://localhost:5000' with the appropriate URL of your Flask server
        url = 'http://localhost:5000/players'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                player_list = response.json()['players']
                return player_list
            else:
                print('Failed to fetch player list. Status code:', response.status_code)
        except requests.exceptions.RequestException as e:
            print('Error:', e)

    def update_players(self, player_list):
        players_text = '\n'.join(player_list)
        self.players_label.setText('Players:\n' + players_text)

    def update_gui(self):
        # Clear the current list
        self.player_list_widget.clear()

        # Fetch the updated player list
        player_list = self.fetch_player_list()

        if player_list:
            # Update the list widget with player names
            for player in player_list:
                self.player_list_widget.addItem(player)

    def shutdown(self):
        # Create a QTimer
        self.timer = QTimer(self)
        # Connect the timeout signal to quit the application
        self.timer.timeout.connect(self.quit_application)
        # Start the timer with a 1ms delay
        self.timer.start(1)

def start_flask_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "Hello, Flask is running!"

    @app.route('/add_player/<player_name>')
    def add_player(player_name):
        players.append(player_name)
        # Update the PyQt5 GUI with the latest player list
        farm_app.update_players(players)
        return "Player added successfully!"

    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = Thread(target=start_flask_app)
    flask_thread.start()

    # Start PyQt5 app
    app = QApplication(sys.argv)
    farm_app = FarmApp()
    sys.exit(app.exec_())
