import cv2
import numpy as np
from ultralytics import YOLO
from camera import Camera

class Dist:
    camera = Camera()
    camera.__init__()
    camera.start_image()
    camera.save_image(camera, )

    def getCenter():
        center_distance = 100
        #Load the image
        image_path = "center_distance.jpg"
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError("Error: Image not loaded. Check the file path.")

        #Get image dimensions
        h, w, _ = image.shape
        center_x, center_y = w // 2, h // 2  # Image center

        #Load YOLO model
        model = YOLO("my_model.pt")  # Ensure the model path is correct

        #Run YOLO object detection
        results = model(image)  

        #Define the target class
        TARGET_CLASS = "resistor"  # Change as needed
        best_match = None
        min_distance = float("inf")

        #Process detections
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])  # Class index
                x_min, y_min, x_max, y_max = map(int, box.xyxy[0])  # Bounding box coordinates
                obj_x = (x_min + x_max) // 2
                obj_y = (y_min + y_max) // 2

            # Compute Euclidean distance from image center
            pixel_distance = abs(obj_x - center_x)

            if pixel_distance < min_distance:
                min_distance = pixel_distance
                best_match = (x_min, y_min, x_max, y_max, obj_x, obj_y)
        #Draw tracking info if an object was found
        if best_match:
            x_min, y_min, x_max, y_max, obj_x, obj_y = best_match
            print(f"Detected {TARGET_CLASS}: Horizontal Distance from center = {min_distance:.2f} pixels")
            center_distance = min_distance
    
    def getRawDist():
        x = 1

