from fastapi import FastAPI, UploadFile, File, HTTPException
import cv2
import numpy as np
import requests
import os
from pathlib import Path

app = FastAPI()

# Создаем папку для временного хранения кадров
Path("received_frames").mkdir(exist_ok=True)


@app.post("/send_frame")
async def send_frame(camera_id: str, file: UploadFile = File(...)):
    """
    Принимает кадр с камеры и отправляет его в service2.

    Параметры:
    - camera_id: ID камеры (например, "cam_1").
    - file: Изображение в формате JPEG/PNG.
    """
    try:
        # Сохраняем кадр временно
        image_data = await file.read()
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        frame_path = f"received_frames/{camera_id}.jpg"
        cv2.imwrite(frame_path, image)

        # Отправляем кадр в service2
        with open(frame_path, "rb") as f:
            response = requests.post(
                "http://service2:8001/process",
                files={"file": (frame_path, f, "image/jpeg")},
                data={"camera_id": camera_id}
            )

        # Удаляем временный файл
        os.remove(frame_path)

        return {"status": "success", "response": response.json()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
