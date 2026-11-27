#----------------------------------------------------------------------------------#
# By Emanuel Nunez and Edward White, updated by Paul Bremner
# Version 1.2s
#----------------------------------------------------------------------------------#
# Original from https://github.com/PaulBremner/Choregraphe/tree/master
#----------------------------------------------------------------------------------#
# Notes
# - No need to change the IP address or port number.
# - The server handles one request per connection.
# - Requires the PyAudio and SpeechRecognition libraries.
# - Run GetDeviceIdx first to find the index of your microphone.
# - Google Speech Recognition requires an internet connection.
# - To stop the server, press Ctrl+C.
#
# To run the server:
#
# python3 NLPServer.py
#----------------------------------------------------------------------------------#

# Import modules
import socket
import speech_recognition as sr

# Set up the speech recognizer and microphone
speech = sr.Microphone(device_index=1) # run GetDeviceIdx first to get the index for your microphone
r = sr.Recognizer()

import socket

# Define the server (computer) details
host = '0.0.0.0'    # Listen on all available IPv4 network interfaces
port = 8889         # Port number


class SimpleServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

    def start_server(self):

        ### 1. Create a socket object

        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address and port
        self.server_socket.bind((self.host, self.port))

        # Listen for incoming connections
        self.server_socket.listen(1)

        ### 2. Wait for a connection
        print("Waiting for incoming connection...")

        try:
            while True: # (forever)

                # A. Wait until a client connects. If a connection is made, accept it
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address} has been established.")

                # B. Process the client's request
                try:
                    self.handle_client(client_socket) # see the handle_client method below

                # C. Close the client socket after processing the request
                finally:
                    client_socket.close()

                # Then go back to A to wait for another connection

        except KeyboardInterrupt:
            print("Server has been closed.")

        finally:
            self.server_socket.close()
            print("Server socket closed.")


    def handle_client(self, client_socket):

        ### 3. Receive the data from the client

        # Receive up to 1024 bytes and convert them into a string
        important_message = client_socket.recv(1024).decode() #this is a blocking call, so program flow waits here until a message is received
        
        # An empty message indicates that the client has disconnected
        if not important_message:
            return
        
        print(f"Received the message: {important_message}")

        ### 4. Process the message
        # If we receive a "1", perform speech recognition
        # Replace these if else statements to get the desired fuctionality

        if important_message == "1": # Check whether the user said the target word
            # Returns "1" if the word is found, or "0" otherwise
            important_answer = self.check_for_word("Shark") # Try to change this!

        # If we get a 2 close the socket as the Choregraphe box has finished
        elif important_message == "2":
            # ---SERVER STUFF: Close the client socket---#
            client_socket.close()

        # If we receive a message we don't recognise...
        else:
            important_answer = "Huh?"
            # ---SERVER STUFF: Sends the output to the client---#
            client_socket.sendall(str(important_answer).encode())

        ### 5. Send the answer back to the client
        print(f"Sending {important_answer} back to the client")

        #---SERVER STUFF: Sends the output to the client---#
        client_socket.sendall(str(important_answer).encode())


    def check_for_word(self, word): 
        # word should be the word we want to check for in the speech

        ### SPEECH RECOGNITION
        try: 
            # A. Record audio using the computer's microphone
            with speech as source:
                 # Calibrate the recognizer to the background noise
                print("Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source)

                # Wait for the user to speak and record their speech
                print("say something!…")
                audio = r.listen(source, timeout=5, phrase_time_limit=10)

                # B. Convert the recorded speech into text
                recog = r.recognize_google(audio, language='en-GB') # Change the language if you want to use a different one
                print("You said: " + recog)

                # C. Check whether the target word appears in the recognised text
                # Convert both strings to lowercase to ignore capitalisation
                if word.lower() in recog.lower():#set the word and the speech all to lower case to ensure there are no capitalisation issues
                    print(word + " found!")
                    return "1"
                else:
                    print(word + " not found!")
                    return "0"
                

        except sr.WaitTimeoutError:
            print("No speech was detected.")
            return "0"

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
            return "0"

        except sr.RequestError as error:
            print("Could not request results from Google Speech Recognition: " + str(error))
            return "Error"


if __name__ == "__main__":
    server = SimpleServer(host, port)
    server.start_server()