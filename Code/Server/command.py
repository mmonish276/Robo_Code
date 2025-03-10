from motor import tankMotor              # Import the tankMotor class from the motor module
from servo import Servo, HardwareServo, HardwarePWM            # Import the Servo class from the servo module
from camera import Camera
import time                              # Import the time module for sleep functionality
import cv2
import numpy as np
from ultralytics import YOLO
import RPi.GPIO as GPIO

from rpi_hardware_pwm import HardwarePWM

leftSpeeds = []
rightSpeeds = []
center_threshold = 50

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
  
    elif direction == "left":
        pwm_motor.setMotorModel(-speed, speed)  # Left motor backward, right motor forward (turn left)

    elif direction == "forward":
        pwm_motor.setMotorModel(-speed, -speed)
        time.sleep(0.75)
    elif direction == "backward":
        pwm_motor.setMotorModel(speed, speed)
        time.sleep(0.75)
    
        
    time.sleep(duration)  # Run for the specified duration
    pwm_motor.setMotorModel(0, 0)  # Stop motors after pulse

def set_gpio_high(pin=18):
    GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
    GPIO.setup(pin, GPIO.OUT)  # Set pin as output
    GPIO.output(pin, GPIO.HIGH)  # Set pin HIG

MAGNET_OFF_DUTY = 0.0
MAGNET_ON_DUTY = 8.0 

class Electromagnet:
    def __init__(self):
        self.magnet = HardwareServo(1)

        # self.magnet.setServoFrequency("2", 2000)
        self.magnet.setServoDuty('1', 0)
        # self.magnet = HardwarePWM(pwm_channel=0, hz=50, chip=2)

    def enable(self):
        self.magnet.setServoDuty('1', MAGNET_ON_DUTY)

    def disable(self):
        self.magnet.setServoDuty('1', MAGNET_OFF_DUTY)


 
def get_center():
        global center_distance 
        center_distance = 100
        camera = Camera()
        print("1")
        camera.start_image()
        print("1")
        camera.save_image("center_distance.jpg")  # Save the image with a valid filename
        print("1")
        camera.close()
        print("1")

        # Load the captured image
        image_path = "center_distance.jpg"
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError("Error: Image not loaded. Check the file path.")
        else:
            print('CHAT WE HAVE A DETECTION')
        # Get image dimensions
        h, w, _ = image.shape
        center_x = w // 2  # X-coordinate of image center

        # Load YOLO model
        model = YOLO("my_model.pt")  # Ensure the model path is correct

        # Run YOLO object detection
        results = model(image)

        # Define the target class
        TARGET_CLASS = "capacitor"  # Change as needed
        best_match = None
        min_distance = float("inf")
        direction = 0  # Default direction (0 means no object detected)

        # Process detections
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])  # Class index
                x_min, y_min, x_max, y_max = map(int, box.xyxy[0])  # Bounding box coordinates
                obj_x = (x_min + x_max) // 2  # Object center X-coordinate

                # Compute signed distance from image center
                pixel_distance = obj_x - center_x  # Negative = Left, Positive = Right

                # Find the closest object to the center
                if abs(pixel_distance) < min_distance:
                    min_distance = abs(pixel_distance)
                    best_match = (x_min, y_min, x_max, y_max, obj_x)
                    direction = pixel_distance  # Preserve sign for direction

        # Draw tracking info if an object was found
        if best_match:
            x_min, y_min, x_max, y_max, obj_x = best_match
            print(f"Detected {TARGET_CLASS}: Horizontal Distance from center = {direction:.2f} pixels")
            center_distance =  direction  # Returns signed distance (negative for left, positive for right)

# def test_magnet(magnet: Electromagnet):
#     while True:
        


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Parameter error: Please assign the device")       # Print an error message if no device is specified
        exit()                                                   # Exit the program
    if sys.argv[1] == 'Command' or sys.argv[1] == 'command':
        print("Running Command")
        Start()
    try:
        magnet = Electromagnet()


        while True:
            leftSpeeds = []
            rightSpeeds = []
            print('test')
            get_center()
            print('test')

            while (abs(center_distance) > center_threshold):
                if center_distance > 0:
                    pulse_turn("left", 0.1, 1500)
                    get_center()
                    print(center_distance)
                    #check_error()
                elif center_distance:
                    pulse_turn("right", 0.1, 1500)
                    get_center()
                    print(center_distance)
                    #check_error()
            magnet.enable()
            DropArm()
            center_distance = 100
            pulse_turn("forward", 0.5, 1000)
            time.sleep(1)
            
            PinchIn()
            RaiseArm()
            magnet.disable()
            
            time.sleep(1)

            pulse_turn("backward", 0.5, 1000)
            
            time.sleep(1)
            pulse_turn("right", 1, 2000)
            PinchOut()
            


            
    except KeyboardInterrupt:
        StopAll()




