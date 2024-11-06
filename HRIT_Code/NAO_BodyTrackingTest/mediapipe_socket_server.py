import cv2
import mediapipe as mp
import socket

# NAO robot's IP address (or the server you are communicating with)
host = '0.0.0.0'  # Replace with your server's IP address
port = 8888      # Replace with your server's port

def DetectHandAndServer():
    # Initialize socket for communication
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)
    
    try:
        # Open webcam
        video_capture = cv2.VideoCapture(0)
        
        # Initialize MediaPipe Hands
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()
        mp_draw = mp.solutions.drawing_utils

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

            hand_raised = False
            if mediapipe_results.multi_hand_landmarks:
                for hand_landmarks in mediapipe_results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Detecting hand raise (basic example, you might need to fine-tune this)
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    if index_finger_tip.y < wrist.y:
                        hand_raised = True

            # Step 4: Send signal to server
            send_signal_to_server(sock, hand_raised)

            # Step 5: Display output
            cv2.imshow('Hand Detection', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(5) & 0xFF == 27:
                break

        # Close video capture
        video_capture.release()
    finally:
        sock.close()

def image_processing(image):
    # Convert the BGR image to RGB.
    return cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

def send_signal_to_server(sock, hand_raised):
    message = 'hand_raised' if hand_raised else 'hand_lowered'
    try:
        sock.sendall(message.encode())
    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == '__main__':
    DetectHandAndServer()
