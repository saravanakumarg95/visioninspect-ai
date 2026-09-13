import os
import cv2
import pytest
from app.calibration.aruco import detect_aruco_marker

def test_aruco_calibration_detection():
    sample_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sample_data/bolt_aruco.png"))
    assert os.path.exists(sample_path), f"Sample image does not exist at {sample_path}"

    image = cv2.imread(sample_path)
    assert image is not None

    cal_res, homography, corners = detect_aruco_marker(image, reference_size_mm=50.0)

    assert cal_res.calibrated is True
    assert cal_res.method == "aruco"
    assert cal_res.reference_size_mm == 50.0
    assert cal_res.scale_px_per_mm > 5.0
    assert cal_res.status == "valid"
    assert homography is not None
