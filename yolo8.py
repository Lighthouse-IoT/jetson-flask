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
    model = YOLO("last.pt")
    eye_model = YOLO("yolov8_eyes_last.pt")

  
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
                                                                               
    if cap.isOpened():
        ret_val, img = cap.read()
        results = model(img)
        eye_results = eye_model(img)


        cap.release()
        cv2.destroyAllWindows()

        # 자세 모델
        if results[0].boxes is None or results[0].boxes.cls is None:
            detected_classes = []
        else:
            detected_classes = [model.names[int(cls)] for cls in results[0].boxes.cls]
        
        # 눈 모델
        if eye_results[0].boxes is None or eye_results[0].boxes.cls is None:
            eye_detected_classes = []
        else:
            eye_detected_classes = [eye_model.names[int(cls)] for cls in eye_results[0].boxes.cls]
        
        detect_result = 0
        # Logic to determine return value
        if "BAD" in detected_classes and "STUDY" in detected_classes:
            detect_result = 1
        elif "BAD" in detected_classes:
            detect_result = 0
        elif "STUDY" in detected_classes:
            detect_result = 1
        else:
            detect_result = 0

        if detect_result == 1:
            closed_variants = {"closed", "closeds"}
            open_variants = {"open", "opens"}
            
            # detected_classes와 eye_detected_classes를 set으로 변환
            detected_classes_set = set(detected_classes)
            eye_detected_classes_set = set(eye_detected_classes)

            if detected_classes_set & closed_variants and detected_classes_set & open_variants:
                print("close and open")
                detect_result = 1
            elif eye_detected_classes_set & open_variants:
                print("open")
                detect_result = 1
            elif eye_detected_classes_set & closed_variants:
                print("close")
                detect_result = 0

            else:
                detect_result = 0


        return detect_result
    else:
        print("Unable to open camera")
        return 0
