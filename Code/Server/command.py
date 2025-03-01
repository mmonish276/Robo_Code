class Command:
    def __init__(self):
        self.CMD_MOTOR = "CMD_MOTOR"
        self.CMD_LED = "CMD_LED"
        self.CMD_SERVO = "CMD_SERVO"
        self.CMD_ACTION = "CMD_ACTION"
        self.CMD_SONIC = "CMD_SONIC"
        self.CMD_MODE ="CMD_MODE"
    
def test_Drive():
    from motor import tankMotor              # Import the tankMotor class from the motor module
    import time                              # Import the time module for sleep functionality
    print("Running command")
    try: 
        drive = tankMotor()
        drive.setMotorModel(2000, 0) 
        print("The car should be moving right")
        time.sleep(2)
        drive.setMotorModel(0, 2000)
        time.sleep(2)
        print("The car should be moving left")
    except KeyboardInterrupt:
        drive.setMotorModel(0,0)
        print("End")

def Pinch():
    from servo import Servo            # Import the Servo class from the servo module
    import time                        # Import the time module for sleep functionality
    print('Pinching Servo')  # Print a start message
    servo = Servo()                    # Initialize the Servo instance
    try:
        for i in range(90, 150, 1):
            servo.setServoAngle('0', i)  # Set servo 0 to angle i
            time.sleep(0.01)           # Wait for 0.01 seconds
    except KeyboardInterrupt:              # Handle keyboard interrupt (Ctrl+C)
        servo.setServoAngle('0', 90)         # Set servo 0 to 90 degrees
        servo.setServoAngle('1', 140)        # Set servo 1 to 140 degrees
        print("\nEnd of program")          # Print an end message
    
def DropArm():
    from servo import Servo            # Import the Servo class from the servo module
    import time                        # Import the time module for sleep functionality
    print('Pinching Servo')  # Print a start message
    servo = Servo()                    # Initialize the Servo instance
    try:
        for i in range(140, 90, -1):
            servo.setServoAngle('1', i)  # Set servo 1 to angle i
            time.sleep(0.01)           # Wait for 0.01 seconds
    except KeyboardInterrupt:              # Handle keyboard interrupt (Ctrl+C)
        servo.setServoAngle('0', 90)         # Set servo 0 to 90 degrees
        servo.setServoAngle('1', 140)        # Set servo 1 to 140 degrees
        print("\nEnd of program")          # Print an end message

def StopAll():
    from servo import Servo            # Import the Servo class from the servo module
    from motor import tankMotor              # Import the tankMotor class from the motor module
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
        End = 0
        while End != 0:
            test_Drive()                                         # Drive
            DropArm()
            Pinch()
            if (KeyboardInterrupt):
                End = 1
        # Ending Code
        StopAll()
       

          



