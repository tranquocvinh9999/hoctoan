from flask_socketio import SocketIO, join_room, leave_room, emit
import random

question = [
    {"question": "1+1", "answer": "2"},
    {"question": "2+2", "answer": "4"},
    {"question": "3+5", "answer": "8"}
]
rooms = {}

