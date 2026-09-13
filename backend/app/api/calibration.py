import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.calibration.aruco import detect_aruco_marker
from app.calibration.scale import calibrate_by_known_object
from app.calibration.ruler import calibrate_by_ruler_points

router = APIRouter(prefix="/api/calibration", tags=["Calibration"])

@router.post("/detect")
async def detect_calibration_reference(
    file: UploadFile = File(...),
    reference_size_mm: float = Form(50.0),
    method: str = Form("aruco")
):
    """
    Detects ArUco marker or reference object and computes scale_px_per_mm.
    """
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image encoding.")

    if method == "aruco":
        cal_res, _, _ = detect_aruco_marker(image, reference_size_mm=reference_size_mm)
        return cal_res.model_dump()
    elif method == "known_object":
        cal_res = calibrate_by_known_object(image, custom_diameter_mm=reference_size_mm)
        return cal_res.model_dump()
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported calibration method: {method}")
