import cv2
import numpy as np
from typing import Tuple, Optional, Dict, Any

def apply_lens_undistortion(
    image: np.ndarray,
    camera_matrix: Optional[np.ndarray] = None,
    dist_coeffs: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, bool]:
    """
    Applies radial and tangential lens distortion correction if camera calibration parameters exist.
    If unavailable, returns original image with status False.
    """
    if camera_matrix is None or dist_coeffs is None:
        return image, False

    height, width = image.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (width, height), 1, (width, height))
    undistorted = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)
    return undistorted, True
