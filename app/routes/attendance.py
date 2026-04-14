from fastapi import APIRouter, UploadFile, File
import numpy as np
import cv2

from app.services.face_service import train_model, recognize_face
from app.services.attendance_service import mark_attendance

router = APIRouter()

label_map = {}

@router.post("/attendance")
async def attendance_api(image: UploadFile = File(...)):
    global label_map

    contents = await image.read()

    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    label_map = train_model()

    if not label_map:
        return {"status": "fail", "message": "No data trained"}

    user = recognize_face(img, label_map)

    if not user:
        return {"status": "fail", "message": "Face not recognized"}

    message = mark_attendance(user)

    return {"status": "success", "message": message, "user": user}