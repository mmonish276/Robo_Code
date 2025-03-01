class Command:
    def __init__(self):
        self.CMD_MOTOR = "CMD_MOTOR"
        self.CMD_LED = "CMD_LED"
        self.CMD_SERVO = "CMD_SERVO"
        self.CMD_ACTION = "CMD_ACTION"
        self.CMD_SONIC = "CMD_SONIC"
        self.CMD_MODE ="CMD_MODE"
    
    def testDrive():
        from motor import tankMotor              # Import the tankMotor class from the motor module
        import time                              # Import the time module for sleep functionality
        print("Running command")
        try: 
            drive = tankMotor()
            while True:
                    drive.setMotorModel(2000, 0) 
                    print("The car should be moving right")
                    time.sleep(2)
                    drive.setMotorMode1(0, 2000)
                    time.sleep(4)
                    print("The car should be moving left")
        except KeyboardInterrupt:
            drive.setMotorModel(0,0)
            print("End")


