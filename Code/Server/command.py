from motor import tankMotor              # Import the tankMotor class from the motor module
from servo import Servo            # Import the Servo class from the servo module
import time                              # Import the time module for sleep functionality
import cv2                    #openCV vision code

leftSpeeds = []
rightSpeeds = []
center_error = 100
dist_error = 0
center_threshold = 5
distance_threshold = 50

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
            if (abs(center_error) > center_threshold):
                if center_error > 0:
                    Drive(1000, -1000)
                    center_error = center_error - 1
                    print(center_error)
                    #check_error()
                else:
                    Drive(-1000, 1000)
                    #check_error()
            DropArm()
            PinchIn()
            RaiseArm()
            PinchOut()
            pulse_turn("right", 0.1, 2000)


            time.sleep(1)

            for i in range(len(leftSpeeds) - 1, -1, -1):
                Drive(-leftSpeeds[i], -rightSpeeds[i])
                time.sleep(1)


            
    except KeyboardInterrupt:
        StopAll()
        
       

          



