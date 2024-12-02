from fastapi import APIRouter
from datetime import timedelta, datetime, timezone

router = APIRouter(
  prefix="/study"
)

@router.get("/time", description="study - 공부시간 전송")
def send_time():
  
  now = datetime.now(timezone(timedelta(hours=9)))
  end = now + timedelta(hours=2)
  print(end)
  return {"start_time":now, "end_time":end}

