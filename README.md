# UFMFUT-15-3-Human-Robot-Interaction-Technologies

Official repository for the human robot interaction technologies (BSc module) at University of the West of England (UFMFUT-15-3)

## Tutorial 2: Communication with the robot

You can find the files for this tutorial in the folder `tutorial2`. The tutorial is divided in two parts:

1. **Part 1: Basic communication with the robot**
2. **Part 2: Advanced communication with the robot**

### Part 1: Basic communication with the robot

You will learn how to send simple commands between the NAO and computer using sockets. The robot will send a message to the server, and the server will perform calculations and send back a response.

The robot code is in the file []() `ONROBOT_connect2server.py` (which you should put in a python box in Choreographe) and the server code is in the file `simple_socket_server.py`.

### Part 2: Advanced communication with the robot

You will learn how to send more complex commands. The server will now perform complicated calculations and send back a response to the robot.

The robot code is in the file `ONROBOT_connect2server.py` (which you should put in a python box in Choreographe) and the server code is in the file `mediapipe_socket_server.py`.

---

# Requirements

If you cannot use mediapipe on your preferred python environment, you can use the following to install it on your system:

1. Make sure you have a Python version between 3.8 and 3.10 (3.8 to 3.10 for Windows).

On Windows, Install Python 3.10

- Option 1: Open a terminal, type Python, go to Microsoft Store
- Option 2: Download from: https://www.python.org/downloads/windows/ , then right click, install as admin.
- Then Reboot

Linux supports up to 3.11, most distros will have it installed

2. Install OpenCV
   Type `pip install opencv-python` on terminal

3. Install Media Pipe
   Type `pip install mediapipe` on terminal
