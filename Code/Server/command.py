class Command:
    def __init__(self):
        self.CMD_MOTOR = "CMD_MOTOR"
        self.CMD_LED = "CMD_LED"
        self.CMD_SERVO = "CMD_SERVO"
        self.CMD_ACTION = "CMD_ACTION"
        self.CMD_SONIC = "CMD_SONIC"
        self.CMD_MODE ="CMD_MODE"

    def test_Led():
        from led import Led                        # Import the Led class from the led module
        import time                                # Import the time module for sleep functionality
        print('Program is starting ... ')          # Print a start message
        led = Led()                                # Initialize the Led instance
        try:
            while True:
                print("ledIndex test")             # Print a test message
                led.ledIndex(0x01, 255, 0, 0)      # Set LED 1 to red
                led.ledIndex(0x02, 0, 255, 0)      # Set LED 2 to green
                led.ledIndex(0x04, 0, 0, 255)      # Set LED 3 to blue
                led.ledIndex(0x08, 255, 255, 255)  # Set LED 4 to white
                time.sleep(3)                      # Wait for 3 seconds

                print("colorWipe test")            # Print a test message
                led.colorWipe((255, 0, 0))         # Perform a red color wipe
                led.colorWipe((0, 255, 0))         # Perform a green color wipe
                led.colorWipe((0, 0, 255))         # Perform a blue color wipe
                time.sleep(1)                      # Wait for 1 second

                print("theaterChaseRainbow test")  # Print a test message
                led.theaterChaseRainbow()          # Perform a theater chase rainbow effect
                print("rainbow test")              # Print a test message
                led.rainbow()                      # Perform a rainbow effect
                print("rainbowCycle test")         # Print a test message
                led.rainbowCycle()                 # Perform a rainbow cycle effect

                led.colorWipe((0, 0, 0), 10)       # Turn off all LEDs
        except KeyboardInterrupt:                  # Handle keyboard interrupt (Ctrl+C)
            led.colorWipe((0, 0, 0), 10)           # Turn off all LEDs
            print("\nEnd of program")              # Print an end message
    
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


