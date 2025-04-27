from fastapi import FastAPI, UploadFile, File, HTTPException
from tensorflow.keras.layers import LocallyConnected2D
from deepface import DeepFace
import cv2
import numpy as np
from sqlalchemy import create_engine, text
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Service2")

# Конфигурация БД
DATABASE_URL = "postgresql://admin:secret@localhost/tracking"

# Детекция лиц через OpenCV (каскады Хаара)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def get_employee_id(embedding) -> int | None:
    """Поиск сотрудника по эмбеддингу."""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            query = text("""
                SELECT id 
                FROM employees 
                WHERE l2_distance(embedding, :embedding) < 0.6
                LIMIT 1
            """)
            result = conn.execute(query, {"embedding": embedding.tolist()})
            return result.scalar()
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")
        return None


@app.post("/process")
async def process_frame(camera_id: str, file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Детекция лиц через OpenCV
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        detected_data = []

        for (x, y, w, h) in faces:
            face_roi = image[y:y + h, x:x + w]

            # Распознавание через DeepFace с бэкендом OpenCV
            embedding = DeepFace.represent(
                face_roi,
                model_name="Facenet",
                detector_backend="opencv"  # Используем OpenCV вместо dlib
            )[0]["embedding"]

            # Поиск в БД
            employee_id = get_employee_id(embedding)

            # Сохранение в БД
            engine = create_engine(DATABASE_URL)
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO detections 
                    (timestamp, employee_id, camera_id) 
                    VALUES (NOW(), :eid, :cid)
                """), {"eid": employee_id, "cid": camera_id})
                conn.commit()

            detected_data.append({"employee_id": employee_id, "camera_id": camera_id})

        return {"detections": detected_data}

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    import os

    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # Отключает oneDNN warnings
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    uvicorn.run(app, host="0.0.0.0", port=8006)
