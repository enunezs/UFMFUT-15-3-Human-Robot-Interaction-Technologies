#----------------------------------------------------------------------------------#
# By Emanuel Nunez and Edward White
# Version 1.2s
#----------------------------------------------------------------------------------#
# Notes
# - For the code to work, the connection to the NAO must be done via IP address! This can change everytime the connection is redone.
# - This address may change between sessions.
# - Use ipconfig (Windows) or ip addr / ifcondig (Linux) to find the IP address.
# - The robot must be able to reach the computer over the network.
# - The port number must match the server.
#----------------------------------------------------------------------------------#
# Usage
# 1. Paste this code into a Python box in Choregraphe.
# 2. Change the output type of onStopped to String.
# 3. Run the server code on the computer.
# 4. Run the behaviour in Choregraphe.
#----------------------------------------------------------------------------------#


# Import the necessary modules (yes, even inside of choregraphe)
import socket
import random
import time

# Parameters for the server
host = '164.11.73.0'     # Replace with your computer's IP address. 'FIND YOUR IP ADDRESS'. See above notes
# host = '127.0.0.1'     # Localhost, if the simulated robot and server share the same host. Uncomment if running in simulation

port = 8888 # No need to change

client_socket = None


class MyClass(GeneratedClass):

    def __init__(self):
        GeneratedClass.__init__(self)
        self.client_socket = None

    def onLoad(self):
        # Called when "play" is pressed
        pass

    def onInput_onStart(self):

        try:
            ### 1. Set up the client socket

            # Create a TCP/IP socket
            self.logger.info("Connecting to socket...")
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            ### 2. Connect to the server
            self.logger.info("Connecting to server...")
            self.client_socket.connect((host, port))
    
            ### 3. Send a message
            important_message = "1" # Try to change this!
            
            # This hard codes the output as this demo code sends,
            # and receives several messages that won't make sense as an output. 
            # When you replace the contents of this method with useful stuff,
            # make sure that "important_message" is set to the value you need the box to output when it has a result from the server
            self.logger.info("Sending: " + important_message)
            
            # Convert the message into bytes and send it
            self.client_socket.sendall(important_message.encode())
    
            # Small delay so the server can keep up
            time.sleep(0.001)
            
            ### 4. Receive the answer
    
            # Receive up to 1024 bytes and convert them into a string
            important_answer = self.client_socket.recv(1024).decode()
            self.logger.info("Received: " + str(important_answer))

            # Logging the answer:
            msgs_log = "" 
            # Note: To make debugging easier, 
            # append received messages to a string to be printed at the end, 
            # as the logger prints in a random order
            msgs_log += important_answer
    
            # Send a number to the output of the box
            self.onStopped(str(important_answer)) 
    
            # Show the logged information:
            self.logger.info("Complete message log: " + str(msgs_log))# Outputs the messages that the NAO just got from the server
             
        except socket.error as error:
            self.logger.error("Communication error: " + str(error))
            important_answer = "Error"

        finally:
            ### 6. Send a close socket message to close the connection and allow the server to listen for further connections
            self.onUnload()
            

        
    def onInput_onStop(self):
        self.onUnload()
        self.onStopped("Stopped") #activate the output of the box

    def onUnload(self):
        # Close the socket when stopped
        if self.client_socket is not None:
            self.client_socket.close()
            self.client_socket = None