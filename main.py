from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import test_run as t
import test_cam as tc
import yolo8 as pre
import eye
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

@app.get("/eye")
def test_eye():
  data = eye.main()
  print(data)
  return data

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