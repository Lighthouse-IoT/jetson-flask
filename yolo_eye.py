# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image
 
import cv2
from ultralytics import YOLO
 
def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def show_camera():
  model = YOLO("yolov8_eyes_last.pt")
  
  # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
  cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
                                                                              
  if cap.isOpened():
      ret_val, img = cap.read()
      results = model(img, save=True)

      cap.release()
      cv2.destroyAllWindows()

      # Handle results and detect classes
      if results[0].boxes is None or results[0].boxes.cls is None:
          detected_classes = []
      else:
          detected_classes = [model.names[int(cls)] for cls in results[0].boxes.cls]

      # Logic to determine return value
      if "BAD" in detected_classes and "STUDY" in detected_classes:
          return 0
      elif "BAD" in detected_classes:
          return 0
      elif "STUDY" in detected_classes:
          return 1
      else:
          return 0  # Default value if neither is detected
  else:
      print("Unable to open camera")
      return -1

