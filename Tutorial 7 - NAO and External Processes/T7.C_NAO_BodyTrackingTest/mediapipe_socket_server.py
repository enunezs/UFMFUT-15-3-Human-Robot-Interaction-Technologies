#----------------------------------------------------------------------------------#
# Simple Hand Raise Server
# By Emanuel Nunez and Edward White (Simplified + Corrected Version)
#----------------------------------------------------------------------------------#

import cv2
import mediapipe as mp
import socket
from threading import Thread, Lock
import time

host = '0.0.0.0'
port = 8888


class SimpleServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
        self.server_socket = None
        self.client_socket = None
        self.lock = Lock()

        self.start_server()

    def start_server(self):
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

        # Start a thread to accept connections
        thread = Thread(target=self.accept_connections, daemon=True)
        thread.start()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address} established.")

            # Replace existing client
            with self.lock:
                self.client_socket = client_socket

    def send_signal(self, message):
        with self.lock:
            if self.client_socket is None:
                print("No client connected.")
                return

            try:
                self.client_socket.sendall(message.encode())
            except Exception:
                print("Client disconnected.")
                self.client_socket = None


def image_processing(image):
    image = cv2.flip(image, 1)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def detect_hand_raise(server_host, server_port):

    print("Starting server...")
    server = SimpleServer(server_host, server_port)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera error")
        return

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    last_state = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        image = image_processing(frame)
        result = hands.process(image)

        state = "DOWN"

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                wrist = hand.landmark[mp_hands.HandLandmark.WRIST]
                index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                if index_tip.y < wrist.y:
                    state = "UP"

        # Only send signal when state changes (prevents flooding)
        if state != last_state:
            if state == "UP":
                server.send_signal("Hand Up")
                print("Hand Up")
            else:
                server.send_signal("Hand Down")
                print("Hand Down")
            last_state = state

        cv2.imshow("Hand Detection", frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_hand_raise(host, port)
