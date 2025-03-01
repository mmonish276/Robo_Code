from motor import tankMotor              # Import the tankMotor class from the motor module
from servo import Servo            # Import the Servo class from the servo module
import time                              # Import the time module for sleep functionality


class Command:
    def __init__(self):
        self.CMD_MOTOR = "CMD_MOTOR"
        self.CMD_LED = "CMD_LED"
        self.CMD_SERVO = "CMD_SERVO"
        self.CMD_ACTION = "CMD_ACTION"
        self.CMD_SONIC = "CMD_SONIC"
        self.CMD_MODE ="CMD_MODE"
    
def Drive(leftSpeed, rightSpeed, time):
    drive = tankMotor()
    drive.setMotorModel(leftSpeed, rightSpeed) 
    print("Car should be moving")
    time.sleep(time)
    
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
   
def StopAll():
    servo = Servo()
    drive = tankMotor()
    drive.setMotorModel(0,0)
    servo.setServoAngle('0', 90)         # Set servo 0 to 90 degrees
    servo.setServoAngle('1', 140)        # Set servo 1 to 140 degrees
    print("\nEnd of program")          # Print an end message


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Parameter error: Please assign the device")       # Print an error message if no device is specified
        exit()                                                   # Exit the program
    if sys.argv[1] == 'Command' or sys.argv[1] == 'command':
        print("Running Command")
    try:
        while 1:
            DropArm()
            PinchIn()
            RaiseArm()
            Drive(-1000, -1000, 1)
            PinchOut()
            
    except KeyboardInterrupt:
        StopAll()
        
       

          



