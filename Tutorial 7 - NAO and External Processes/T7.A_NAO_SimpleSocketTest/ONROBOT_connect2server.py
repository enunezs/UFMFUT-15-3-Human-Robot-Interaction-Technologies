#----------------------------------------------------------------------------------#
# By Emanuel Nunez and Edward White
# Version 1.1s
#----------------------------------------------------------------------------------#
# Notes    
# For the code to work, the IP address must be set first. This can change everytime the computer is restarted.
# The IP address can be found by using the command `ipconfig` in the command prompt (Windows), or with `ifconfig` (Linux). 
# The port number is set to 8888 and is the same for the server and client.
# The private IP address for the computer is used and not the public one
#----------------------------------------------------------------------------------#
# Usage
# This code is used to connect to a server that is running on a computer. The server is listening for a connection from pc
# 1. Paste this code onto a Python box in Choregraphe
# 2. Change the output type of onStopped to string
# 3. Run the server code on the computer
# 4. Run the code on Choregraphe
#----------------------------------------------------------------------------------#


# Import the necessary modules (yes, even inside of choregraphe)
import socket
import random
import time

# Parameters for the server

host = '169.254.13.207'     # = 'FIND YOUR IP ADDRESS' # See above notes
# host = '127.0.0.1'          # Localhost, uncomment if running in simulation
port = 8888 # No need to change

client_socket = None


class MyClass(GeneratedClass):

    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        # Called when "play" is pressed
        pass

    def onInput_onStart(self):

        ### 1. Define the server        
        self.logger.info("Connecting to socket...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        self.logger.info("Connecting to server...")
        client_socket.connect((host, port))

        ### 2. Send a message
        important_message = random.randint(2,6)
        self.logger.info("Sending a random test value %s",str(important_message))
        client_socket.sendall(str(important_message).encode())
        
        # Small delay so the server can keep up
        time.sleep(0.001)
        # Sends a 1 to the server
        client_socket.sendall("1".encode())

        ### 3. Receive a message
        num = client_socket.recv(1024).decode()
        msgs = ""#append rec messages to a string to print at the end as if they are printed on receipt logger prints in a random order so makes debugging harder
        msgs += num

        ### 4. Send another message
        client_socket.sendall("3".encode())#it replies with Huh?
        num = client_socket.recv(1024).decode()
        msgs += num
        
        ### 5. Send a close socket message to close the connection and allow the server to listen for further connections
        client_socket.sendall("2".encode())#end of messages so send a close socket msg
        
        num = 1 #this hard codes the output as this demo code sends and receives several messages that won't make sense as an output. When you replace the contents of this method with useful stuff make sure that num is set to the value you need the box to output when it has a result from the server

        self.onStopped(str(num)) #send a number to the output of the box
        #self.logger.info(str(num))
        self.logger.info(str(msgs))# Outputs the messages that the NAO just got from the server

    def onInput_onStop(self):
        self.onUnload() 
        self.onStopped("Stopped") #activate the output of the box

    def onUnload(self): 
        # Close the socket when stopped   
        if client_socket is not None:          
            client_socket.close()   
        pass