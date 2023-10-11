# import sys
# import asyncio
# import requests
# import websockets
# from websockets import connect
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
#
# class FarmApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Farm Desktop App')
#         self.setGeometry(300, 300, 400, 200)  # Adjust dimensions as needed
#
#         layout = QVBoxLayout()
#
#         self.label = QLabel('Farm Desktop App', self)
#         layout.addWidget(self.label)
#
#         # Display the session code obtained from the server
#         session_code = self.fetch_session_code()
#         self.session_label = QLabel(f'Session Code: {session_code}', self)
#         layout.addWidget(self.session_label)
#
#         self.setLayout(layout)
#         self.show()
#
#         asyncio.get_event_loop().run_until_complete(self.websocket_handler())
#
#     def fetch_session_code(self):
#         # Replace with your server endpoint to fetch the session code
#         endpoint = 'https://to-farm-or-not-tofarm.onrender.com/session_code'
#         try:
#             response = requests.get(endpoint)
#             response.raise_for_status()  # Raise an exception for bad status codes (4xx, 5xx)
#             return response.json().get('session_code', 'Unknown')
#         except requests.exceptions.RequestException as e:
#             print('Error:', e)
#             return 'Error fetching session code'
#
#     async def websocket_handler(self):
#         uri = "wss://to-farm-or-not-tofarm.onrender.com/"  # Replace with your WebSocket URL
#         async with websockets.connect(uri) as websocket:
#             while True:
#                 message = await websocket.recv()
#                 self.session_label.setText(f"Session Code: {message}")
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     farm_app = FarmApp()
#     sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from socketio import Client

class FarmApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Farm Desktop App')
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Farm Desktop App', self)
        layout.addWidget(self.label)

        self.session_label = QLabel('Session Code: Fetching...', self)
        layout.addWidget(self.session_label)

        self.setLayout(layout)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    farm_app = FarmApp()

    # Connect to the SocketIO server
    socket = Client()
    socket.connect('https://to-farm-or-not-tofarm.onrender.com:5000')

    # Listen for 'session_code' event
    @socket.on('session_code')
    def on_session_code(session_code):
        farm_app.session_label.setText(f'Session Code: {session_code}')

    sys.exit(app.exec_())


