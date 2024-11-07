#----------------------------------------------------------------------------------#
# By Emanuel Nunez and Edward White
# Version 1.1s
#----------------------------------------------------------------------------------#
# Notes
# To run the server:
"""
python3 combined_server_camera.py
"""
#----------------------------------------------------------------------------------#

# Importing required libraries
import cv2
import mediapipe as mp
import socket
from threading import Thread, Lock

# Define the server (computer) details
host = '0.0.0.0'    # Localhost
port = 8888         # Port number


# Define the SimpleServer class
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
        # Bind the socket to the address and port
        self.server_socket.bind((self.host, self.port))
        # Listen for incoming connections
        self.server_socket.listen(1)

        # Start a thread to accept client connections
        accept_thread = Thread(target=self.accept_connections)
        accept_thread.start()

    def accept_connections(self):
        while True:
            self.client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address} has been established.")

    def send_signal(self, message):
        with self.lock:
            if self.client_socket:
                try:
                    self.client_socket.sendall(message.encode())
                    print(f"Sent message: {message}")
                except (BrokenPipeError, ConnectionResetError):
                    self.client_socket = None
                    print("Client disconnected.")
            else:
                print("No client connected.")

        # TODO: Add a try-except block to handle exceptions
        # TODO: Return a boolean value to indicate success or failure


# Main function
def detect_hand_raise(server_host, server_port):

    # First, create the server socket in a separate thread
    print("Creating server...")
    server = SimpleServer(server_host, server_port)
    print("Server created.")

    # At very start, open webcam
    video_capture = cv2.VideoCapture(0) # sometimes called "cap"

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    # Did we do it? Repeat until we get bored
    # One day change to thread
    while video_capture.isOpened():

        # Step 1: Read frame from camera
        success, image = video_capture.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Step 2: Image processing
        image = image_processing(image)

        # Step 3: Hand detection
        mediapipe_results = hands.process(image)

        if mediapipe_results.multi_hand_landmarks:
            for hand_landmarks in mediapipe_results.multi_hand_landmarks:
                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Detecting hand raise (basic example, you might need to fine-tune this)
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                if index_finger_tip.y < wrist.y: # If the index finger is above the wrist
                    print("Hand Raised")
                    signal_thread = Thread(target=server.send_signal, args=("Hand Up",))
                    signal_thread.start()
                else:
                    print("Hand Lowered")
                    signal_thread = Thread(target=server.send_signal, args=("Hand Down",))
                    signal_thread.start()

        # Step 4: Display output
        cv2.imshow('Hand Detection', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        if cv2.waitKey(5) & 0xFF == 27:
            break

    # At end, close it
    video_capture.release()

def image_processing(image):
    # Step 2.1: Convert the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    return image


if __name__ == "__main__":
    # Start detecting hand raises and send signals to the server
    detect_hand_raise(host, port)
