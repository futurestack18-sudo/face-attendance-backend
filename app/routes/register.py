from fastapi import APIRouter, UploadFile, File, Form
import numpy as np
import cv2
import os

router = APIRouter()

DATASET_PATH = "dataset"

@router.post("/register-face")
async def register_face(name: str = Form(...), image: UploadFile = File(...)):
    contents = await image.read()

    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    user_path = os.path.join(DATASET_PATH, name)
    os.makedirs(user_path, exist_ok=True)

    count = len(os.listdir(user_path))
    file_path = os.path.join(user_path, f"{count}.jpg")

    cv2.imwrite(file_path, img)

    return {"message": "Face saved"}