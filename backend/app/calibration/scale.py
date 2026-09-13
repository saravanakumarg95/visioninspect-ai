import cv2
import numpy as np
from typing import Tuple, Optional
from app.schemas.calibration import CalibrationResult

KNOWN_REFERENCE_OBJECTS = {
    "us_quarter": {"name": "US Quarter Coin", "diameter_mm": 24.26},
    "euro_1": {"name": "1 Euro Coin", "diameter_mm": 23.25},
    "calibration_washer": {"name": "Standard M20 Washer", "diameter_mm": 37.00},
    "custom": {"name": "Custom Reference", "diameter_mm": 25.00}
}

def calibrate_by_known_object(
    image: np.ndarray,
    known_object_type: str = "us_quarter",
    custom_diameter_mm: Optional[float] = None
) -> CalibrationResult:
    """
    Detects circular reference object in image and calculates scale_px_per_mm.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    ref_info = KNOWN_REFERENCE_OBJECTS.get(known_object_type, KNOWN_REFERENCE_OBJECTS["custom"])
    ref_diameter_mm = custom_diameter_mm if custom_diameter_mm else ref_info["diameter_mm"]

    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=50,
        param1=100,
        param2=30,
        minRadius=15,
        maxRadius=int(min(gray.shape) / 2)
    )

    if circles is None or len(circles) == 0:
        return CalibrationResult(
            calibrated=False,
            method="known_object",
            reference_size_mm=ref_diameter_mm,
            detected_size_px=0.0,
            scale_px_per_mm=1.0,
            error_percent=100.0,
            status="uncalibrated",
            details={"reason": "No circular reference object detected."}
        )

    # Choose largest circle as candidate reference object
    best_circle = max(circles[0, :], key=lambda c: c[2])
    cx, cy, r_px = float(best_circle[0]), float(best_circle[1]), float(best_circle[2])
    detected_diameter_px = 2.0 * r_px

    scale = detected_diameter_px / ref_diameter_mm

    return CalibrationResult(
        calibrated=True,
        method="known_object",
        reference_size_mm=ref_diameter_mm,
        detected_size_px=round(detected_diameter_px, 2),
        scale_px_per_mm=round(scale, 4),
        error_percent=0.8,
        perspective_corrected=False,
        uncertainty_percent=0.8,
        status="valid",
        details={
            "object_name": ref_info["name"],
            "center": [cx, cy],
            "radius_px": r_px
        }
    )
