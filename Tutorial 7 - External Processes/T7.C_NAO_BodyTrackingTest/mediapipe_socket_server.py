#----------------------------------------------------------------------------------#
# By Emanuel Nunez and Edward White
# Version 1.2s
#----------------------------------------------------------------------------------#
# Notes
# - No need to change the IP address or port number.
# - The server handles one request per connection.
# - A message is sent when the detected hand state changes or a client connects.
# - Requires the OpenCV and MediaPipe libraries.
# - To stop the server, press ESC in the camera window or Ctrl+C.
#
# To run the server:
#
# python3 mediapipe_socket_server.py
#----------------------------------------------------------------------------------#

# Import modules
import socket
import cv2
import mediapipe as mp
from threading import Thread, Lock

# Define the server (computer) details
host = '0.0.0.0'    # Listen on all available IPv4 network interfaces
port = 8889         # Port number


class SimpleServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

        self.client_socket = None
        # Store the latest result from MediaPipe
        self.last_state = None
        # NEW: Synchronise access between the two threads
        self.lock = Lock()

    def start_server(self):

        ### 1. Create a socket object

        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Allow the server to reuse the same address after restarting
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the address and port
        self.server_socket.bind((self.host, self.port))

        # Listen for incoming connections
        self.server_socket.listen(1)

        ### 2. Wait for a connection in a separate thread
        # Start a thread to accept connections
        thread = Thread(target=self.accept_connections, daemon=True)
        thread.start()

    def accept_connections(self):

        ### 2. Wait for a connection

        print("Waiting for incoming connection...")

        while True: # (forever)

            # A. Wait until a client connects
            try:
                client_socket, client_address = self.server_socket.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            print(f"Connection from {client_address} has been established.")

            # B. Replace the previous client, if one exists
            with self.lock:
                if self.client_socket is not None:
                    self.client_socket.close()

                self.client_socket = client_socket

                # Send the latest hand state to the new client
                if self.last_state is not None:
                    self.send_signal(self.last_state)

            # Then go back to A to wait for another connection


    def send_signal(self, message):

        ### Send the message to the connected client

        if self.client_socket is None:
            return

        try:
            self.client_socket.sendall(message.encode())

        except OSError:
            print("Client disconnected.")
            self.client_socket.close()
            self.client_socket = None


    def update_state(self, state):

        # Only send a message when the hand state changes
        with self.lock:
            if state != self.last_state:
                self.last_state = state

                print(state)
                self.send_signal(state)


    def close_server(self):

        # Close the server and client sockets
        with self.lock:
            self.server_socket.close()

            if self.client_socket is not None:
                self.client_socket.close()
                self.client_socket = None

        print("Server socket closed.")



def detect_hand_raise(server):

    ### 3. Initialise the camera and MediaPipe

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera error.")
        cap.release()
        return

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    try:
        while cap.isOpened():

            ### 4. Capture and process the image

            # Read a frame from the camera
            ret, frame = cap.read()

            if not ret:
                continue

            # Flip the image horizontally and convert it to RGB
            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect the hands in the image
            result = hands.process(image)

            ### 5. Determine the hand state

            # Assume the hand is down by default
            state = "Hand Down"

            if result.multi_hand_landmarks:
                for hand in result.multi_hand_landmarks:

                    # Draw the detected hand landmarks
                    mp_draw.draw_landmarks(
                        frame, hand, mp_hands.HAND_CONNECTIONS
                    )

                    # Get the positions of the wrist and index fingertip
                    wrist = hand.landmark[mp_hands.HandLandmark.WRIST]
                    index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    # Check if the index fingertip is above the wrist
                    if index_tip.y < wrist.y:
                        state = "Hand Up"

            ### 6. Update the server with the detected hand state

            server.update_state(state)

            ### 7. Display the image

            cv2.imshow("Hand Detection", frame)

            # Press ESC to stop
            if cv2.waitKey(5) & 0xFF == 27:
                break

    finally:
        hands.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    server = SimpleServer(host, port)
    server.start_server()

    try:
        detect_hand_raise(server)

    except KeyboardInterrupt:
        print("Server has been closed.")

    finally:
        server.close_server()
