import cv2
import numpy as np
from ultralytics import YOLO
from camera import Camera

class Dist:
    def get_center(self):
        self.camera = Camera()
        self.camera.save_image("center_distance.jpg")  # Save the image with a valid filename
        self.camera.close()

        # Load the captured image
        image_path = "center_distance.jpg"
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError("Error: Image not loaded. Check the file path.")

        # Get image dimensions
        h, w, _ = image.shape
        center_x = w // 2  # X-coordinate of image center

        # Load YOLO model
        model = YOLO("my_model.pt")  # Ensure the model path is correct

        # Run YOLO object detection
        results = model(image)

        # Define the target class
        TARGET_CLASS = "resistor"  # Change as needed
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
            return direction  # Returns signed distance (negative for left, positive for right)

        return None  # If no object was detected


