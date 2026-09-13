import cv2
import numpy as np
from typing import Tuple, List, Optional
from app.schemas.calibration import CalibrationResult

def calibrate_by_ruler_points(
    pt1: Tuple[float, float],
    pt2: Tuple[float, float],
    known_distance_mm: float = 10.0
) -> CalibrationResult:
    """
    Calculates calibration scale from 2 user-selected ruler points.
    """
    dist_px = float(np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2))
    if dist_px <= 0 or known_distance_mm <= 0:
        return CalibrationResult(
            calibrated=False,
            method="ruler",
            reference_size_mm=known_distance_mm,
            detected_size_px=0.0,
            scale_px_per_mm=1.0,
            error_percent=100.0,
            status="failed",
            details={"reason": "Invalid distance between points."}
        )

    scale = dist_px / known_distance_mm
    return CalibrationResult(
        calibrated=True,
        method="ruler",
        reference_size_mm=known_distance_mm,
        detected_size_px=round(dist_px, 2),
        scale_px_per_mm=round(scale, 4),
        error_percent=1.0,  # Estimated manual selection uncertainty 1%
        perspective_corrected=False,
        uncertainty_percent=1.0,
        status="valid",
        details={"pt1": list(pt1), "pt2": list(pt2)}
    )
