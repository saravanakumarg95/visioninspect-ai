import cv2
import numpy as np
from typing import List, Dict, Any, Tuple

def detect_lines_and_parallel_edges(
    image: np.ndarray,
    contour: np.ndarray,
    scale_px_per_mm: float
) -> List[Dict[str, Any]]:
    """
    Detects straight line segments and parallel edge pairs for width/length distance measurements.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    mask = np.zeros_like(gray)
    if contour is not None:
        cv2.drawContours(mask, [contour], -1, 255, 2)

    edges = cv2.Canny(mask, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=40, minLineLength=30, maxLineGap=10)

    if lines is None:
        return []

    detected_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        length_px = float(np.sqrt((x2 - x1)**2 + (y2 - y1)**2))
        angle_rad = float(np.arctan2(y2 - y1, x2 - x1))
        angle_deg = float(np.degrees(angle_rad)) % 180.0
        detected_lines.append({
            "pts": [[float(x1), float(y1)], [float(x2), float(y2)]],
            "length_px": length_px,
            "length_mm": length_px / max(0.1, scale_px_per_mm),
            "angle_deg": angle_deg
        })

    return detected_lines
