import cv2
import dlib
from scipy.spatial import distance

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

def calculate_ear(eye):
    A = distance.euclidean((eye[1].x, eye[1].y), (eye[5].x, eye[5].y))
    B = distance.euclidean((eye[2].x, eye[2].y), (eye[4].x, eye[4].y))
    C = distance.euclidean((eye[0].x, eye[0].y), (eye[3].x, eye[3].y))
    ear = (A + B) / (2.0 * C)
    return ear * 2

def initialize_detector(predictor_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)
    return detector, predictor

def process_frame(frame, detector, predictor, ear_threshold=0.40, consec_frames=1):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = detector(gray)
    frame_counter = 0
    detect = 0
    print(faces)
    for face in faces:
        landmarks = predictor(gray, face)
        
        left_eye = [landmarks.part(i) for i in range(36, 42)]
        right_eye = [landmarks.part(i) for i in range(42, 48)]
        left_ear = calculate_ear(left_eye)
        right_ear = calculate_ear(right_eye)
        ear = (left_ear + right_ear) / 2.2
        print(ear)
        if ear < ear_threshold:
            frame_counter += 1
        else:
            frame_counter = 0
        
        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        detect = 1
        if frame_counter >= consec_frames:
            cv2.putText(frame, "Dozing", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            detect = 0

    return frame, detect

def main(predictor_path='shape_predictor_68_face_landmarks.dat'):
    detector, predictor = initialize_detector(predictor_path)
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("ERROR: Could not open video stream.")
        return
    
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Could not read frame.")
        return

    frame, detect = process_frame(frame, detector, predictor)
    # cv2.imwrite("test_output.jpg", frame)
    print(f"Detection result: {detect}")
        
    cap.release()
    cv2.destroyAllWindows()
    return detect
