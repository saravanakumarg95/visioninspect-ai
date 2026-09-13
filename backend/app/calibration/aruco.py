import cv2
import numpy as np
from typing import Tuple, Optional, Dict, Any
from app.schemas.calibration import CalibrationResult

ARUCO_DICT_MAP = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}

def detect_aruco_marker(
    image: np.ndarray,
    reference_size_mm: float = 50.0,
    aruco_dict_name: str = "DICT_4X4_50",
    expected_id: Optional[int] = None
) -> Tuple[CalibrationResult, Optional[np.ndarray], Optional[np.ndarray]]:
    """
    Detects ArUco marker in image, calculates scale_px_per_mm, homography matrix, and calibration error.
    Returns: (CalibrationResult, homography_matrix, corners)
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    dict_type = ARUCO_DICT_MAP.get(aruco_dict_name, cv2.aruco.DICT_4X4_50)
    aruco_dict = cv2.aruco.getPredefinedDictionary(dict_type)

    # Detect ArUco markers (compatible with OpenCV 4.x / 5.x)
    try:
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, rejected = detector.detectMarkers(gray)
    except AttributeError:
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is None or len(corners) == 0:
        return CalibrationResult(
            calibrated=False,
            method="aruco",
            reference_size_mm=reference_size_mm,
            detected_size_px=0.0,
            scale_px_per_mm=1.0,
            error_percent=100.0,
            perspective_corrected=False,
            status="uncalibrated",
            details={"reason": "No ArUco marker detected in frame."}
        ), None, None

    # Pick target marker (matching expected_id or first detected)
    selected_idx = 0
    if expected_id is not None and len(ids) > 0:
        found = False
        for idx, marker_id in enumerate(ids.flatten()):
            if marker_id == expected_id:
                selected_idx = idx
                found = True
                break

    pts = corners[selected_idx][0]  # 4 corner points (top-left, top-right, bottom-right, bottom-left)
    marker_id = int(ids.flatten()[selected_idx])

    # Refine corners with sub-pixel precision
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
    pts_sub = cv2.cornerSubPix(gray, np.float32(pts), (5, 5), (-1, -1), criteria)

    # Calculate side lengths in pixels
    side0 = float(np.linalg.norm(pts_sub[0] - pts_sub[1]))  # Top edge
    side1 = float(np.linalg.norm(pts_sub[1] - pts_sub[2]))  # Right edge
    side2 = float(np.linalg.norm(pts_sub[2] - pts_sub[3]))  # Bottom edge
    side3 = float(np.linalg.norm(pts_sub[3] - pts_sub[0]))  # Left edge

    mean_side_px = (side0 + side1 + side2 + side3) / 4.0
    scale_px_per_mm = mean_side_px / reference_size_mm

    # Calibration error percentage (variance among 4 side lengths)
    side_std = float(np.std([side0, side1, side2, side3]))
    error_percent = float((side_std / mean_side_px) * 100.0) if mean_side_px > 0 else 0.0

    # Compute Homography matrix for perspective correction to ideal square of reference_size_mm
    dst_size_px = mean_side_px
    dst_pts = np.array([
        [0, 0],
        [dst_size_px, 0],
        [dst_size_px, dst_size_px],
        [0, dst_size_px]
    ], dtype=np.float32)

    homography, _ = cv2.findHomography(pts_sub, dst_pts)

    res = CalibrationResult(
        calibrated=True,
        method="aruco",
        reference_size_mm=reference_size_mm,
        detected_size_px=round(mean_side_px, 2),
        scale_px_per_mm=round(scale_px_per_mm, 4),
        error_percent=round(error_percent, 2),
        perspective_corrected=True,
        homography_matrix=homography.tolist() if homography is not None else None,
        uncertainty_percent=round(max(0.2, error_percent), 2),
        status="valid",
        details={
            "marker_id": marker_id,
            "side_lengths_px": [round(s, 2) for s in [side0, side1, side2, side3]],
            "corners": pts_sub.tolist()
        }
    )

    return res, homography, pts_sub
