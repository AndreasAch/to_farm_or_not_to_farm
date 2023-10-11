import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class FarmApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Farm Desktop App')
        self.setGeometry(300, 300, 400, 200)  # Adjust dimensions as needed

        layout = QVBoxLayout()

        self.label = QLabel('Farm Desktop App', self)
        layout.addWidget(self.label)

        # Display the session code obtained from the server
        session_code = self.fetch_session_code()
        self.session_label = QLabel(f'Session Code: {session_code}', self)
        layout.addWidget(self.session_label)

        self.setLayout(layout)
        self.show()

    def fetch_session_code(self):
        # Replace with your server endpoint to fetch the session code
        endpoint = 'https://to-farm-or-not-to-farm-0cabd20d5aac.herokuapp.com/session_code'
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                return response.json().get('session_code', 'Unknown')
            else:
                print('Failed to fetch session code. Status code:', response.status_code)
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return 'Unknown'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    farm_app = FarmApp()
    sys.exit(app.exec_())
