#----------------------------------------------------------------------------------#
# Movement detection for NAO robot red light green light game
# Version 1.0       Start writing the code get webcam working 08/11/2023
# Version 1.1        Get the position overlay working 09/11/2023
# Version 1.2       Fix all crashes with exeptions 11/11/2023
# Version 1.3       Get the file sending and reading to work 15/11/2023
# Version 1.4       Current

# Edward White
#----------------------------------------------------------------------------------#

# Import all the required add-ons
import cv2
import mediapipe as mp

# Count is for a counter to ignore first frames (set later on)
count = 0
# The amount of movement allowed before getting caught out
error = 0.01
# error_check is used to make sure that the part of the body is on frame or not
error_check = 0.5

# Draws the pose estimation
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence= 0.5, min_tracking_confidence= 0.5)
# Starts video capture
cap = cv2.VideoCapture(0)
# Sets the webcam to the resolution of the monitor
cap.set(3, 1920 )
cap.set(4, 1080)

# Both classes are used to both make typing out the code easier and to make the code easier to follow
# Used to get the x,y coords of each joint and to get how visible to the camera it is
class move:
    def __init__(self, x, y,vis):
        self.x = x
        self.y = y
        self.vis = vis
# Used to get the previous x, y coords of each joint to later compare
class prev:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Sets the code to go forever
while True:
    # Opens the text file that tells the script when to fully run
    # It does not close the webcam only pauses the live feed this is due to hardware limitations
    with open("red.txt", "r") as read:
        content = read.read()
    # Checks if the file contains the number 1 if so it carries on the loop
    if content == "1":
        # Capture the webcam live feed
        ret, img = cap.read()
        # Turns the image to RGB so the colours are not inverted at the output
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Checks if the webcam is on or plugged in
        if not ret:
            print("Error, cannot connect to webcam")
            break
        # Overlays the pose drawing on to the live feed from the webcam
        pose_results = pose.process(img_rgb)
        mp_drawing.draw_landmarks(img, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        move_flag = 0
        # Uses the move class to define each part of body that we are watching
        try:
            Nose = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].visibility)
            LeftShoulder = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].visibility)
            RightShoulder = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].visibility)
            LeftElbow = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].visibility)
            RightElbow = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].visibility)
            LeftWrist = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].visibility)
            RightWrist = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].visibility)
            LeftHand = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].visibility)
            RightHand = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].visibility)
            LeftHip = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].visibility)
            RightHip = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].visibility)
            LeftKnee = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].visibility)
            RightKnee = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].visibility)
            LeftAnkle = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].visibility)
            RightAnkle = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].visibility)
            LeftFoot = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].visibility)
            RightFoot = move(pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y, pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].visibility)
        # If it fails due to the person no longer being detected
        except:
            print("Please put your face back in frame")

        # Creates a buffer to allow the first prev to work and so the movement detection doesn't falsely flag after being re-opened
        if count > 5:
            # Checks if that part of the body is visible
            if Nose.vis > error_check:
                # Checks for movement in both the x and y-axis with the error for micro stutters
                if Nose.x < NosePrev.x - error or Nose.x > NosePrev.x + error or Nose.y < NosePrev.y - error or Nose.y > NosePrev.y + error:
                    print("Nose Moved")
                    move_flag = 1

            if LeftShoulder.vis > error_check:
                if LeftShoulder.x < LeftShoulderPrev.x - error or LeftShoulder.x > LeftShoulderPrev.x + error or LeftShoulder.y < LeftShoulderPrev.y - error or LeftShoulder.y > LeftShoulderPrev.y + error:
                    print("Left Shoulder Moved")
                    move_flag = 1

            if RightShoulder.vis > error_check:
                if RightShoulder.x < RightShoulderPrev.x - error or RightShoulder.x > RightShoulderPrev.x + error or RightShoulder.y < RightShoulderPrev.y - error or RightShoulder.y > RightShoulderPrev.y + error:
                    print("Right Shoulder Moved")
                    move_flag = 1

            if LeftElbow.vis > error_check:
                if LeftElbow.x < LeftElbowPrev.x - error or LeftElbow.x > LeftElbowPrev.x + error or LeftElbow.y < LeftElbowPrev.y - error or LeftElbow.y > LeftElbowPrev.y + error:
                    print("Left Elbow Moved")
                    move_flag = 1

            if RightElbow.vis > error_check:
                if RightElbow.x < RightElbowPrev.x - error or RightElbow.x > RightElbowPrev.x + error or RightElbow.y < RightElbowPrev.y - error or RightElbow.y > RightElbowPrev.y + error:
                    print("Right Elbow Moved")
                    move_flag = 1

            if LeftWrist.vis > error_check:
                if LeftWrist.x < LeftWristPrev.x - error or LeftWrist.x > LeftWristPrev.x + error or LeftWrist.y < LeftWristPrev.y - error or LeftWrist.y > LeftWristPrev.y + error:
                    print("Left Wrist Moved")
                    move_flag = 1

            if RightWrist.vis > error_check:
                if RightWrist.x < RightWristPrev.x - error or RightWrist.x > RightWristPrev.x + error or RightWrist.y < RightWristPrev.y - error or RightWrist.y > RightWristPrev.y + error:
                    print("Right Wrist Moved")
                    move_flag = 1

            if LeftHand.vis > error_check:
                if LeftHand.x < LeftHand.x - error or LeftHand.x > LeftHandPrev.x + error or LeftHand.y < LeftHandPrev.y - error or LeftHand.y > LeftHandPrev.y + error:
                    print("Left Hand Moved")
                    move_flag = 1

            if RightHand.vis > error_check:
                if RightHand.x < RightHandPrev.x - error or RightHand.x > RightHandPrev.x + error or RightHand.y < RightHandPrev.y - error or RightHand.y > RightHandPrev.y + error:
                    print("Right Hand Moved")
                    move_flag = 1

            if LeftHip.vis > error_check:
                if LeftHip.x < LeftHipPrev.x - error or LeftHip.x > LeftHipPrev.x + error or LeftHip.y < LeftHipPrev.y - error or LeftHip.y > LeftHipPrev.y + error:
                    print("Left Hip Moved")
                    move_flag = 1

            if RightHip.vis > error_check:
                if RightHip.x < RightHipPrev.x - error or RightHip.x > RightHipPrev.x + error or RightHip.y < RightHipPrev.y - error or RightHip.y > RightHipPrev.y + error:
                    print("Right Hip Moved")
                    move_flag = 1

            if LeftKnee.vis > error_check:
                if LeftKnee.x < LeftKneePrev.x - error or LeftKnee.x > LeftKneePrev.x + error or LeftKnee.y < LeftKneePrev.y - error or LeftKnee.y > LeftKneePrev.y + error:
                    print("Left Knee Moved")
                    move_flag = 1

            if RightKnee.vis > error_check:
                if RightKnee.x < RightKneePrev.x - error or RightKnee.x > RightKneePrev.x + error or RightKnee.y < RightKneePrev.y - error or RightKnee.y > RightKneePrev.y + error:
                    print("Right Knee Moved")
                    move_flag = 1

            if LeftAnkle.vis > error_check:
                if LeftAnkle.x < LeftAnklePrev.x - error or LeftAnkle.x > LeftAnklePrev.x + error or LeftAnkle.y < LeftAnklePrev.y - error or LeftAnkle.y > LeftAnklePrev.y + error:
                    print("Left Ankle Moved")
                    move_flag = 1

            if RightAnkle.vis > error_check:
                if RightAnkle.x < RightAnklePrev.x - error or RightAnkle.x > RightAnklePrev.x + error or RightAnkle.y < RightAnklePrev.y - error or RightAnkle.y > RightAnklePrev.y + error:
                    print("Right Ankle Moved")
                    move_flag = 1

            if LeftFoot.vis > error_check:
                if LeftFoot.x < LeftFootPrev.x - error or LeftFoot.x > LeftFootPrev.x + error or LeftFoot.y < LeftFootPrev.y - error or LeftFoot.y > LeftFootPrev.y + error:
                    print("Left Foot Moved")
                    move_flag = 1

            if RightFoot.vis > error_check:
                if RightFoot.x < RightFootPrev.x - error or RightFoot.x > RightFootPrev.x + error or RightFoot.y < RightFootPrev.y - error or RightFoot.y > RightFootPrev.y + error:
                    print("Right Foot Moved")
                    move_flag = 1
        # Gets the values from the current frame and stores it to compare to the next frame
        try:
            NosePrev = prev(Nose.x, Nose.y)
            LeftShoulderPrev = prev(LeftShoulder.x, LeftShoulder.y)
            RightShoulderPrev = prev(RightShoulder.x, RightShoulder.y)
            LeftElbowPrev = prev(LeftElbow.x, LeftElbow.y)
            RightElbowPrev = prev(RightElbow.x, RightElbow.y)
            LeftWristPrev = prev(LeftWrist.x, LeftWrist.y)
            RightWristPrev = prev(RightWrist.x, RightWrist.y)
            LeftHandPrev = prev(LeftHand.x, LeftHand.y)
            RightHandPrev = prev(RightHand.x, RightHand.y)
            LeftHipPrev = prev(LeftHip.x, LeftHip.y)
            RightHipPrev = prev(RightHip.x, RightHip.y)
            LeftKneePrev = prev(LeftKnee.x, LeftKnee.y)
            RightKneePrev = prev(RightKnee.x, RightKnee.y)
            LeftAnklePrev = prev(LeftAnkle.x, LeftAnkle.y)
            RightAnklePrev = prev(RightAnkle.x, RightAnkle.y)
            LeftFootPrev = prev(LeftFoot.x, LeftFoot.y)
            RightFootPrev = prev(RightFoot.x, RightFoot.y)
        # If it fails
        except:
            print("Please Allow webcam to see you")
        # Increases the counter for the frame skip
        count = count + 1
        # Debugging
        #print(move_flag)
        # Constantly writes the output of the movement script
        with open("move.txt", "w") as file:
            file.write(str(move_flag))
        # Outputs the live feed mostly for debugging as it is not needed
        cv2.imshow('test', img)
        # Checks if the 'q' key has been pressed then ends the loop
        if cv2.waitKey(1) == ord('q'):
            break
    # This is what prints when the red.txt file is set to 0
    else:
        print("waiting")
        count = 0
# Turns off the webcam and ends the script
cv2.destroyAllWindows()
cap.release()