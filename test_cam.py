import cv2
import random

def save_image():
  capture = cv2.VideoCapture(1)
  capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
  ret, frame = capture.read()
  # cv2.imshow("VideoFrame", frame)
  # print(frame)

  random_path = random.randrange(1001,9999)

  cv2.imwrite(f"test_{random_path}.jpg",frame)
  
  capture.release()
  cv2.destroyAllWindows()


