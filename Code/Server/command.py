from motor import tankMotor              # Import the tankMotor class from the motor module
from servo import Servo            # Import the Servo class from the servo module
from cent_dist import Dist
import time                              # Import the time module for sleep functionality
import cv2                    #openCV vision code

leftSpeeds = []
rightSpeeds = []
center_threshold = 50
center_distance = 100

class Command:
    def __init__(self):
        self.CMD_MOTOR = "CMD_MOTOR"
        self.CMD_LED = "CMD_LED"
        self.CMD_SERVO = "CMD_SERVO"
        self.CMD_ACTION = "CMD_ACTION"
        self.CMD_SONIC = "CMD_SONIC"
        self.CMD_MODE ="CMD_MODE"







def Drive(leftSpeed, rightSpeed):
    drive = tankMotor()
    drive.setMotorModel(leftSpeed, rightSpeed) 
    leftSpeeds.append(leftSpeed)
    rightSpeeds.append(rightSpeed)
    print("Car should be moving")
    time.sleep(2)
    
def PinchIn():
    print('Pinching Servo In')  # Print a start message
    servo = Servo()                    # Initialize the Servo instance
    servo.setServoAngle('0', 140)  # Set servo 0 to angle 140
    time.sleep(1)           # Wait for 0.01 seconds

def PinchOut():
    print('Pinching Servo Out')  # Print a start message
    servo = Servo()                    # Initialize the Servo instance
    servo.setServoAngle('0', 90)  # Set servo 0 to angle 90
    time.sleep(1)           # Wait for 0.01 seconds
    
def DropArm():
    print('Drop Arm')  # Print a start message
    servo = Servo()                    # Initialize the Servo instance
    servo.setServoAngle('1', 90)   # Set the angle for servo 1 to 90°
    time.sleep(1)           # Wait for 0.01 seconds

def RaiseArm():
    print('Raise Arm')  # Print a start message
    servo = Servo()                    # Initialize the Servo instance
    servo.setServoAngle('1', 140)   # Set the angle for servo 1 to 140°
    time.sleep(1)           # Wait for 0.01 seconds

def Start():
    servo = Servo()
    drive = tankMotor()
    drive.setMotorModel(0,0)
    servo.setServoAngle('0', 90)         # Set servo 0 to 90 degrees
    servo.setServoAngle('1', 140)        # Set servo 1 to 140 degrees

def StopAll():
    servo = Servo()
    drive = tankMotor()
    drive.setMotorModel(0,0)
    servo.setServoAngle('0', 90)         # Set servo 0 to 90 degrees
    servo.setServoAngle('1', 140)        # Set servo 1 to 140 degrees
    print("\nEnd of program")          # Print an end message

def check_error():
    #center_error = center_error - 1
    #dist_error = dist_error - 1
    x = 0

def pulse_turn(direction="right", duration=0.2, speed=2000):
    pwm_motor= tankMotor()
    """Send a short pulse to turn the car."""
    if direction == "right":
        pwm_motor.setMotorModel(speed, -speed)  # Left motor forward, right motor backward (turn right)
    else:
        pwm_motor.setMotorModel(-speed, speed)  # Left motor backward, right motor forward (turn left)
        
    time.sleep(duration)  # Run for the specified duration
    pwm_motor.setMotorModel(0, 0)  # Stop motors after pulse

def getCent():
    camera = Camera()
    center_distance = camera.getCent()



    
        
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Parameter error: Please assign the device")       # Print an error message if no device is specified
        exit()                                                   # Exit the program
    if sys.argv[1] == 'Command' or sys.argv[1] == 'command':
        print("Running Command")
        Start()
    try:
        while True:
            leftSpeeds = []
            rightSpeeds = []
            getCent()
            print(center_distance)

            while (abs(center_distance) > center_threshold):
                if center_distance > 0:
                    pulse_turn("left", 0.25, 2000)
                    getCent()
                    print(center_distance)
                    #check_error()
                elif center_distance:
                    pulse_turn("right", 0.25, 2000)
                    getCent()
                    print(center_distance)
                    #check_error()

            Drive(2000,2000)
            DropArm()
            PinchIn()
            RaiseArm()
            
            time.sleep(1)

            for i in range(len(leftSpeeds) - 1, -1, -1):
                Drive(-leftSpeeds[i], -rightSpeeds[i])
                time.sleep(1)
            
            Drive(2000,-2000)
            PinchOut()
            Drive(-2000,2000)


            
    except KeyboardInterrupt:
        StopAll()




