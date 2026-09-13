import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.cv.preprocessing import analyze_image_quality

router = APIRouter(prefix="/api/camera", tags=["Camera & Quality"])

@router.post("/quality-check")
async def check_quality(file: UploadFile = File(...)):
    """
    Analyzes camera capture frame quality (blur, exposure, glare, coverage, perspective).
    """
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image file format.")

    quality = analyze_image_quality(image)
    return quality.model_dump()
