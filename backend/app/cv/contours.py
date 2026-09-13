import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict, Any

def extract_component_contours(
    image: np.ndarray,
    exclude_corners: Optional[np.ndarray] = None
) -> Tuple[Optional[np.ndarray], List[np.ndarray], Dict[str, Any]]:
    """
    Extracts main mechanical component contour from image, ignoring calibration marker region.
    Returns: (main_contour, all_contours, metadata)
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    height, width = gray.shape[:2]

    # Mask out calibration reference if provided
    mask = np.ones((height, width), dtype=np.uint8) * 255
    if exclude_corners is not None:
        pts = np.int32(exclude_corners)
        cv2.fillPoly(mask, [pts], 0)

    masked_gray = cv2.bitwise_and(gray, gray, mask=mask)

    # Adaptive thresholding + Otsu
    blurred = cv2.GaussianBlur(masked_gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Morphological close to bridge tiny breaks
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, [], {}

    # Filter out noise & ArUco leftover
    valid_contours = []
    min_area = (height * width) * 0.005  # At least 0.5% frame size
    max_area = (height * width) * 0.85

    for c in contours:
        area = cv2.contourArea(c)
        if min_area <= area <= max_area:
            valid_contours.append(c)

    if not valid_contours:
        return None, [], {}

    # Main component is the largest valid contour
    main_contour = max(valid_contours, key=cv2.contourArea)

    # Calculate shape descriptors
    area = float(cv2.contourArea(main_contour))
    perimeter = float(cv2.arcLength(main_contour, True))
    rect = cv2.minAreaRect(main_contour)
    (cx, cy), (w, h), angle = rect
    aspect_ratio = float(max(w, h) / max(0.1, min(w, h)))
    hull = cv2.convexHull(main_contour)
    hull_area = cv2.contourArea(hull)
    solidity = float(area / max(1.0, hull_area))

    metadata = {
        "area_px": area,
        "perimeter_px": perimeter,
        "centroid": [cx, cy],
        "min_rect": {"center": [cx, cy], "size": [w, h], "angle": angle},
        "aspect_ratio": aspect_ratio,
        "solidity": solidity
    }

    return main_contour, valid_contours, metadata
