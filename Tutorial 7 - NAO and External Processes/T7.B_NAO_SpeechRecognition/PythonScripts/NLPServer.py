#prereqs: PyAudio and SpeechRecognition libraries]
# Original from https://github.com/PaulBremner/Choregraphe/tree/master

# run GetDeviceIdx first to get the index for your microphone

import speech_recognition as sr

speech = sr.Microphone(device_index=1)  # set the correct device_index for the mircrophone you want to use
r = sr.Recognizer()

import socket

# Define the server (computer) details
host = '0.0.0.0'  # Localhost
port = 8888  # Port number


class SimpleServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

    def start_server(self):

        ### 1. Create a socket object
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the address and port
        self.server_socket.bind((self.host, self.port))
        # Listen for incoming connections
        self.server_socket.listen(1)

        ### 2. Wait for a connection (forever)
        print("Waiting for incoming connection...")
        try:
            # ---SERVER STUFF: If a connection is made, accept it---#
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address} has been established.")

            while True:

                if client_socket._closed is True:#if there is no open socket
                    print("socket accept")
                    client_socket, client_address = self.server_socket.accept()#wait for a new connection forever
                    print(f"Connection from {client_address} has been established.")
                else:#if a socket is open process incoming messages
                    # ---SERVER STUFF: Handle client communication---#
                    self.handle_client(client_socket)

        except KeyboardInterrupt:
            print("Server has been closed.")
        finally:
            self.server_socket.close()
            print("server socket closed")

    def handle_client(self, client_socket):
        ### 3. Receive the data from the client
        important_message = client_socket.recv(1024).decode()#this is a blocking call, so program flow waits here until a message is received
        print(f"Received the message: {important_message}")

        # If we get a 1 do speech processing. Replace these if else statements to get the desired fuctionality
        if important_message == "1":
            result = self.check_for_word("banana")#the method returns a 1 if the word is found and a 0 if not

            # ---SERVER STUFF: Sends the result to the client---#
            client_socket.sendall(str(result).encode())
        # If we get a 2 close the socket as the Choregraphe box has finished
        elif important_message == "2":
            # ---SERVER STUFF: Close the client socket---#
            client_socket.close()
        # If we get a message we don't recognise
        else:
            important_answer = "Huh?"
            # ---SERVER STUFF: Sends the output to the client---#
            client_socket.sendall(str(important_answer).encode())

    def check_for_word(self, word):#word should be the word we want to check for in the speech
        with speech as source:
            print("say something!…")
            audio = r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            recog = r.recognize_google(audio, language='en-US')
            print("You said: " + recog)
            if word.lower() in recog.lower():#set the word and the speech all to lower case to ensure there are no capitalisation issues
                print(word + " found!")
                return "1"
            else:
                return "0"
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


if __name__ == "__main__":
    server = SimpleServer(host, port)
    server.start_server()