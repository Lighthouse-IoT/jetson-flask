from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from check import capture_image
from fastapi.middleware.cors import CORSMiddleware
import requests
import test_run as t
import test_cam as tc
import yolo8 as pre
import eye
import yolo_eye as ye
import random

import os

from dotenv import load_dotenv

import router.study_router as study_router

load_dotenv()

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(study_router.router)

@app.get("/")
def root():
  return {"message":"^^7"}

@app.get("/read-file")
def file_test():
  return t.current_date()

@app.get("/yeye")
def test_yeye():
  data = ye.show_camera()
  return data  

@app.get("/eye")
def test_eye():
  data = eye.main()
  print(data)
  return data

@app.get("/check")
async def get_photo():
  try:
    filepath  = capture_image()
    
  # 파일을 클라이언트에 전달 후 삭제
    response = FileResponse(filepath, media_type="image/jpeg", filename=os.path.basename(filepath))
    response.headers["Cache-Control"] = "no-cache"
    response.background = remove_file_after_response(filepath)
    return response
  
  except Exception as e:
      return {"error": str(e)}

def remove_file_after_response(filepath: str):
    from starlette.background import BackgroundTask
    return BackgroundTask(lambda: os.remove(filepath))

@app.get("/test")
def test_send(userId: str = ''):
  url = os.environ.get("NODE_SERVER_URL")
  # zero_one = random.randrange(0,2)
  # t.current_date()
  data = pre.show_camera()
  
  print(data)
  print("호출함!")
  
  return {"isStudy":data, "userId":userId}
  # tc.save_image()
  # try:
  #   response = requests.get(url)
  #   print(url)
  #   if response.status_code == 200:
  #     print(response.json()['message'])
  #     return zero_one
  # except:
  #   print("Error", response.status_code)
  #   return None