import cv2
import numpy as np
from typing import Tuple, Optional

def rectify_perspective(
    image: np.ndarray,
    homography_matrix: np.ndarray
) -> np.ndarray:
    """
    Applies homography transformation matrix to rectify image perspective to perpendicular planar view.
    """
    if homography_matrix is None:
        return image.copy()

    height, width = image.shape[:2]
    rectified = cv2.warpPerspective(image, homography_matrix, (width, height))
    return rectified
