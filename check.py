import cv2
import uuid
import os

# GStreamer Pipeline 설정 (CSI 카메라)
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=30,
    flip_method=0,
):
    return (
        f"nvarguscamerasrc sensor-id={sensor_id} ! "
        f"video/x-raw(memory:NVMM), width=(int){capture_width}, height=(int){capture_height}, "
        f"format=(string)NV12, framerate=(fraction){framerate}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)BGRx ! "
        f"videoconvert ! video/x-raw, format=(string)BGR ! appsink"
    )

def capture_image(output_dir="/tmp"):
    # 카메라 초기화
    camera = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if not camera.isOpened():
        raise RuntimeError("Could not open CSI camera")

    # 사진 촬영
    ret, frame = camera.read()
    camera.release()

    if not ret:
        raise RuntimeError("Failed to capture image")

    # 파일 저장
    filename = f"capture_{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(output_dir, filename)
    cv2.imwrite(filepath, frame)
    return filepath
