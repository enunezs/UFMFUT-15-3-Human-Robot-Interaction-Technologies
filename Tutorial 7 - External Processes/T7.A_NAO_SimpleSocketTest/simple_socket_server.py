#----------------------------------------------------------------------------------#
# By Emanuel Nunez and Edward White
# Version 1.1s
#----------------------------------------------------------------------------------#
# Notes
# - No need to change the IP address or port number.
# - The server handles one request per connection.
# - To stop the server, press Ctrl+C.
#
# To run the server: 
#
# python3 simple_socket_server.py
#----------------------------------------------------------------------------------#

# Import modules
import socket

# Define the server (computer) details
host = '0.0.0.0'    # Listen on all available IPv4 network interfaces
port = 8888         # Port number

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
        important_message = client_socket.recv(1024).decode()

        # An empty message indicates that the client has disconnected
        if not important_message:
            return
        
        print(f"Received the message: {important_message}")

        ### 4. Process the message

        # If we get the right answer, do complex maths to answer the client's request!
        if important_message == "1":
            print("Sending a 2 back to the client")
            important_answer = 2

        # If we get the wrong answer...
        else:
            important_answer = "Server: Huh? I don't understand the client message..."

        ### 5. Send the answer back to the client
        print(f"Sending {important_answer} back to the client")

        #---SERVER STUFF: Sends the output to the client---#
        client_socket.sendall(str(important_answer).encode())


if __name__ == "__main__":
    server = SimpleServer(host, port)
    server.start_server()
