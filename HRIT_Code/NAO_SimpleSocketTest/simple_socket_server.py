#----------------------------------------------------------------------------------#
# By Emanuel Nunez and Edward White
# Version 1.1s
#----------------------------------------------------------------------------------#
# Notes
# No need to change the IP address or port number
# To run the server: 
"""
python3 simple_socket_server.py
"""
#----------------------------------------------------------------------------------#

# Import modules
import socket

# Define the server (computer) details
host = '0.0.0.0'    # Localhost
port = 8888         # Port number

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
            while True:
                #---SERVER STUFF: If a connection is made, accept it---#
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address} has been established.")

                #---SERVER STUFF: Handle client communication---#
                self.handle_client(client_socket)

        except KeyboardInterrupt:
            print("Server has been closed.")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        ### 3. Receive the data from the client
        important_message = client_socket.recv(1024).decode()
        print(f"Received the message: {important_message}")
        
        # If we get the right answer, do complex maths to answer the client's request
        if important_message == "1":
            print("Sending a 2 back to the client")
            important_answer = 2
        
            #---SERVER STUFF: Sends the output to the client---#
            client_socket.sendall(str(important_answer).encode())

        # If we get the wrong answer...
        else:
            important_answer = "Huh?"
            #---SERVER STUFF: Sends the output to the client---#
            client_socket.sendall(str(important_answer).encode())

        #---SERVER STUFF: Close the client socket---#
        client_socket.close()

if __name__ == "__main__":
    server = SimpleServer(host, port)
    server.start_server()
