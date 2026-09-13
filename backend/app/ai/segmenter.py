import cv2
import numpy as np
from typing import Tuple, Optional

def segment_component_mask(image: np.ndarray, contour: np.ndarray) -> np.ndarray:
    """
    Generates binary segmentation mask of component.
    """
    height, width = image.shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)
    if contour is not None:
        cv2.drawContours(mask, [contour], -1, 255, -1)
    return mask
