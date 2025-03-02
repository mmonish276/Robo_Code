from motor import tankMotor              # Import the tankMotor class from the motor module
from servo import Servo                  # Import the Servo class from the servo module
import time                               # Import the time module for sleep functionality
import cv2                                # OpenCV for vision processing
from ultrasonic import Ultrasonic         # Ultrasonic sensor module

leftSpeeds = []
rightSpeeds = []
center_error = 100  # Initial error in alignment
center_threshold = 5  # Acceptable alignment threshold
distance_threshold = 50  # Distance at which to stop moving forward
ultrasonic = Ultrasonic()  # Initialize ultrasonic sensor
sensor_distance = ultrasonic.get_distance()  # Get initial distance

class Command:
    def __init__(self):
        self.CMD_MOTOR = "CMD_MOTOR"
        self.CMD_LED = "CMD_LED"
        self.CMD_SERVO = "CMD_SERVO"
        self.CMD_ACTION = "CMD_ACTION"
        self.CMD_SONIC = "CMD_SONIC"
        self.CMD_MODE = "CMD_MODE"

def Drive(leftSpeed, rightSpeed):
    drive = tankMotor()
    drive.setMotorModel(leftSpeed, rightSpeed)
    leftSpeeds.append(leftSpeed)
    rightSpeeds.append(rightSpeed)
    print("Car should be moving")
    time.sleep(0.1)

def PinchIn():
    print('Pinching Servo In')
    servo = Servo()
    servo.setServoAngle('0', 140)
    time.sleep(1)

def PinchOut():
    print('Pinching Servo Out')
    servo = Servo()
    servo.setServoAngle('0', 90)
    time.sleep(1)

def DropArm():
    print('Drop Arm')
    servo = Servo()
    servo.setServoAngle('1', 90)
    time.sleep(1)

def RaiseArm():
    print('Raise Arm')
    servo = Servo()
    servo.setServoAngle('1', 140)
    time.sleep(1)

def Start():
    servo = Servo()
    drive = tankMotor()
    drive.setMotorModel(0,0)
    servo.setServoAngle('0', 90) 
    servo.setServoAngle('1', 140)

def StopAll():
    servo = Servo()
    drive = tankMotor()
    drive.setMotorModel(0,0)
    servo.setServoAngle('0', 90)
    servo.setServoAngle('1', 140)
    print("\nEnd of program")

def check_error():
    global center_error
    center_error -= 10  # Simulate error reduction (should be updated based on camera processing)

def pulse_turn(direction="right", duration=0.2, speed=2000):
    pwm_motor = tankMotor()
    """Send a short pulse to turn the car."""
    if direction == "right":
        pwm_motor.setMotorModel(speed, -speed)  
    else:
        pwm_motor.setMotorModel(-speed, speed)  
        
    time.sleep(duration)
    pwm_motor.setMotorModel(0, 0)  

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Parameter error: Please assign the device")
        exit()
    if sys.argv[1] == 'Command' or sys.argv[1] == 'command':
        print("Running Command")
        Start()
    try:
        # Step 1: Align the robot with the object
        while abs(center_error) > center_threshold:
            if center_error > 0:
                pulse_turn("left", 0.1, 2000)
            else:
                pulse_turn("right", 0.1, 2000)

            time.sleep(1)
            check_error()

        # Step 2: Move toward the object
        sensor_distance = ultrasonic.get_distance()  
        while sensor_distance > distance_threshold:
            Drive(500, 500)
            time.sleep(0.1)
            sensor_distance = ultrasonic.get_distance()  

        # Step 3: Pick up the object
        DropArm()
        PinchIn()
        RaiseArm()

        # Step 4: Move backward and place the object down
        Drive(-500, -500)
        time.sleep(2)  
        Drive(-500,300)
        time.sleep(1)
        PinchOut()

    except KeyboardInterrupt:
        StopAll()


import cv2

from ultralytics import solutions

cap = cv2.VideoCapture("Path/to/video/file.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Video writer
video_writer = cv2.VideoWriter("distance_calculation.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Init distance-calculation obj
distance = solutions.DistanceCalculation(model="yolo11n.pt", show=True)

# Process video
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    im0 = distance.calculate(im0)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()