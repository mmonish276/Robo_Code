import cv2
import torch
import numpy as np
from ultralytics import YOLO
import time
import RPi.GPIO as GPIO

# Load your YOLOv5 model
model = YOLO("my_model.pt")  # Load trained model

# Initialize camera
cap = cv2.VideoCapture(0)

# PID controller variables
Kp = 0.01   # Proportional gain (adjust for turning speed)
Kd = 0.005  # Derivative gain (reduces wobbling)
previous_error = 0
TURN_THRESHOLD = 15  # How close to the center before stopping

# Frame width (assuming 640x480 resolution)
FRAME_WIDTH = 640  
FRAME_CENTER = FRAME_WIDTH // 2

# Motor setup
LEFT_MOTOR = 17
RIGHT_MOTOR = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_MOTOR, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR, GPIO.OUT)

# Motor control functions
def move_forward():
    GPIO.output(LEFT_MOTOR, True)
    GPIO.output(RIGHT_MOTOR, True)

def turn_left():
    GPIO.output(LEFT_MOTOR, False)
    GPIO.output(RIGHT_MOTOR, True)

def turn_right():
    GPIO.output(LEFT_MOTOR, True)
    GPIO.output(RIGHT_MOTOR, False)

def stop_motors():
    GPIO.output(LEFT_MOTOR, False)
    GPIO.output(RIGHT_MOTOR, False)

def get_motor_correction(error, previous_error):
    """PID-based correction for small turning adjustments"""
    correction = Kp * error + Kd * (error - previous_error)
    previous_error = error
    return correction, previous_error

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv5 model on frame
    results = model(frame)

    capacitor_center_x = None  # Store detected capacitor center
    for result in results:
        for box in result.boxes:  # Loop through detected objects
            class_id = int(box.cls[0])  # Get class ID

            # Check if class is "capacitor" (change class_id based on your training)
            if class_id == 0:  # Assuming class 0 is capacitor
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
                capacitor_center_x = (x1 + x2) // 2  # Find center of capacitor

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (capacitor_center_x, (y1 + y2) // 2), 5, (0, 0, 255), -1)

    if capacitor_center_x is not None:
        alignment_error = capacitor_center_x - FRAME_CENTER  # Compute error
        correction, previous_error = get_motor_correction(alignment_error, previous_error)

        # Use correction value to adjust motors in small increments
        if abs(alignment_error) > TURN_THRESHOLD:
            if alignment_error > 0:
                print("Turning Right (small step)")
                turn_right()
            elif alignment_error < 0:
                print("Turning Left (small step)")
                turn_left()
        else:
            print("Centered! Stopping motors.")
            stop_motors()

    cv2.imshow("Frame", frame)  # Show video feed

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
