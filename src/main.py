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
import requests
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
import websockets

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

        self.session_label = QLabel('Session Code: Loading...', self)
        layout.addWidget(self.session_label)

        self.setLayout(layout)
        self.show()

    async def connect_to_server_and_get_session_code(self):
        uri = "wss://to-farm-or-not-tofarm.onrender.com:8765"  # Replace with your WebSocket URL
        async with websockets.connect(uri) as websocket:
            await websocket.send('get_session_code')  # Request session code
            session_code = await websocket.recv()  # Receive session code
            self.session_label.setText(f'Session Code: {session_code}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    farm_app = FarmApp()
    loop = asyncio.get_event_loop()  # Get the event loop
    loop.create_task(farm_app.connect_to_server_and_get_session_code())  # Run the asynchronous task
    sys.exit(app.exec_())

